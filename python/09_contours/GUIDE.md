# やさしい解説: 輪郭検出 (Python 版)

## 輪郭ってなに？

白黒画像のなかで **白い島の縁 (へり)** をぐるっとなぞった線のこと。Python では座標 (x, y) の点を並べた **NumPy 配列のリスト** として返ってきます。

身近な例: 紙にハサミで切り抜いた星の形。星の **外側の縁** を指でなぞった軌跡が「輪郭」です。

## Python での返り値を理解する

```python
contours, hierarchy = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
```

- `contours`: 輪郭のリスト。各要素は `shape = (点数, 1, 2)` の NumPy 配列
- `hierarchy`: 輪郭の親子関係 (穴の中に穴など)

**OpenCV 3 と 4 で返り値の数が違う** ことがあるので注意。OpenCV 4 では常に 2 つ返ります。

## 面積でノイズを除去する

```python
# 面積が 100 ピクセル未満の小さな輪郭を除く
contours = [c for c in contours if cv2.contourArea(c) > 100]
```

Python のリスト内包表記でスッキリ書けます。

## 輪郭から形の特徴を取り出す

```python
for c in contours:
    area    = cv2.contourArea(c)                # 面積
    peri    = cv2.arcLength(c, True)            # 周長
    M       = cv2.moments(c)                    # モーメント
    cx      = int(M['m10'] / M['m00'])          # 重心 x
    cy      = int(M['m01'] / M['m00'])          # 重心 y
    x,y,w,h = cv2.boundingRect(c)              # 外接矩形

    # 近似多角形 (頂点の数で三角・四角…を判定)
    eps    = 0.02 * peri
    approx = cv2.approxPolyDP(c, eps, True)
    print(f'頂点数: {len(approx)}')             # 3→三角、4→四角、…
```

## NumPy でできる形状チェック

輪郭点は NumPy 配列なので、そのまま NumPy で扱えます。

```python
# 輪郭点の最大 x 座標を取得
pts = c.reshape(-1, 2)          # (N, 1, 2) → (N, 2)
max_x = pts[:, 0].max()
```

## 一言まとめ

輪郭検出は **「白い島の縁を NumPy 配列の点列にする」処理**。リスト内包表記でフィルタして、`moments` や `arcLength` で形の特徴を数字として取り出すと、物の大きさ・形・場所を自動で判断できます。
