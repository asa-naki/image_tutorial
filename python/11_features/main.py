"""11_features: 特徴点検出・記述・マッチング (ORB / AKAZE)
Usage (CLI): python main.py [image1] [image2]
  image2 を省略すると image1 を 30° 回転させた画像でマッチングを試みる。
"""
import argparse
import sys
from pathlib import Path

import cv2
import numpy as np

sys.path.insert(0, str(Path(__file__).parent.parent))
from utils import DATA_DIR, load_image, show


def _rotate_image(img: np.ndarray, angle: float = 30.0) -> np.ndarray:
    h, w = img.shape[:2]
    M = cv2.getRotationMatrix2D((w / 2, h / 2), angle, 0.9)
    return cv2.warpAffine(img, M, (w, h))


def _match_and_draw(img1, img2, detector_name: str):
    gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

    if detector_name == "ORB":
        det = cv2.ORB_create(nfeatures=500)
    elif detector_name == "AKAZE":
        det = cv2.AKAZE_create()
    else:
        raise ValueError(f"Unknown detector: {detector_name}")

    kp1, des1 = det.detectAndCompute(gray1, None)
    kp2, des2 = det.detectAndCompute(gray2, None)

    if des1 is None or des2 is None or len(des1) == 0 or len(des2) == 0:
        canvas = np.zeros((max(img1.shape[0], img2.shape[0]),
                           img1.shape[1] + img2.shape[1], 3), dtype=np.uint8)
        cv2.putText(canvas, "no descriptors", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        return canvas, 0

    # ブルートフォースマッチング
    norm = cv2.NORM_HAMMING  # ORB/AKAZE はバイナリ記述子
    bf = cv2.BFMatcher(norm, crossCheck=True)
    matches = bf.match(des1, des2)
    matches = sorted(matches, key=lambda m: m.distance)
    good = matches[:50]

    result = cv2.drawMatches(img1, kp1, img2, kp2, good, None,
                             flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
    print(f"{detector_name}: kp1={len(kp1)}, kp2={len(kp2)}, matches={len(good)}")
    return result, len(good)


def run(img1_path: str | Path, img2_path: str | Path | None = None):
    img1 = load_image(img1_path)
    img2 = load_image(img2_path) if img2_path else _rotate_image(img1)

    # 特徴点のみ可視化
    gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    orb = cv2.ORB_create(nfeatures=500)
    kp_vis = img1.copy()
    kps, _ = orb.detectAndCompute(gray1, None)
    cv2.drawKeypoints(img1, kps, kp_vis,
                      flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

    orb_match, _ = _match_and_draw(img1, img2, "ORB")
    akaze_match, _ = _match_and_draw(img1, img2, "AKAZE")

    pairs = [
        ("img1", img1),
        ("img2 (rotated)" if img2_path is None else "img2", img2),
        ("ORB keypoints", kp_vis),
        ("ORB matches", orb_match),
        ("AKAZE matches", akaze_match),
    ]
    return pairs


def main():
    parser = argparse.ArgumentParser(description="11_features: 特徴点検出・マッチング")
    parser.add_argument("image1", nargs="?", default=str(DATA_DIR / "lena.png"))
    parser.add_argument("image2", nargs="?", default=None)
    parser.add_argument("--no-show", action="store_true")
    args = parser.parse_args()

    pairs = run(args.image1, args.image2)
    if not args.no_show:
        show(pairs, cols=2)


if __name__ == "__main__":
    main()
