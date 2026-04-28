# 13_calibration — カメラキャリブレーション

> はじめての方は [GUIDE.md](GUIDE.md) (中学生向けやさしい解説) もどうぞ。

## 目的

- チェスボードコーナー検出 → `cv::calibrateCamera` → 歪み補正の流れを学ぶ。
- Eigen で内部行列を保持し、1 視点目の再投影誤差を手動で再計算する。

## 理論メモ

ピンホールカメラモデル:

$$
s\, \mathbf{m} = K \, [R \mid t] \, \mathbf{M}, \qquad
K = \begin{pmatrix} f_x & 0 & c_x \\ 0 & f_y & c_y \\ 0 & 0 & 1 \end{pmatrix}
$$

歪み係数 $(k_1, k_2, p_1, p_2, k_3)$ を含めて再投影誤差を最小化する非線形最適化を、`calibrateCamera` が内部で実行します。

## ビルド・実行

```bash
cmake --build build -j 13_calibration
./build/13_calibration/13_calibration ../data/chessboard 9 6 1.0
```

引数: `<dir> <cols> <rows> <square_size>`。OpenCV 同梱の `left01.jpg` 〜 `left14.jpg` は `9 x 6` パターン。

## 期待される出力

- 標準出力に RMS 誤差と内部行列 `K`、歪み係数。
- view0 の再投影誤差 (手計算) も表示し、`calibrateCamera` の結果と整合することを確認。
- ウィンドウに 1) コーナー描画、2) 歪み補正後画像。

## 参考

- [OpenCV: Camera Calibration](https://docs.opencv.org/4.x/dc/dbb/tutorial_py_calibration.html)
