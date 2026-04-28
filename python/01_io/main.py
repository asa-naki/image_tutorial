"""01_io: 画像の入出力と表示
Usage (CLI): python main.py [input_image] [output_path]
Usage (import): from main import run; pairs = run(img_path)
"""
import argparse
import sys
from pathlib import Path

import cv2

sys.path.insert(0, str(Path(__file__).parent.parent))
from utils import DATA_DIR, load_image, show


def run(in_path: str | Path, out_path: str | Path | None = None):
    in_path = Path(in_path)

    # カラー (BGR) として読み込み
    color = load_image(in_path, cv2.IMREAD_COLOR)
    # グレースケールとして読み込み
    gray = load_image(in_path, cv2.IMREAD_GRAYSCALE)
    # アルファチャネル付き (なければ通常BGRと同じ)
    bgra = load_image(in_path, cv2.IMREAD_UNCHANGED)

    print(f"size  : {color.shape[1]} x {color.shape[0]}")
    print(f"chans : {color.shape[2] if color.ndim == 3 else 1}")
    print(f"dtype : {color.dtype}")

    # PNG として保存
    if out_path is not None:
        out_path = Path(out_path)
        cv2.imwrite(str(out_path), color)
        print(f"saved : {out_path}")

    pairs = [("color (BGR)", color), ("gray", gray), ("bgra/unchanged", bgra)]
    return pairs


def main():
    parser = argparse.ArgumentParser(description="01_io: 画像入出力と表示")
    parser.add_argument("input", nargs="?", default=str(DATA_DIR / "lena.png"))
    parser.add_argument("output", nargs="?", default="01_io_out.png")
    parser.add_argument("--no-show", action="store_true", help="ウィンドウ表示しない")
    args = parser.parse_args()

    pairs = run(args.input, args.output)
    if not args.no_show:
        show(pairs)


if __name__ == "__main__":
    main()
