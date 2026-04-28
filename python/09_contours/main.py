"""09_contours: 輪郭検出・形状特徴
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

    # 二値化 → 輪郭検出
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    _, binary = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    contours, hierarchy = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # 面積でフィルタ (小さな輪郭を除去)
    min_area = 100
    contours_filtered = [c for c in contours if cv2.contourArea(c) > min_area]

    # 1) 全輪郭描画
    all_contours = src.copy()
    cv2.drawContours(all_contours, contours_filtered, -1, (0, 255, 0), 2)

    # 2) バウンディングボックス / 最小外接円 / 最小外接矩形
    bbox_img = src.copy()
    circle_img = src.copy()
    rect_img = src.copy()

    for c in contours_filtered:
        # バウンディングボックス
        x, y, cw, ch = cv2.boundingRect(c)
        cv2.rectangle(bbox_img, (x, y), (x + cw, y + ch), (255, 0, 0), 2)

        # 最小外接円
        (cx, cy), radius = cv2.minEnclosingCircle(c)
        cv2.circle(circle_img, (int(cx), int(cy)), int(radius), (0, 0, 255), 2)

        # 最小外接矩形 (回転あり)
        rect = cv2.minAreaRect(c)
        box = cv2.boxPoints(rect).astype(int)
        cv2.drawContours(rect_img, [box], 0, (0, 255, 255), 2)

    # 3) 凸包
    hull_img = src.copy()
    for c in contours_filtered:
        hull = cv2.convexHull(c)
        cv2.drawContours(hull_img, [hull], 0, (255, 0, 255), 2)

    # 4) 近似輪郭 (approxPolyDP)
    approx_img = src.copy()
    for c in contours_filtered:
        eps = 0.02 * cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, eps, True)
        cv2.drawContours(approx_img, [approx], 0, (0, 128, 255), 2)

    # 面積・重心を最大輪郭で出力
    if contours_filtered:
        largest = max(contours_filtered, key=cv2.contourArea)
        M = cv2.moments(largest)
        if M["m00"] > 0:
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])
            print(f"最大輪郭 面積={cv2.contourArea(largest):.1f}, 重心=({cx},{cy})")

    print(f"輪郭数 (フィルタ後): {len(contours_filtered)}")

    pairs = [
        ("src", src),
        ("binary", binary),
        ("all contours", all_contours),
        ("bounding box", bbox_img),
        ("min enclosing circle", circle_img),
        ("min area rect", rect_img),
        ("convex hull", hull_img),
        ("approx poly", approx_img),
    ]
    return pairs


def main():
    parser = argparse.ArgumentParser(description="09_contours: 輪郭検出")
    parser.add_argument("input", nargs="?", default=str(DATA_DIR / "lena.png"))
    parser.add_argument("--no-show", action="store_true")
    args = parser.parse_args()

    pairs = run(args.input)
    if not args.no_show:
        show(pairs, cols=4)


if __name__ == "__main__":
    main()
