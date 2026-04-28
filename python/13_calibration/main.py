"""13_calibration: カメラキャリブレーション
Usage (CLI): python main.py [chessboard_dir] [--cols N] [--rows N] [--square S]
  チェスボード画像が入ったディレクトリを指定。省略時は合成チェスボードで動作確認。

キャリブレーション結果 (camera_matrix.npz) を保存します。
"""
import argparse
import sys
from pathlib import Path

import cv2
import numpy as np

sys.path.insert(0, str(Path(__file__).parent.parent))
from utils import DATA_DIR, show


def generate_synthetic_chessboard(cols: int = 9, rows: int = 6,
                                  square: int = 60, n: int = 10):
    """キャリブレーション用に合成チェスボード画像を生成する。"""
    board_w = cols * square
    board_h = rows * square
    base = np.zeros((board_h + square, board_w + square), dtype=np.uint8)

    for r in range(rows + 1):
        for c in range(cols + 1):
            if (r + c) % 2 == 0:
                y0, y1 = r * square, (r + 1) * square
                x0, x1 = c * square, (c + 1) * square
                base[y0:y1, x0:x1] = 255

    images = []
    rng = np.random.default_rng(42)
    for i in range(n):
        angle = rng.uniform(-15, 15)
        tx = rng.uniform(-20, 20)
        ty = rng.uniform(-20, 20)
        h, w = base.shape
        M = cv2.getRotationMatrix2D((w / 2, h / 2), angle, 0.85)
        M[0, 2] += tx
        M[1, 2] += ty
        warped = cv2.warpAffine(base, M, (w, h), borderValue=128)
        # 軽いノイズ
        noise = rng.integers(0, 10, warped.shape, dtype=np.uint8)
        warped = cv2.add(warped, noise)
        images.append(warped)
    return images


def calibrate(images, cols: int, rows: int, square_m: float = 0.025):
    """チェスボード画像リストからキャリブレーションを実施する。"""
    pattern = (cols, rows)
    objp = np.zeros((cols * rows, 3), np.float32)
    objp[:, :2] = np.mgrid[0:cols, 0:rows].T.reshape(-1, 2) * square_m

    obj_points = []
    img_points = []
    img_shape = None

    for img in images:
        if img.ndim == 3:
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        else:
            gray = img
        img_shape = gray.shape[::-1]
        ret, corners = cv2.findChessboardCorners(gray, pattern, None)
        if ret:
            criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
            corners = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
            obj_points.append(objp)
            img_points.append(corners)

    if len(obj_points) < 3:
        print(f"[warn] コーナー検出成功: {len(obj_points)} 枚 (最低 3 枚必要)")
        return None, None, None

    rms, K, dist, rvecs, tvecs = cv2.calibrateCamera(
        obj_points, img_points, img_shape, None, None)

    print(f"RMS reprojection error: {rms:.4f} px")
    print(f"Camera matrix K:\n{K}")
    print(f"Distortion coeffs: {dist.ravel()}")
    return K, dist, rms


def run(image_dir: str | Path | None = None,
        cols: int = 9, rows: int = 6, square_m: float = 0.025):

    if image_dir is not None:
        image_dir = Path(image_dir)
        paths = sorted(image_dir.glob("*.jpg")) + sorted(image_dir.glob("*.png"))
        images = [cv2.imread(str(p)) for p in paths]
        print(f"読み込み: {len(images)} 枚 ({image_dir})")
    else:
        print("[info] 合成チェスボード画像でデモ実行します")
        images = generate_synthetic_chessboard(cols, rows, square=60, n=10)

    K, dist, rms = calibrate(images, cols, rows, square_m)

    # コーナー描画の可視化 (最初の4枚)
    pairs = []
    pattern = (cols, rows)
    for i, img in enumerate(images[:4]):
        gray = img if img.ndim == 2 else cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        color = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR) if img.ndim == 2 else img.copy()
        ret, corners = cv2.findChessboardCorners(gray, pattern, None)
        if ret:
            cv2.drawChessboardCorners(color, pattern, corners, ret)
        pairs.append((f"corners {i}", color))

    if K is not None and dist is not None:
        # 補正画像 (最初の1枚)
        sample = images[0] if images[0].ndim == 3 else cv2.cvtColor(images[0], cv2.COLOR_GRAY2BGR)
        h, w = sample.shape[:2]
        K_new, roi = cv2.getOptimalNewCameraMatrix(K, dist, (w, h), 1)
        undist = cv2.undistort(sample, K, dist, None, K_new)
        pairs.append(("original", sample))
        pairs.append(("undistorted", undist))

        np.savez("camera_matrix.npz", K=K, dist=dist, rms=rms)
        print("saved: camera_matrix.npz")

    return pairs


def main():
    parser = argparse.ArgumentParser(description="13_calibration: カメラキャリブレーション")
    parser.add_argument("image_dir", nargs="?", default=None,
                        help="チェスボード画像ディレクトリ (省略時: 合成画像)")
    parser.add_argument("--cols", type=int, default=9, help="内側コーナー列数")
    parser.add_argument("--rows", type=int, default=6, help="内側コーナー行数")
    parser.add_argument("--square", type=float, default=0.025, help="正方形サイズ [m]")
    parser.add_argument("--no-show", action="store_true")
    args = parser.parse_args()

    pairs = run(args.image_dir, args.cols, args.rows, args.square)
    if not args.no_show:
        show(pairs, cols=3)


if __name__ == "__main__":
    main()
