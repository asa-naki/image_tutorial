"""08_histogram: ヒストグラム計算・均一化・CLAHE
Usage (CLI): python main.py [input_image]
"""
import argparse
import sys
from pathlib import Path

import cv2
import numpy as np

sys.path.insert(0, str(Path(__file__).parent.parent))
from utils import DATA_DIR, load_image, show


def _draw_hist(gray: np.ndarray, title: str = "") -> np.ndarray:
    """1チャネル画像のヒストグラムを可視化した BGR 画像を返す。"""
    hist = cv2.calcHist([gray], [0], None, [256], [0, 256])
    h, w = 200, 256
    canvas = np.zeros((h, w, 3), dtype=np.uint8)
    max_val = hist.max()
    for i, v in enumerate(hist.flatten()):
        bar_h = int(v / max_val * h)
        cv2.line(canvas, (i, h), (i, h - bar_h), (200, 200, 200))
    return canvas


def run(in_path: str | Path):
    src = load_image(in_path)
    gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)

    # 1) ヒストグラム可視化
    hist_img = _draw_hist(gray, "hist")

    # 2) グローバル均一化 (equalizeHist)
    eq = cv2.equalizeHist(gray)
    hist_eq = _draw_hist(eq, "hist eq")

    # 3) CLAHE (Contrast Limited Adaptive HE)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    clahe_img = clahe.apply(gray)
    hist_clahe = _draw_hist(clahe_img, "hist CLAHE")

    # 4) カラー CLAHE (各チャネルに適用)
    lab = cv2.cvtColor(src, cv2.COLOR_BGR2Lab)
    l, a, b_ch = cv2.split(lab)
    l_clahe = clahe.apply(l)
    lab_clahe = cv2.merge([l_clahe, a, b_ch])
    color_clahe = cv2.cvtColor(lab_clahe, cv2.COLOR_Lab2BGR)

    print(f"gray  mean={gray.mean():.1f} std={gray.std():.1f}")
    print(f"eq    mean={eq.mean():.1f} std={eq.std():.1f}")
    print(f"clahe mean={clahe_img.mean():.1f} std={clahe_img.std():.1f}")

    pairs = [
        ("gray", gray),
        ("hist", hist_img),
        ("equalizeHist", eq),
        ("hist (eq)", hist_eq),
        ("CLAHE", clahe_img),
        ("hist (CLAHE)", hist_clahe),
        ("color CLAHE (Lab)", color_clahe),
    ]
    return pairs


def main():
    parser = argparse.ArgumentParser(description="08_histogram: ヒストグラム")
    parser.add_argument("input", nargs="?", default=str(DATA_DIR / "lena.png"))
    parser.add_argument("--no-show", action="store_true")
    args = parser.parse_args()

    pairs = run(args.input)
    if not args.no_show:
        show(pairs, cols=3)


if __name__ == "__main__":
    main()
