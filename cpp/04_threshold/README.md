# 04_threshold — 閾値処理

> はじめての方は [GUIDE.md](GUIDE.md) (中学生向けやさしい解説) もどうぞ。

## 目的

- `cv::threshold` の固定閾値と Otsu の自動閾値を比較する。
- 局所的な明るさに対応する `cv::adaptiveThreshold` を学ぶ。

## ポイント

- Otsu はクラス間分散最大化により最適閾値 $t^*$ を選ぶ:

$$
t^* = \arg\max_{t}\, w_0(t)\, w_1(t)\, (\mu_0(t) - \mu_1(t))^2
$$

- Adaptive は局所窓 (`blockSize`) の平均/重み付き平均から閾値を引いた値を画素ごとの閾値に使う。照明ムラに強い。
- `blockSize` は奇数。`C` は引き算する定数。

## ビルド・実行

```bash
cmake --build build -j 04_threshold
./build/04_threshold/04_threshold ../data/lena.png
```

## 期待される出力

- gray / 固定閾値 / Otsu / Adaptive Mean / Adaptive Gaussian の 5 ウィンドウ。
- 標準出力に Otsu が選んだ閾値。

## 参考

- [OpenCV: Image Thresholding](https://docs.opencv.org/4.x/d7/d4d/tutorial_py_thresholding.html)
