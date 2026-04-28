# 08_histogram — ヒストグラム

> はじめての方は [GUIDE.md](GUIDE.md) (中学生向けやさしい解説) もどうぞ。

## 目的

- `cv::calcHist` でヒストグラムを計算し可視化する。
- 全体平坦化 (`cv::equalizeHist`) と適応的平坦化 (CLAHE) を比較する。

## ポイント

- グローバル平坦化は累積分布関数を変換に使う。コントラストは上がるが過剰に強調されることもある。
- CLAHE (Contrast Limited Adaptive Histogram Equalization) は局所窓ごとに平坦化し、`clipLimit` でヒストグラムを上限制限。陰影の強い画像で有効。

## ビルド・実行

```bash
cmake --build build -j 08_histogram
./build/08_histogram/08_histogram ../data/lena.png
```

## 期待される出力

- 元画像とそのヒストグラム / 平坦化後 / CLAHE の 6 ウィンドウ。

## 参考

- [OpenCV: Histograms](https://docs.opencv.org/4.x/de/db2/tutorial_py_table_of_contents_histograms.html)
