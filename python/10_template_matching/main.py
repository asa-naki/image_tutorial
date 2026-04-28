"""10_template_matching: テンプレートマッチング
Usage (CLI): python main.py [input_image] [template_image]
  template_image を省略すると入力画像の中央 1/4 を自動切り出してテンプレートに使う。
"""
import argparse
import sys
from pathlib import Path

import cv2
import numpy as np

sys.path.insert(0, str(Path(__file__).parent.parent))
from utils import DATA_DIR, load_image, show


def run(in_path: str | Path, tmpl_path: str | Path | None = None):
    src = load_image(in_path)
    h, w = src.shape[:2]

    if tmpl_path is not None:
        tmpl = load_image(tmpl_path)
    else:
        # 画像中央 1/4 をテンプレートとして切り出す
        y1, y2 = h // 4, h * 3 // 4
        x1, x2 = w // 4, w * 3 // 4
        tmpl = src[y1:y2, x1:x2].copy()

    th, tw = tmpl.shape[:2]
    gray_src = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
    gray_tmpl = cv2.cvtColor(tmpl, cv2.COLOR_BGR2GRAY)

    methods = [
        ("TM_SQDIFF",        cv2.TM_SQDIFF),
        ("TM_SQDIFF_NORMED", cv2.TM_SQDIFF_NORMED),
        ("TM_CCORR_NORMED",  cv2.TM_CCORR_NORMED),
        ("TM_CCOEFF_NORMED", cv2.TM_CCOEFF_NORMED),
    ]

    pairs = [("src", src), ("template", tmpl)]

    for name, method in methods:
        result = cv2.matchTemplate(gray_src, gray_tmpl, method)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

        # SQDIFF 系は最小値が最良
        if method in (cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED):
            top_left = min_loc
            score = min_val
        else:
            top_left = max_loc
            score = max_val

        bottom_right = (top_left[0] + tw, top_left[1] + th)
        vis = src.copy()
        cv2.rectangle(vis, top_left, bottom_right, (0, 0, 255), 3)
        print(f"{name:22s}: score={score:.4f}, loc={top_left}")
        pairs.append((f"{name}\nscore={score:.3f}", vis))

    return pairs


def main():
    parser = argparse.ArgumentParser(description="10_template_matching")
    parser.add_argument("input", nargs="?", default=str(DATA_DIR / "lena.png"))
    parser.add_argument("template", nargs="?", default=None)
    parser.add_argument("--no-show", action="store_true")
    args = parser.parse_args()

    pairs = run(args.input, args.template)
    if not args.no_show:
        show(pairs, cols=3)


if __name__ == "__main__":
    main()
