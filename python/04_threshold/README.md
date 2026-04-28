# 04_threshold — 閾値処理・二値化

> はじめての方は [GUIDE.md](GUIDE.md) (やさしい解説) もどうぞ。

## 目的

- `cv2.threshold` の固定閾値 / Otsu / Triangle を比較する。
- 局所的な明るさに対応する `cv2.adaptiveThreshold` を学ぶ。

## ポイント

- `cv2.threshold` は **(retval, dst)** のタプルを返す。`_, binary = cv2.threshold(...)` で不要な返り値を捨てる。
- Otsu は `THRESH_BINARY | THRESH_OTSU` を組み合わせ、閾値は自動設定される。
- `adaptiveThreshold` の `blockSize` は **奇数**、`C` は引き算する定数。
- 照明ムラのある画像には `ADAPTIVE_THRESH_GAUSSIAN_C` が向いている。

## Otsu のアルゴリズム概要

クラス間分散

$$\sigma_B^2(t) = w_0(t)\,w_1(t)\,[\mu_0(t) - \mu_1(t)]^2$$

を最大にする閾値 $t^*$ を全探索する。

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

gray / fixed(127) / fixed_inv / Otsu / Triangle / adaptive-mean / adaptive-Gaussian の各画像が表示される。標準出力に Otsu・Triangle の閾値が表示される。

## 参考

- [OpenCV: Image Thresholding](https://docs.opencv.org/4.x/d7/d4d/tutorial_py_thresholding.html)
