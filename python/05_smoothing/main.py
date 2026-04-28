"""05_smoothing: 平滑化フィルタ (均一化・ガウシアン・メディアン・バイラテラル)
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
    src = load_image(in_path)

    # ノイズを加えた画像でフィルタ効果を比較
    noise = np.random.randint(0, 50, src.shape, dtype=np.uint8)
    noisy = cv2.add(src, noise)

    # 1) 均一化ブラー (Box filter)
    box = cv2.blur(noisy, (9, 9))

    # 2) ガウシアンブラー
    gauss = cv2.GaussianBlur(noisy, (9, 9), sigmaX=0)

    # 3) メディアンフィルタ (ソルト&ペッパーノイズに強い)
    median = cv2.medianBlur(noisy, 9)

    # 4) バイラテラルフィルタ (エッジ保持平滑化)
    bilateral = cv2.bilateralFilter(noisy, d=9, sigmaColor=75, sigmaSpace=75)

    # 5) カスタムカーネル (シャープネス強調)
    kernel_sharp = np.array([
        [0, -1,  0],
        [-1,  5, -1],
        [0, -1,  0],
    ], dtype=np.float32)
    sharpened = cv2.filter2D(src, -1, kernel_sharp)

    pairs = [
        ("src", src),
        ("noisy (+ random)", noisy),
        ("box blur 9x9", box),
        ("Gaussian blur 9x9", gauss),
        ("median blur 9", median),
        ("bilateral d=9", bilateral),
        ("sharpened", sharpened),
    ]
    return pairs


def main():
    parser = argparse.ArgumentParser(description="05_smoothing: 平滑化フィルタ")
    parser.add_argument("input", nargs="?", default=str(DATA_DIR / "lena.png"))
    parser.add_argument("--no-show", action="store_true")
    args = parser.parse_args()

    pairs = run(args.input)
    if not args.no_show:
        show(pairs, cols=3)


if __name__ == "__main__":
    main()
