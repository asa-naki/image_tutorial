# 14_dnn — DNN 推論 (ONNX)

> はじめての方は [GUIDE.md](GUIDE.md) (中学生向けやさしい解説) もどうぞ。

## 目的

- `cv::dnn::readNetFromONNX` で ONNX モデルを読み込み、CPU 上で推論する。
- 1) 画像分類 (例: MobileNetV2) と 2) 物体検出 (例: YOLOv5/YOLOv8) の 2 サブサンプル。

## モデル取得 (任意)

### 分類: MobileNetV2 (ImageNet 1000 クラス)

```bash
cd image_tutorial/data
# ONNX Model Zoo から
curl -L -o mobilenetv2.onnx \
    https://github.com/onnx/models/raw/main/vision/classification/mobilenet/model/mobilenetv2-12.onnx

# ImageNet ラベル (1行1クラス)
curl -L -o imagenet_labels.txt \
    https://raw.githubusercontent.com/onnx/models/main/vision/classification/synset.txt
```

### 検出: YOLOv5s ONNX

PyTorch の YOLOv5 リポジトリで `python export.py --weights yolov5s.pt --include onnx` でエクスポートしたモデルを `data/yolov5s.onnx` に置きます。COCO ラベル (`coco.names`, 80 クラス) も用意します。

YOLOv8 の ONNX (Ultralytics で `yolo export model=yolov8n.pt format=onnx`) も同じ実装でハンドリングできます (出力 shape を自動判別)。

## ビルド・実行

```bash
cmake --build build -j 14_dnn

# 分類
./build/14_dnn/14_dnn_classify \
    ../data/mobilenetv2.onnx \
    ../data/imagenet_labels.txt \
    ../data/lena.png

# 検出
./build/14_dnn/14_dnn_detect \
    ../data/yolov5s.onnx \
    ../data/coco.names \
    ../data/scene.png \
    0.25 0.45
```

## 期待される出力

- 分類: 標準出力に Top-5 (確率, ラベル)。ウィンドウに最上位ラベルを描画。
- 検出: 標準出力に NMS 後の検出数。ウィンドウに矩形 + ラベル + 信頼度。

## 注意

- モデル未取得時は分かりやすいエラーメッセージで終了します。
- ImageNet/COCO の前処理パラメータはモデルにより異なるため、別モデルを使う場合は `mean`, `std`, 入力解像度などを調整してください。

## 参考

- [OpenCV: Deep Neural Networks](https://docs.opencv.org/4.x/d6/d0f/group__dnn.html)
- [ONNX Model Zoo](https://github.com/onnx/models)
- [Ultralytics YOLOv8 export](https://docs.ultralytics.com/modes/export/)
