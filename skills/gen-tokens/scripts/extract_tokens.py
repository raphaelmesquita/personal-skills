from __future__ import annotations

import argparse
from math import sqrt
from pathlib import Path

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


def extract_tokens(source: Path, output_dir: Path) -> list[Path]:
    with Image.open(source) as image:
        cell_size = validate_source(image, source)
        mask = make_hex_mask(cell_size)
        output_dir.mkdir(parents=True, exist_ok=True)

        written: list[Path] = []
        token_number = 1

        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                left = col * cell_size
                upper = row * cell_size
                box = (left, upper, left + cell_size, upper + cell_size)

                token = image.crop(box)
                token = apply_mask(token, mask)

                output_path = output_dir / f"{source.stem}_token_{token_number}.png"
                token.save(output_path)
                written.append(output_path)
                token_number += 1

        return written


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
        written.extend(extract_tokens(source, args.output_dir))

    for path in written:
        print(path)


if __name__ == "__main__":
    main()
