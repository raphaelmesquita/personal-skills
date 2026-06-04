from __future__ import annotations

import argparse
from math import sqrt
from pathlib import Path
import re
import unicodedata
import zipfile

try:
    from PIL import Image, ImageDraw
except ImportError as exc:
    requirements_path = Path(__file__).resolve().parents[1] / "requirements.txt"
    raise SystemExit(
        "Missing dependency: Pillow. Install it with:\n"
        f"python -m pip install -r {requirements_path}"
    ) from exc


GRID_SIZE = 3
MASK_SCALE = 4
DEFAULT_INPUT_DIR = Path("input")
DEFAULT_OUTPUT_DIR = Path("output")
SUPPORTED_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp", ".bmp", ".tif", ".tiff"}


def slugify(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", value)
    ascii_value = normalized.encode("ascii", "ignore").decode("ascii")
    slug = re.sub(r"[^a-zA-Z0-9]+", "_", ascii_value).strip("_").lower()
    return slug or "roll20_token"


def validate_source(image: Image.Image, source: Path) -> int:
    width, height = image.size

    if width != height:
        raise ValueError(f"{source} must be square, got {width}x{height}.")

    if width % GRID_SIZE != 0:
        raise ValueError(
            f"{source} dimensions must be divisible by {GRID_SIZE}, got {width}x{height}."
        )

    return width // GRID_SIZE


def make_hex_mask(size: int) -> Image.Image:
    scaled_size = size * MASK_SCALE
    mid = scaled_size / 2
    radius = scaled_size / 2
    x_offset = radius * sqrt(3) / 2
    y_offset = radius / 2
    last = scaled_size - 1

    points = [
        (mid, 0),
        (mid + x_offset, y_offset),
        (mid + x_offset, scaled_size - y_offset),
        (mid, last),
        (mid - x_offset, scaled_size - y_offset),
        (mid - x_offset, y_offset),
    ]

    mask = Image.new("L", (scaled_size, scaled_size), 0)
    draw = ImageDraw.Draw(mask)
    draw.polygon(points, fill=255)
    return mask.resize((size, size), Image.Resampling.LANCZOS)


def apply_mask(token: Image.Image, mask: Image.Image) -> Image.Image:
    output = token.convert("RGBA")
    output.putalpha(mask)
    return output


def token_sources(input_dir: Path) -> list[Path]:
    if not input_dir.exists():
        input_dir.mkdir(parents=True)
        return []

    return sorted(
        path
        for path in input_dir.iterdir()
        if path.is_file() and path.suffix.lower() in SUPPORTED_EXTENSIONS
    )


def extract_tokens(source: Path, output_dir: Path, slug: str | None = None) -> list[Path]:
    with Image.open(source) as image:
        cell_size = validate_source(image, source)
        mask = make_hex_mask(cell_size)
        output_dir.mkdir(parents=True, exist_ok=True)
        file_slug = slugify(slug or source.stem)

        written: list[Path] = []
        token_number = 1

        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                left = col * cell_size
                upper = row * cell_size
                box = (left, upper, left + cell_size, upper + cell_size)

                token = image.crop(box)
                token = apply_mask(token, mask)

                output_path = output_dir / f"{file_slug}_{token_number:02d}.png"
                token.save(output_path)
                written.append(output_path)
                token_number += 1

        return written


def write_zip(token_paths: list[Path], output_dir: Path, slug: str) -> Path:
    zip_path = output_dir / f"{slugify(slug)}_tokens.zip"
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for token_path in token_paths:
            archive.write(token_path, arcname=token_path.name)
    return zip_path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Extract Roll20-ready hex tokens from 3x3 square token grid images."
    )
    parser.add_argument(
        "source",
        nargs="?",
        type=Path,
        help="Optional single image to extract. Defaults to every image in --input-dir.",
    )
    parser.add_argument(
        "-i",
        "--input-dir",
        type=Path,
        default=DEFAULT_INPUT_DIR,
        help=f"Directory scanned when source is omitted. Defaults to {DEFAULT_INPUT_DIR}.",
    )
    parser.add_argument(
        "-o",
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help=f"Directory for extracted tokens. Defaults to {DEFAULT_OUTPUT_DIR}.",
    )
    parser.add_argument(
        "--slug",
        help=(
            "Base name for output files, usually derived from the requested character "
            "type, faction, or concept."
        ),
    )
    parser.add_argument(
        "--zip",
        action="store_true",
        help="Also create a ZIP file containing the extracted PNG tokens.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    if args.source:
        if not args.source.is_file():
            raise FileNotFoundError(f"Source image not found: {args.source}")

        if args.source.suffix.lower() not in SUPPORTED_EXTENSIONS:
            supported = ", ".join(sorted(SUPPORTED_EXTENSIONS))
            raise ValueError(f"Unsupported image extension for {args.source}. Use: {supported}")

        sources = [args.source]
    else:
        sources = token_sources(args.input_dir)

    if not sources:
        print(f"No supported image files found in {args.input_dir}.")
        return

    written: list[Path] = []

    for source in sources:
        print(f"Processing {source}...")
        source_slug = args.slug or source.stem
        source_written = extract_tokens(source, args.output_dir, source_slug)
        written.extend(source_written)

        if args.zip:
            zip_path = write_zip(source_written, args.output_dir, source_slug)
            print(zip_path)

    for path in written:
        print(path)


if __name__ == "__main__":
    main()
