# やさしい解説: モルフォロジー演算 (Python 版)

## 名前は難しいけど、やってることはシンプル

白黒画像の **白い部分を太らせたり細らせたり** する処理です。スタンプを **押す/削る** イメージ。

## 2 つの基本演算

- **膨張 (dilate)**: 白い部分が **太くなる** (周りに白を広げる)
- **収縮 (erode)**: 白い部分が **細くなる** (端を削る)

身近な例: 二値化したテキストにゴマ塩ノイズが乗ったとき、**収縮 → 膨張** でノイズだけ消して文字の太さを元に戻せます。

## 組み合わせワザ

| 名前 | やること | 効果 |
|---|---|---|
| **オープン (open)** | 収縮 → 膨張 | **小さな白いノイズを消す** |
| **クローズ (close)** | 膨張 → 収縮 | **白の中の小さな黒い穴を埋める** |
| **勾配 (gradient)** | 膨張 − 収縮 | **輪郭だけ取り出す** |
| **トップハット** | 元 − オープン | **明るい小さな点を浮かす** |
| **ブラックハット** | クローズ − 元 | **暗い小さな点を浮かす** |

## Python での書き方

```python
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))

# 基本演算
eroded  = cv2.erode(binary, kernel, iterations=2)
dilated = cv2.dilate(binary, kernel, iterations=2)

# 派生演算は morphologyEx でまとめて
opened   = cv2.morphologyEx(binary, cv2.MORPH_OPEN,     kernel)
closed   = cv2.morphologyEx(binary, cv2.MORPH_CLOSE,    kernel)
gradient = cv2.morphologyEx(binary, cv2.MORPH_GRADIENT, kernel)
tophat   = cv2.morphologyEx(src,    cv2.MORPH_TOPHAT,   kernel)
blackhat = cv2.morphologyEx(src,    cv2.MORPH_BLACKHAT, kernel)
```

### 構造要素の形を変える

```python
rect    = cv2.getStructuringElement(cv2.MORPH_RECT,    (7, 7))  # 四角
cross   = cv2.getStructuringElement(cv2.MORPH_CROSS,   (7, 7))  # 十字
ellipse = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))  # 楕円
```

楕円は斜め方向のエッジに対して自然な膨張・収縮をかけたいときに便利です。

## NumPy との等価表現

`MORPH_GRADIENT` は `dilate(img) - erode(img)` と同じです。NumPy で書くと:

```python
grad = dilated.astype(np.int16) - eroded.astype(np.int16)
grad = np.clip(grad, 0, 255).astype(np.uint8)
```

`morphologyEx` を使う方が簡潔で速いですが、仕組みを理解するために自分で書いてみるのも良い練習です。

## 一言まとめ

モルフォロジー演算は **「白黒画像をスタンプで押したり削ったりする道具」**。`getStructuringElement` でスタンプの形を決めて、`morphologyEx` を呼ぶだけで大抵の操作がこなせます。
