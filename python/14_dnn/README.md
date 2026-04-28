# 14_dnn — DNN 推論

> はじめての方は [GUIDE.md](GUIDE.md) (やさしい解説) もどうぞ。

## 目的

- `cv2.dnn.readNetFromONNX` で YOLOv8n を読み込む。
- `cv2.dnn.blobFromImage` で前処理 (リサイズ / 正規化 / BGR→RGB 変換) を行う。
- `net.forward()` で推論し、NumPy で後処理 (NMS / スコアフィルタ / 座標変換) を行う。

## ポイント

- `blobFromImage` の返り値は `shape = (1, 3, H, W)` の `float32` 配列 (**NCHW 順**)。
- YOLOv8 の出力は `shape = (1, 84, 8400)` → 転置して `(8400, 84)` にすると扱いやすい。
- `cv2.dnn.NMSBoxes` で重複検出を除去する。
- モデルがない場合はエッジ検出デモにフォールバックする。

## モデルの準備

```bash
pip install ultralytics
yolo export model=yolov8n.pt format=onnx
mkdir -p 14_dnn/models
mv yolov8n.onnx 14_dnn/models/
```

## 実行

# Linux / Ubuntu
```bash
# モデルあり (物体検出)
python3 main.py ../data/lena.png
# モデルパスを明示
python3 main.py ../data/lena.png --model 14_dnn/models/yolov8n.onnx
# 信頼度閾値を変更
python3 main.py ../data/lena.png --conf 0.3
# ウィンドウなし
python3 main.py ../data/lena.png --no-show
```

# Windows / macOS
```bash
# モデルあり (物体検出)
python main.py ../data/lena.png
# モデルパスを明示
python main.py ../data/lena.png --model 14_dnn/models/yolov8n.onnx
# 信頼度閾値を変更
python main.py ../data/lena.png --conf 0.3
# ウィンドウなし
python main.py ../data/lena.png --no-show
```

## 期待される出力

- モデルあり: src と検出結果 (バウンディングボックス + ラベル + スコア) を表示。標準出力にクラス名・スコア・座標。
- モデルなし: src とエッジ検出デモ画像を表示。モデルの取得案内を出力。

## 参考

- [OpenCV: DNN module](https://docs.opencv.org/4.x/d2/d58/tutorial_table_of_content_dnn.html)
- [Ultralytics YOLOv8](https://docs.ultralytics.com/modes/export/)
