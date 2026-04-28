# 02_color — 色空間変換

> はじめての方は [GUIDE.md](GUIDE.md) (中学生向けやさしい解説) もどうぞ。

## 目的

- `cv::cvtColor` で BGR ↔ Gray ↔ HSV の変換を行う。
- `cv::split` でチャネル分離し、各チャネル画像を表示する。
- HSV 空間で色閾値を組み、特定色 (赤) のマスクを作る。

## ポイント

- OpenCV では H ∈ [0, 180), S, V ∈ [0, 255]。
- 赤色は色相環の 0 付近と 180 付近にまたがるため、2 範囲を OR する。
- `cv::inRange(src, lo, hi, dst)` は範囲内なら 255、外は 0 のマスクを返す。

## ビルド・実行

```bash
cd image_tutorial/cpp
cmake --build build -j 02_color
./build/02_color/02_color ../data/lena.png
```

## 期待される出力

- BGR / Gray / HSV / B / G / R / 赤マスク / 赤抽出 の 8 ウィンドウ。

## 参考

- [OpenCV: Color conversions](https://docs.opencv.org/4.x/de/d25/imgproc_color_conversions.html)
