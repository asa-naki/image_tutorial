"""03_geometry: 幾何変換 (resize / rotate / affine / perspective)
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
    h, w = src.shape[:2]

    # 1) リサイズ (半分 / 2倍)
    half = cv2.resize(src, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
    double = cv2.resize(src, None, fx=2.0, fy=2.0, interpolation=cv2.INTER_LINEAR)

    # 2) 回転 (中心 30°, スケール 1.0)
    center = (w / 2, h / 2)
    M_rot = cv2.getRotationMatrix2D(center, 30.0, 1.0)
    rotated = cv2.warpAffine(src, M_rot, (w, h))

    # 3) アフィン変換 (3点対応)
    src_pts = np.float32([[0, 0], [w - 1, 0], [0, h - 1]])
    dst_pts = np.float32([
        [w * 0.1, h * 0.2],
        [w * 0.9, h * 0.1],
        [w * 0.2, h * 0.9],
    ])
    M_aff = cv2.getAffineTransform(src_pts, dst_pts)
    affined = cv2.warpAffine(src, M_aff, (w, h))

    # 4) パースペクティブ変換 (せん断 + スケール)
    H = np.array([
        [1.0, 0.2, 0.0],
        [0.1, 1.0, 0.0],
        [0.0, 0.0, 1.0],
    ], dtype=np.float64)
    warped = cv2.warpPerspective(src, H, (w, h))

    # 5) 反転 (左右・上下・両方)
    flip_h = cv2.flip(src, 1)   # 左右
    flip_v = cv2.flip(src, 0)   # 上下

    print(f"元サイズ : {w} x {h}")
    print(f"半分     : {half.shape[1]} x {half.shape[0]}")
    print(f"ホモグラフィ H:\n{H}")

    pairs = [
        ("src", src),
        ("resize x0.5", half),
        ("rotate 30°", rotated),
        ("affine (3pt)", affined),
        ("perspective (shear)", warped),
        ("flip horizontal", flip_h),
        ("flip vertical", flip_v),
    ]
    return pairs


def main():
    parser = argparse.ArgumentParser(description="03_geometry: 幾何変換")
    parser.add_argument("input", nargs="?", default=str(DATA_DIR / "lena.png"))
    parser.add_argument("--no-show", action="store_true")
    args = parser.parse_args()

    pairs = run(args.input)
    if not args.no_show:
        show(pairs, cols=3)


if __name__ == "__main__":
    main()
