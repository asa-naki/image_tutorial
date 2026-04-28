"""04_threshold: 固定閾値 / Otsu / Adaptive
Usage (CLI): python main.py [input_image]
"""
import argparse
import sys
from pathlib import Path

import cv2

sys.path.insert(0, str(Path(__file__).parent.parent))
from utils import DATA_DIR, load_image, show


def run(in_path: str | Path):
    gray = load_image(in_path, cv2.IMREAD_GRAYSCALE)

    # 1) 固定閾値 (127)
    _, fixed_bin = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
    _, fixed_inv = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV)

    # 2) Otsu 自動閾値
    otsu_thr, otsu_bin = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

    # 3) Triangle 法
    tri_thr, tri_bin = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_TRIANGLE)

    # 4) Adaptive (Mean / Gaussian) - ブロックサイズ 31, 定数 5
    adapt_mean = cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 31, 5)
    adapt_gauss = cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 5)

    print(f"Otsu 閾値     = {otsu_thr:.1f}")
    print(f"Triangle 閾値 = {tri_thr:.1f}")

    pairs = [
        ("gray", gray),
        ("fixed thr=127", fixed_bin),
        ("fixed inv thr=127", fixed_inv),
        ("Otsu", otsu_bin),
        ("Triangle", tri_bin),
        ("adaptive mean", adapt_mean),
        ("adaptive Gaussian", adapt_gauss),
    ]
    return pairs


def main():
    parser = argparse.ArgumentParser(description="04_threshold: 閾値処理・二値化")
    parser.add_argument("input", nargs="?", default=str(DATA_DIR / "lena.png"))
    parser.add_argument("--no-show", action="store_true")
    args = parser.parse_args()

    pairs = run(args.input)
    if not args.no_show:
        show(pairs, cols=3)


if __name__ == "__main__":
    main()
