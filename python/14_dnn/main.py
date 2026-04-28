"""14_dnn: DNN 推論 (OpenCV dnn モジュール)
Usage (CLI): python main.py [input_image] [--model MODEL] [--classes CLASSES]
  デフォルトはダウンロード済みの MobileNet-SSD (COCO) を使用。
  モデルがなければダウンロード方法を案内します。

対応フォーマット: ONNX / Caffe / TensorFlow (OpenCV dnn.readNet で自動判定)
"""
import argparse
import sys
from pathlib import Path

import cv2
import numpy as np

sys.path.insert(0, str(Path(__file__).parent.parent))
from utils import DATA_DIR, load_image, show

MODEL_DIR = Path(__file__).parent / "models"

# YOLOv8n ONNX (軽量) のデフォルトパス
DEFAULT_MODEL = MODEL_DIR / "yolov8n.onnx"

COCO_CLASSES = [
    "person", "bicycle", "car", "motorcycle", "airplane", "bus", "train",
    "truck", "boat", "traffic light", "fire hydrant", "stop sign",
    "parking meter", "bench", "bird", "cat", "dog", "horse", "sheep",
    "cow", "elephant", "bear", "zebra", "giraffe", "backpack", "umbrella",
    "handbag", "tie", "suitcase", "frisbee", "skis", "snowboard",
    "sports ball", "kite", "baseball bat", "baseball glove", "skateboard",
    "surfboard", "tennis racket", "bottle", "wine glass", "cup", "fork",
    "knife", "spoon", "bowl", "banana", "apple", "sandwich", "orange",
    "broccoli", "carrot", "hot dog", "pizza", "donut", "cake", "chair",
    "couch", "potted plant", "bed", "dining table", "toilet", "tv",
    "laptop", "mouse", "remote", "keyboard", "cell phone", "microwave",
    "oven", "toaster", "sink", "refrigerator", "book", "clock", "vase",
    "scissors", "teddy bear", "hair drier", "toothbrush",
]


def run_yolov8(src: np.ndarray, model_path: Path,
               conf_thr: float = 0.4, iou_thr: float = 0.5):
    """YOLOv8 ONNX モデルで推論して検出結果を描画した画像を返す。"""
    h, w = src.shape[:2]
    inp_size = 640

    # 前処理: letterbox → 正規化
    scale = min(inp_size / w, inp_size / h)
    nw, nh = int(w * scale), int(h * scale)
    resized = cv2.resize(src, (nw, nh))
    padded = np.full((inp_size, inp_size, 3), 114, dtype=np.uint8)
    padded[:nh, :nw] = resized
    blob = cv2.dnn.blobFromImage(padded, 1 / 255.0, (inp_size, inp_size),
                                 swapRB=True, crop=False)

    net = cv2.dnn.readNetFromONNX(str(model_path))
    net.setInput(blob)
    outputs = net.forward()  # shape: (1, 84, 8400)

    # 後処理
    out = outputs[0].T  # (8400, 84)
    boxes, scores, class_ids = [], [], []
    for row in out:
        cls_scores = row[4:]
        cls_id = int(np.argmax(cls_scores))
        conf = float(cls_scores[cls_id])
        if conf < conf_thr:
            continue
        cx, cy, bw, bh = row[:4]
        # undo letterbox
        x1 = (cx - bw / 2 - 0) / scale
        y1 = (cy - bh / 2 - 0) / scale
        x2 = (cx + bw / 2 - 0) / scale
        y2 = (cy + bh / 2 - 0) / scale
        boxes.append([int(x1), int(y1), int(x2 - x1), int(y2 - y1)])
        scores.append(conf)
        class_ids.append(cls_id)

    indices = cv2.dnn.NMSBoxes(boxes, scores, conf_thr, iou_thr)
    result = src.copy()
    rng = np.random.default_rng(0)
    colors = {i: tuple(rng.integers(80, 255, 3).tolist()) for i in range(80)}

    for idx in (indices.flatten() if len(indices) > 0 else []):
        x, y, bw, bh = boxes[idx]
        cls_id = class_ids[idx]
        label = COCO_CLASSES[cls_id] if cls_id < len(COCO_CLASSES) else str(cls_id)
        color = colors[cls_id]
        cv2.rectangle(result, (x, y), (x + bw, y + bh), color, 2)
        cv2.putText(result, f"{label} {scores[idx]:.2f}",
                    (x, max(y - 6, 10)), cv2.FONT_HERSHEY_SIMPLEX, 0.55, color, 2)
        print(f"  {label}: {scores[idx]:.3f} @ [{x},{y},{x+bw},{y+bh}]")

    return result


def run_demo_edge(src: np.ndarray):
    """モデルなし動作確認用: OpenCV の組み込み structured-edge を使う代替デモ。"""
    gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150)
    edges_bgr = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
    return edges_bgr


def run(in_path: str | Path, model_path: str | Path | None = None,
        conf: float = 0.4):
    src = load_image(in_path)

    if model_path is None:
        model_path = DEFAULT_MODEL

    model_path = Path(model_path)
    if not model_path.exists():
        print(f"[warn] モデルが見つかりません: {model_path}")
        print("       YOLOv8n ONNX を取得するには:")
        print("         pip install ultralytics")
        print("         yolo export model=yolov8n.pt format=onnx")
        print("         mv yolov8n.onnx python/14_dnn/models/")
        print("       代わりにエッジ検出デモを表示します。")
        fallback = run_demo_edge(src)
        return [("src", src), ("edge demo (no model)", fallback)]

    print(f"モデル: {model_path}")
    result = run_yolov8(src, model_path, conf_thr=conf)
    return [("src", src), ("detection result", result)]


def main():
    parser = argparse.ArgumentParser(description="14_dnn: DNN 推論")
    parser.add_argument("input", nargs="?", default=str(DATA_DIR / "lena.png"))
    parser.add_argument("--model", default=None, help="ONNX モデルパス")
    parser.add_argument("--conf", type=float, default=0.4, help="信頼度閾値")
    parser.add_argument("--no-show", action="store_true")
    args = parser.parse_args()

    pairs = run(args.input, args.model, args.conf)
    if not args.no_show:
        show(pairs, cols=2)


if __name__ == "__main__":
    main()
