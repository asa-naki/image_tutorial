# やさしい解説: ヒストグラム (Python 版)

## ヒストグラムってなに？

画像の **明るさの棒グラフ** のことです。横軸を「明るさの値 (0〜255)」、縦軸を「その明るさのマスがいくつあるか」にしてグラフを書くと、その画像の **明るさのクセ** が見えます。

- 真っ暗な写真 → 棒が **左 (暗い側) に集中**
- まぶしい写真 → 棒が **右 (明るい側) に集中**
- メリハリのある写真 → **左右に幅広く** 棒が立つ

## Python でヒストグラムを計算する 2 つの方法

### ① OpenCV の calcHist

```python
hist = cv2.calcHist([gray], [0], None, [256], [0, 256])
# hist.shape = (256, 1) ← 1次元の棒グラフが縦方向に並んでいる
```

引数の配列・リストが多くて最初は混乱しますが、「グレー 1 枚 / マスクなし / 256 本 / 0〜255」と読めば OK。

### ② NumPy の histogram

```python
hist, bin_edges = np.histogram(gray.ravel(), bins=256, range=(0, 256))
```

`ravel()` で 2D 配列を 1D に伸ばしてから渡します。NumPy 版は返り値が `ndarray` なので、そのまま NumPy 演算できて便利です。

## matplotlib でヒストグラムを描く

Notebook では `plt.hist()` が一番簡単です。

```python
import matplotlib.pyplot as plt

plt.hist(gray.ravel(), bins=256, range=(0, 256), color='gray')
plt.xlabel('pixel value')
plt.ylabel('count')
plt.show()
```

## ヒストグラム平坦化と CLAHE

棒グラフが片側に偏っていると写真は「のっぺり」して見えます。**平坦化 (equalization)** で棒を横に広げるとメリハリが出ます。

```python
eq = cv2.equalizeHist(gray)                           # グローバル均一化

clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
clahe_img = clahe.apply(gray)                         # ローカル均一化
```

**CLAHE** はブロックごとに均一化するので、照明ムラがある画像で特に効果的です。カラー画像に適用するときは、Lab 色空間の **L チャネルだけ** に使うのがコツです。

## 一言まとめ

ヒストグラムは **画像の明るさの個性を見る棒グラフ**。Python では matplotlib と組み合わせて視覚的に確かめながら、CLAHE で **自然なコントラスト強調** を試してみましょう。
