#!/usr/bin/env python3
import json
import urllib.request
import os
import sys
import smtplib
import html
import urllib.parse
from datetime import datetime, timezone, tzinfo, timedelta
from pathlib import Path
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Try to import ZoneInfo (with fallback for Windows without tzdata package)
try:
    from zoneinfo import ZoneInfo
    # Test instantiation
    ZoneInfo("America/Sao_Paulo")
except Exception:
    class ZoneInfoFallback(tzinfo):
        def __init__(self, key):
            if key != "America/Sao_Paulo":
                raise ValueError(
                    "Timezone data is unavailable. Install tzdata or use America/Sao_Paulo."
                )
            self.key = key
        def utcoffset(self, dt):
            return timedelta(hours=-3)
        def tzname(self, dt):
            return "BRT"
        def dst(self, dt):
            return timedelta(0)
    ZoneInfo = ZoneInfoFallback

API_URL = "https://chatgpt.com/backend-api/wham/rate-limit-reset-credits"
AUTH_PATH = Path.home() / ".codex" / "auth.json"
try:
    from see_resets import TIMEZONE as DEFAULT_TIMEZONE
except ImportError:
    DEFAULT_TIMEZONE = "America/Sao_Paulo"
DAYS_THRESHOLD = 10


def load_env():
    env_paths = [
        Path.cwd() / ".env",
        Path(__file__).resolve().parent.parent / ".env"
    ]
    loaded = False
    for path in env_paths:
        if path.exists():
            for line in path.read_text(encoding='utf-8').splitlines():
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                if '=' in line:
                    key, val = line.split('=', 1)
                    key = key.strip()
                    val = val.strip().strip('"').strip("'")
                    os.environ[key] = val
            loaded = True
            break
    return loaded


def fmt_time_left(time_left):
    days = time_left.days
    hours, remainder = divmod(time_left.seconds, 3600)
    minutes, _ = divmod(remainder, 60)

    parts = []
    if days > 0:
        parts.append(f"{days} dia{'s' if days > 1 else ''}")
    if hours > 0:
        parts.append(f"{hours} hora{'s' if hours > 1 else ''}")
    if minutes > 0:
        parts.append(f"{minutes} minuto{'s' if minutes > 1 else ''}")

    return ", ".join(parts) if parts else "menos de um minuto"


def configured_timezone_name():
    return os.environ.get("TIMEZONE", DEFAULT_TIMEZONE)


def parse_api_datetime(timestamp):
    parsed = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        return parsed.replace(tzinfo=timezone.utc)
    return parsed


def fmt_utc_offset(dt):
    offset = dt.utcoffset()
    if offset is None:
        return "UTC"

    total_minutes = int(offset.total_seconds() // 60)
    sign = "+" if total_minutes >= 0 else "-"
    total_minutes = abs(total_minutes)
    hours, minutes = divmod(total_minutes, 60)
    return f"UTC{sign}{hours:02d}:{minutes:02d}"


def fmt_local_expiry(timestamp, timezone_name=None):
    timezone_name = timezone_name or configured_timezone_name()
    local_tz = ZoneInfo(timezone_name)
    local_expiry = parse_api_datetime(timestamp).astimezone(local_tz)
    return local_expiry.strftime("%d/%m/%Y às %H:%M:%S")


def configured_notify_channel():
    return os.environ.get("NOTIFY_CHANNEL", "email").strip().lower()


def required_config_vars(channel):
    if channel == "email":
        return ['SMTP_HOST', 'SMTP_PORT', 'SMTP_USER', 'SMTP_PASSWORD', 'EMAIL_FROM', 'EMAIL_TO']
    if channel == "telegram":
        return ['TELEGRAM_BOT_TOKEN', 'TELEGRAM_CHAT_ID']
    print(f"Erro: NOTIFY_CHANNEL inválido: {channel}. Use 'email' ou 'telegram'.", file=sys.stderr)
    sys.exit(1)


def build_notification(all_resets):
    subject = "[ChatGPT Reset] Alerta de Expiração de Limite de Uso"

    body_lines = [
        "Este é um alerta automático informando sobre os seus créditos de uso do ChatGPT.",
        "Abaixo estão todos os seus resets ativos:",
        ""
    ]
    for r in all_resets:
        if r["is_expiring"]:
            body_lines.append(f"- Expira em: {r['expiry_date']} (Tempo restante: {r['time_left_str']}) [PRESTES A EXPIRAR]")
        else:
            body_lines.append(f"- Expira em: {r['expiry_date']} (Tempo restante: {r['time_left_str']})")

    body_lines.extend([
        "",
        "Por favor, planeje o uso da sua conta adequadamente.",
        "",
        "Atenciosamente,",
        "Script de Alerta de Resets"
    ])
    body = "\n".join(body_lines)

    html_lines = [
        "<html>",
        "<body>",
        "<p>Olá,</p>",
        "<p>Este é um alerta automático informando sobre os seus créditos de uso do ChatGPT.</p>",
        "<p>Abaixo estão todos os seus resets ativos:</p>",
        "<ul>"
    ]
    for r in all_resets:
        if r["is_expiring"]:
            html_lines.append(
                f"  <li><strong><span style=\"color: red;\">Expira em: {r['expiry_date']} (Tempo restante: {r['time_left_str']}) [PRESTES A EXPIRAR]</span></strong></li>"
            )
        else:
            html_lines.append(
                f"  <li>Expira em: {r['expiry_date']} (Tempo restante: {r['time_left_str']})</li>"
            )

    html_lines.extend([
        "</ul>",
        "<p>Por favor, planeje o uso da sua conta adequadamente.</p>",
        "<p>Atenciosamente,<br>Script de Alerta de Resets</p>",
        "</body>",
        "</html>"
    ])
    html_body = "\n".join(html_lines)

    return subject, body, html_body


def build_telegram_notification(all_resets):
    expiring_count = sum(1 for r in all_resets if r["is_expiring"])
    lines = [
        "<b>ChatGPT Reset</b>",
        f"<b>{expiring_count} reset(s) prestes a expirar</b>",
        "",
        "Resets ativos:",
        "",
    ]

    for index, r in enumerate(all_resets, start=1):
        expiry_date = html.escape(r["expiry_date"])
        time_left = html.escape(r["time_left_str"])
        if r["is_expiring"]:
            lines.extend([
                f"<b>{index}. Expira em {expiry_date}</b>",
                f"Tempo restante: <b>{time_left}</b>",
                "<b>PRESTES A EXPIRAR</b>",
                "",
            ])
        else:
            lines.extend([
                f"{index}. Expira em {expiry_date}",
                f"Tempo restante: {time_left}",
                "",
            ])

    return "\n".join(lines)


def send_email(subject, body, html_body):
    msg = MIMEMultipart('alternative')
    msg['From'] = os.environ['EMAIL_FROM']
    msg['To'] = os.environ['EMAIL_TO']
    msg['Subject'] = subject

    part1 = MIMEText(body, 'plain', 'utf-8')
    part2 = MIMEText(html_body, 'html', 'utf-8')
    msg.attach(part1)
    msg.attach(part2)

    host = os.environ['SMTP_HOST']
    port = int(os.environ['SMTP_PORT'])
    user = os.environ['SMTP_USER']
    password = os.environ['SMTP_PASSWORD']

    if port == 465:
        server = smtplib.SMTP_SSL(host, port, timeout=30)
    else:
        server = smtplib.SMTP(host, port, timeout=30)
        server.starttls()

    server.login(user, password)
    server.send_message(msg)
    server.quit()


def send_telegram(body):
    token = os.environ['TELEGRAM_BOT_TOKEN']
    chat_id = os.environ['TELEGRAM_CHAT_ID']
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = urllib.parse.urlencode({
        "chat_id": chat_id,
        "text": body,
        "parse_mode": "HTML",
        "disable_web_page_preview": "true",
    }).encode()
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
    }

    request = urllib.request.Request(url, data=payload, headers=headers, method="POST")
    response = json.loads(urllib.request.urlopen(request, timeout=30).read().decode())
    if not response.get("ok"):
        raise RuntimeError(response)


def main():
    if not load_env():
        print("Aviso: Nenhum arquivo .env encontrado. Usando variáveis de ambiente do sistema.")

    notify_channel = configured_notify_channel()
    required_vars = required_config_vars(notify_channel)
    missing = [var for var in required_vars if not os.environ.get(var)]
    if missing:
        print(f"Erro: Faltam as seguintes variáveis de configuração no .env ou ambiente: {', '.join(missing)}")
        sys.exit(1)

    if not AUTH_PATH.exists():
        print(f"Erro: O arquivo de autenticação {AUTH_PATH} não foi encontrado.", file=sys.stderr)
        sys.exit(1)

    # Read Auth details
    try:
        auth = json.loads(AUTH_PATH.read_text())
        tokens = auth["tokens"]
    except Exception as e:
        print(f"Erro ao ler o arquivo {AUTH_PATH}: {e}", file=sys.stderr)
        sys.exit(1)

    headers = {
        "Authorization": f"Bearer {tokens['access_token']}",
        "OpenAI-Beta": "codex-1",
        "originator": "Codex Desktop",
    }

    account_id = tokens.get("account_id")
    if account_id:
        headers["ChatGPT-Account-ID"] = account_id

    # Fetch credits
    try:
        request = urllib.request.Request(API_URL, headers=headers)
        payload = json.loads(urllib.request.urlopen(request, timeout=30).read().decode())
    except Exception as e:
        print(f"Erro ao consultar a API de resets: {e}", file=sys.stderr)
        sys.exit(1)

    credits = payload.get("credits") or []
    now = datetime.now(timezone.utc)
    
    resets_data = []
    for c in credits:
        expires_at_str = c.get("expires_at")
        if not expires_at_str:
            continue
        
        expires_at = parse_api_datetime(expires_at_str)
        time_left = expires_at - now
        
        # Only show active resets (not already expired)
        if time_left.total_seconds() >= 0:
            resets_data.append((expires_at, expires_at_str, time_left))
            
    # Sort resets by expiration date
    resets_data.sort(key=lambda x: x[0])
    
    all_resets = []
    has_expiring = False
    for expires_at, expires_at_str, time_left in resets_data:
        local_expiry_str = fmt_local_expiry(expires_at_str)
        time_left_str = fmt_time_left(time_left)
        is_expiring = time_left.total_seconds() < DAYS_THRESHOLD * 24 * 60 * 60
        if is_expiring:
            has_expiring = True
            
        all_resets.append({
            "expiry_date": local_expiry_str,
            "time_left_str": time_left_str,
            "is_expiring": is_expiring
        })
        
    if not has_expiring:
        print(f"Nenhum reset expirando em menos de {DAYS_THRESHOLD} dias.")
        return

    print(f"Encontrado(s) {sum(1 for r in all_resets if r['is_expiring'])} reset(s) prestes a expirar. Enviando via {notify_channel}...")
    subject, body, html_body = build_notification(all_resets)

    try:
        if notify_channel == "email":
            send_email(subject, body, html_body)
        else:
            send_telegram(build_telegram_notification(all_resets))
        print("Notificação enviada com sucesso!")
    except Exception as e:
        print(f"Erro ao enviar a notificação: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
