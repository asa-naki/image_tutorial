# 06_edge — エッジ検出

> はじめての方は [GUIDE.md](GUIDE.md) (中学生向けやさしい解説) もどうぞ。

## 目的

- 一次微分 (Sobel) と二次微分 (Laplacian)、そして実用的な Canny を比較する。

## ポイント

- Sobel は水平 $G_x$ と垂直 $G_y$ の勾配を別々に計算し、強度を $|G| = \sqrt{G_x^2 + G_y^2}$ または近似 $|G_x|+|G_y|$ で得る。
- Canny は次のステップを踏む:
  1. ガウシアン平滑化
  2. 勾配計算 (Sobel)
  3. 非極大抑制
  4. 二重閾値処理 (low/high)
  5. ヒステリシスによる連結
- 16 ビット中間表現 (`CV_16S`) で計算し、`cv::convertScaleAbs` で 8 ビットに正規化する。

## ビルド・実行

```bash
cmake --build build -j 06_edge
./build/06_edge/06_edge ../data/building.jpg
```

## 期待される出力

- gray / Sobel x / Sobel y / Sobel mag / Laplacian / Canny の 6 ウィンドウ。

## 参考

- [OpenCV: Canny Edge Detection](https://docs.opencv.org/4.x/da/d22/tutorial_py_canny.html)
