"""12_video: 動画・カメラ入力
Usage (CLI):
  動画ファイル : python main.py --video path/to/video.mp4
  カメラ       : python main.py --camera 0
  Notebook     : from main import process_frame; 単フレームで処理確認

注意: Jupyter Notebook でのリアルタイムプレビューは環境依存のため、
      ここではフレームを静止画として取得する関数を提供します。
"""
import argparse
import sys
from pathlib import Path

import cv2
import numpy as np

sys.path.insert(0, str(Path(__file__).parent.parent))
from utils import DATA_DIR, show


def process_frame(frame: np.ndarray):
    """1フレームに処理を施して返す (Notebook からも呼び出せる)。"""
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150)
    edges_bgr = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
    overlay = cv2.addWeighted(frame, 0.7, edges_bgr, 0.3, 0)
    return overlay


def grab_frames(source, n_frames: int = 5):
    """動画 / カメラから最大 n_frames 枚取得して返す。"""
    cap = cv2.VideoCapture(source)
    if not cap.isOpened():
        print(f"[error] 開けません: {source}")
        sys.exit(1)

    total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    print(f"source : {source}")
    print(f"size   : {w}x{h}, fps={fps:.1f}, total={total}")

    frames = []
    step = max(1, total // n_frames) if total > 0 else 1
    for i in range(n_frames):
        if total > 0:
            cap.set(cv2.CAP_PROP_POS_FRAMES, i * step)
        ret, frame = cap.read()
        if not ret:
            break
        frames.append(frame)
    cap.release()
    return frames


def run_cli(source, output_path: str | None = None):
    """CLI 実行: フレームごとに処理してウィンドウ表示 (ESC/q で終了)。"""
    cap = cv2.VideoCapture(source)
    if not cap.isOpened():
        print(f"[error] 開けません: {source}")
        sys.exit(1)

    writer = None
    if output_path:
        fps = cap.get(cv2.CAP_PROP_FPS) or 30
        w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        writer = cv2.VideoWriter(output_path, fourcc, fps, (w, h))

    print("[info] ESC または 'q' で終了")
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        out = process_frame(frame)
        cv2.imshow("12_video", out)
        if writer:
            writer.write(out)
        if cv2.waitKey(1) & 0xFF in (27, ord('q')):
            break

    cap.release()
    if writer:
        writer.release()
        print(f"saved: {output_path}")
    cv2.destroyAllWindows()


def run_notebook(source, n_frames: int = 5):
    """Notebook 用: フレームを取得して処理結果を pairs で返す。"""
    frames = grab_frames(source, n_frames)
    pairs = []
    for i, f in enumerate(frames):
        pairs.append((f"frame {i}", f))
        pairs.append((f"processed {i}", process_frame(f)))
    return pairs


def main():
    parser = argparse.ArgumentParser(description="12_video: 動画・カメラ入力")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--video", default=str(DATA_DIR / "sample.mp4"),
                       help="動画ファイルパス")
    group.add_argument("--camera", type=int, metavar="ID", help="カメラデバイス番号")
    parser.add_argument("--output", default=None, help="処理済み動画の保存先")
    parser.add_argument("--no-show", action="store_true",
                        help="ウィンドウを出さずフレームを Notebook モードで表示")
    args = parser.parse_args()

    source = args.camera if args.camera is not None else args.video

    if args.no_show:
        pairs = run_notebook(source)
        show(pairs, cols=2)
    else:
        run_cli(source, args.output)


if __name__ == "__main__":
    main()
