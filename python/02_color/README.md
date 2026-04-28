# 02_color — 色空間変換

> はじめての方は [GUIDE.md](GUIDE.md) (やさしい解説) もどうぞ。

## 目的

- `cv2.cvtColor` で BGR ↔ Gray / HSV / Lab の変換を行う。
- `cv2.split` でチャネルを分離し、各チャネル画像を表示する。
- HSV 空間で色閾値を組み、特定色 (赤) のマスクを作る。

## ポイント

- OpenCV の HSV: H ∈ [0, 180), S, V ∈ [0, 255]。
- 赤色は色相環の **0 付近と 180 付近にまたがる** ため、2 範囲を OR で合成する。
- `cv2.inRange` は条件を満たすマスを 255、外を 0 にしたマスク画像を返す。
- チャネル分離は `cv2.split` でも NumPy スライス `img[:,:,0]` でも可。

## 実行

# Linux / Ubuntu
```bash
python3 main.py ../data/lena.png
python3 main.py ../data/lena.png --no-show
```

# Windows / macOS
```bash
python main.py ../data/lena.png
python main.py ../data/lena.png --no-show
```

## 期待される出力

BGR / gray / HSV / Lab / B / G / R / 赤マスク / 赤抽出 の各画像が表示される。

## 参考

- [OpenCV: Color conversions](https://docs.opencv.org/4.x/de/d25/imgproc_color_conversions.html)
- [OpenCV tutorial: Changing Colorspaces](https://docs.opencv.org/4.x/df/d9d/tutorial_py_colorspaces.html)
