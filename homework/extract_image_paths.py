"""
Extract paths of large images from the Amazon Berkeley Objects (small) dataset.

Usage:
    uv run python homework/extract_image_paths.py [dataset_dir] [output_file]

<dataset_dir> is the folder where abo-images-small.tar was unpacked (default: homework/data),
i.e. the one that contains `images/metadata/images.csv.gz` and `images/small/`.
"""

import sys
from pathlib import Path

import polars as pl

MIN_SIZE = 1000
DEFAULT_DIR = Path(__file__).parent / "data"


def extract_image_paths(dataset_dir: Path, min_size: int = MIN_SIZE) -> list[Path]:
    """Return paths of existing images with width and height >= min_size."""
    metadata_path = dataset_dir / "images" / "metadata" / "images.csv.gz"
    images_dir = dataset_dir / "images" / "small"

    # columns: image_id, height, width, path (path is relative to images/small)
    paths = (
        pl.read_csv(metadata_path)
        .drop_nulls(["height", "width", "path"])
        .filter((pl.col("width") >= min_size) & (pl.col("height") >= min_size))
        .get_column("path")
        .to_list()
    )

    return [p for p in (images_dir / path for path in paths) if p.is_file()]


def main() -> None:
    dataset_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_DIR
    output_file = Path(sys.argv[2] if len(sys.argv) > 2 else "image_paths.txt")

    image_paths = extract_image_paths(dataset_dir)
    output_file.write_text("\n".join(map(str, image_paths)) + "\n")
    print(f"Saved {len(image_paths)} image paths to {output_file}")


if __name__ == "__main__":
    main()
