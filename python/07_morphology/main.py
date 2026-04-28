"""07_morphology: モルフォロジー演算
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
    src = load_image(in_path, cv2.IMREAD_GRAYSCALE)

    # Otsu で二値化
    _, binary = cv2.threshold(src, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

    # 構造要素
    kernel3 = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    kernel7 = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7))
    kernel_ellipse = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 9))

    # 1) 収縮 (erosion)
    eroded = cv2.erode(binary, kernel3, iterations=2)

    # 2) 膨張 (dilation)
    dilated = cv2.dilate(binary, kernel3, iterations=2)

    # 3) オープニング (erosion → dilation: 細い突起除去)
    opened = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel7)

    # 4) クロージング (dilation → erosion: 小さな穴を埋める)
    closed = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel7)

    # 5) モルフォロジー勾配 (輪郭抽出)
    gradient = cv2.morphologyEx(binary, cv2.MORPH_GRADIENT, kernel3)

    # 6) Top Hat (元画像 - opening: 明るい小物体の抽出)
    tophat = cv2.morphologyEx(src, cv2.MORPH_TOPHAT, kernel_ellipse)

    # 7) Black Hat (closing - 元画像: 暗い小物体の抽出)
    blackhat = cv2.morphologyEx(src, cv2.MORPH_BLACKHAT, kernel_ellipse)

    pairs = [
        ("src (gray)", src),
        ("binary (Otsu)", binary),
        ("erode x2", eroded),
        ("dilate x2", dilated),
        ("opening 7x7", opened),
        ("closing 7x7", closed),
        ("gradient 3x3", gradient),
        ("top hat", tophat),
        ("black hat", blackhat),
    ]
    return pairs


def main():
    parser = argparse.ArgumentParser(description="07_morphology: モルフォロジー演算")
    parser.add_argument("input", nargs="?", default=str(DATA_DIR / "lena.png"))
    parser.add_argument("--no-show", action="store_true")
    args = parser.parse_args()

    pairs = run(args.input)
    if not args.no_show:
        show(pairs, cols=3)


if __name__ == "__main__":
    main()
