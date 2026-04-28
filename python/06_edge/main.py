"""06_edge: エッジ検出 (Sobel / Laplacian / Canny / Scharr)
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
    gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)

    # 前処理: ガウシアンブラーでノイズ軽減
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # 1) Sobel (X方向・Y方向・合成)
    sobelx = cv2.Sobel(blurred, cv2.CV_64F, 1, 0, ksize=3)
    sobely = cv2.Sobel(blurred, cv2.CV_64F, 0, 1, ksize=3)
    sobel_mag = cv2.magnitude(sobelx, sobely)
    sobel_mag = np.clip(sobel_mag, 0, 255).astype(np.uint8)
    sobelx_u8 = cv2.convertScaleAbs(sobelx)
    sobely_u8 = cv2.convertScaleAbs(sobely)

    # 2) Scharr (Sobel より精度高い)
    scharrx = cv2.Scharr(blurred, cv2.CV_64F, 1, 0)
    scharry = cv2.Scharr(blurred, cv2.CV_64F, 0, 1)
    scharr_mag = cv2.magnitude(scharrx, scharry)
    scharr_mag = np.clip(scharr_mag, 0, 255).astype(np.uint8)

    # 3) Laplacian
    lap = cv2.Laplacian(blurred, cv2.CV_64F, ksize=3)
    lap_u8 = cv2.convertScaleAbs(lap)

    # 4) Canny (ヒステリシス閾値)
    canny_lo = cv2.Canny(blurred, 50, 150)
    canny_hi = cv2.Canny(blurred, 100, 200)

    pairs = [
        ("gray", gray),
        ("Sobel X", sobelx_u8),
        ("Sobel Y", sobely_u8),
        ("Sobel magnitude", sobel_mag),
        ("Scharr magnitude", scharr_mag),
        ("Laplacian", lap_u8),
        ("Canny (50,150)", canny_lo),
        ("Canny (100,200)", canny_hi),
    ]
    return pairs


def main():
    parser = argparse.ArgumentParser(description="06_edge: エッジ検出")
    parser.add_argument("input", nargs="?", default=str(DATA_DIR / "lena.png"))
    parser.add_argument("--no-show", action="store_true")
    args = parser.parse_args()

    pairs = run(args.input)
    if not args.no_show:
        show(pairs, cols=4)


if __name__ == "__main__":
    main()
