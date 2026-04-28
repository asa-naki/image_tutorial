# 03_geometry — 幾何変換

> はじめての方は [GUIDE.md](GUIDE.md) (中学生向けやさしい解説) もどうぞ。

## 目的

- リサイズ・回転・アフィン変換・射影変換 (ホモグラフィ) を扱う。
- Eigen で 3x3 の変換行列を構築し、`cv::warpPerspective` に渡す。

## ポイント

アフィン変換は 2x3 行列 $M$ で

$$
\begin{pmatrix} x' \\ y' \end{pmatrix} = M \begin{pmatrix} x \\ y \\ 1 \end{pmatrix}
$$

ホモグラフィ (射影変換) は 3x3 行列 $H$ で

$$
\begin{pmatrix} x' \\ y' \\ w' \end{pmatrix} = H \begin{pmatrix} x \\ y \\ 1 \end{pmatrix}, \quad
\hat x = x'/w', \ \hat y = y'/w'
$$

OpenCV/Eigen の row-major / column-major 違いに注意。`cv::Mat::at<double>(row,col)` と `Eigen::Matrix(row,col)` でアクセスして要素を写すのが安全。

## ビルド・実行

```bash
cmake --build build -j 03_geometry
./build/03_geometry/03_geometry ../data/lena.png
```

## 期待される出力

- 元画像 / 半分にリサイズ / 30°回転 / 3点アフィン / Eigen 由来のホモグラフィ の 5 ウィンドウ。
- 標準出力に Eigen の `H` 行列。

## 参考

- [OpenCV: Geometric Transformations](https://docs.opencv.org/4.x/da/d54/group__imgproc__transform.html)
