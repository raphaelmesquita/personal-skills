#!/usr/bin/env python3
import json
import urllib.request
import os
import sys
import smtplib
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
TIMEZONE = "America/Sao_Paulo"


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


def main():
    if not load_env():
        print("Aviso: Nenhum arquivo .env encontrado. Usando variáveis de ambiente do sistema.")

    required_vars = ['SMTP_HOST', 'SMTP_PORT', 'SMTP_USER', 'SMTP_PASSWORD', 'EMAIL_FROM', 'EMAIL_TO']
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
    expiring_resets = []

    for c in credits:
        expires_at_str = c.get("expires_at")
        if not expires_at_str:
            continue
        
        expires_at = datetime.fromisoformat(expires_at_str.replace("Z", "+00:00"))
        time_left = expires_at - now

        # We only care about resets expiring in less than 10 days, but not already expired
        if 0 <= time_left.total_seconds() < 10 * 24 * 60 * 60:
            local_tz = ZoneInfo(TIMEZONE)
            local_expiry = expires_at.astimezone(local_tz)
            local_expiry_str = local_expiry.strftime("%d/%m/%Y às %H:%M:%S")
            expiring_resets.append((local_expiry_str, fmt_time_left(time_left)))

    if not expiring_resets:
        print("Nenhum reset expirando em menos de 10 dias.")
        return

    # Build and send email
    print(f"Encontrado(s) {len(expiring_resets)} reset(s) prestes a expirar. Enviando e-mail...")
    
    subject = "[ChatGPT Reset] Alerta de Expiração de Limite de Uso"
    body_lines = [
        "Olá,",
        "",
        "Este é um alerta automático informando que há crédito(s) de uso do ChatGPT prestes a expirar nos próximos 10 dias:",
        ""
    ]
    for expiry_date, time_left_str in expiring_resets:
        body_lines.append(f"- Expira em: {expiry_date} (Tempo restante: {time_left_str})")
    
    body_lines.extend([
        "",
        "Por favor, planeje o uso da sua conta adequadamente.",
        "",
        "Atenciosamente,",
        "Script de Alerta de Resets"
    ])
    
    body = "\n".join(body_lines)

    try:
        msg = MIMEMultipart()
        msg['From'] = os.environ['EMAIL_FROM']
        msg['To'] = os.environ['EMAIL_TO']
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain', 'utf-8'))

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
        print("E-mail enviado com sucesso!")
    except Exception as e:
        print(f"Erro ao enviar o e-mail: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
