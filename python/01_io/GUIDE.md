# やさしい解説: 画像入出力・表示 (Python 版)

## 画像って、コンピュータの中ではどうなってるの？

写真は人間の目には「きれいな絵」に見えますが、コンピュータは絵を **とても小さなマス目 (= 画素・ピクセル)** に分けて、一つひとつのマス目に「色の数字」を入れて覚えています。

たとえば 512×512 の画像には、横 512 個 × 縦 512 個のマス目があり、それぞれに「青・緑・赤」3 つの数字 (各 0〜255) が入っています。

## Python での画像は「NumPy 配列」

C++ の画像は `cv::Mat` という専用の型でしたが、Python では **NumPy の `ndarray`** がそのまま画像になります。

```python
import cv2
import numpy as np

img = cv2.imread("lena.png")
print(type(img))    # <class 'numpy.ndarray'>
print(img.shape)    # (512, 512, 3)  → (縦, 横, チャネル数)
print(img.dtype)    # uint8  → 0〜255 の整数
```

NumPy を知っていれば、画像もスライスで切り取れます。

```python
roi = img[100:200, 50:150]   # y=100〜200, x=50〜150 の領域
```

## なぜ「BGR」なの？ RGB じゃないの？

ふつう「光の三原色」は **R (赤) G (緑) B (青)** の順で習いますね。でも OpenCV では昔の事情で **B → G → R の順** で並んでいます。

- matplotlib や PIL は **RGB** 順を期待する
- OpenCV は **BGR** 順を使う

**つなぎ目を変換するひと工夫** が必要です。

```python
rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # matplotlib に渡す前に
# または
rgb = img[:, :, ::-1]                        # NumPy スライスで逆順にする
```

## カラーとグレースケールの違い

- **カラー画像**: `shape = (H, W, 3)`。1 マスに 3 つの数字 (B, G, R)
- **グレースケール画像**: `shape = (H, W)`。1 マスに 1 つの数字 (明るさだけ)

データ量が 1/3、NumPy の計算も速くなります。

## Jupyter Notebook での表示

`cv2.imshow` はターミナル環境向けです。Notebook では **matplotlib** を使います。

```python
import matplotlib.pyplot as plt

plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
plt.axis('off')
plt.show()
```

このチュートリアルの `utils.show_nb()` はこの処理をまとめて、複数画像を並べて表示してくれます。

## 一言まとめ

Python での画像は **NumPy 配列**。`shape` と `dtype` を確認する習慣と、**BGR → RGB の変換**さえ押さえれば、あとは NumPy 操作として自然に扱えます。
