"""02_color: 色空間変換とチャネル分離・HSV による色抽出
Usage (CLI): python main.py [input_image]
"""
import argparse
import sys
from pathlib import Path

import cv2
import numpy as np

sys.path.insert(0, str(Path(__file__).parent.parent))
from utils import DATA_DIR, load_image, show


def run(in_path: str | Path):
    bgr = load_image(in_path)

    # 1) BGR -> Gray
    gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)

    # 2) BGR -> HSV
    hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)

    # 3) BGR -> Lab
    lab = cv2.cvtColor(bgr, cv2.COLOR_BGR2Lab)

    # 4) チャネル分離 (BGR)
    b, g, r = cv2.split(bgr)

    # 5) HSV 閾値による赤色抽出 (H=0付近 + H=180付近)
    mask1 = cv2.inRange(hsv, (0, 80, 80), (10, 255, 255))
    mask2 = cv2.inRange(hsv, (170, 80, 80), (180, 255, 255))
    red_mask = mask1 | mask2
    red_only = cv2.bitwise_and(bgr, bgr, mask=red_mask)

    print(f"BGR mean : {cv2.mean(bgr)[:3]}")
    print(f"Gray mean: {cv2.mean(gray)[0]:.1f}")

    pairs = [
        ("bgr", bgr),
        ("gray", gray),
        ("hsv (visualized)", hsv),
        ("Lab (visualized)", lab),
        ("B channel", b),
        ("G channel", g),
        ("R channel", r),
        ("red mask", red_mask),
        ("red only", red_only),
    ]
    return pairs


def main():
    parser = argparse.ArgumentParser(description="02_color: 色空間変換")
    parser.add_argument("input", nargs="?", default=str(DATA_DIR / "lena.png"))
    parser.add_argument("--no-show", action="store_true")
    args = parser.parse_args()

    pairs = run(args.input)
    if not args.no_show:
        show(pairs, cols=3)


if __name__ == "__main__":
    main()
