# やさしい解説: 特徴点検出とマッチング (Python 版)

## 「特徴点」ってなに？

画像のなかで **目立つ場所**、たとえば **建物のカド** や **看板の角** のような点のこと。「どこから見てもわかりやすい目印」です。

身近な例: 友達と待ち合わせするとき、「コンビニの角」「信号の柱」と決めますね。広い空や真っ白い壁の真ん中はダメ。特徴点とは画像版の "わかりやすい待ち合わせ場所" です。

## やることは 3 ステップ

1. **検出 (detect)**: 画像から「目立つ点」を探す
2. **記述 (describe)**: その点のまわりの見た目を短いデータ列 (記述子) に変換する
3. **マッチング (match)**: 2 枚の画像の記述子を見比べて、似ているペアを見つける

## Python での書き方

```python
# ORB (OpenCV 標準。ライセンス問題なし)
orb = cv2.ORB_create(nfeatures=500)
kp1, des1 = orb.detectAndCompute(gray1, None)
kp2, des2 = orb.detectAndCompute(gray2, None)

# ブルートフォースマッチング
bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
matches = sorted(bf.match(des1, des2), key=lambda m: m.distance)

# 上位 N 件を描画
result = cv2.drawMatches(img1, kp1, img2, kp2, matches[:50], None,
    flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
```

### 記述子の型に合ったノルムを使う

| アルゴリズム | 記述子の型 | 使うノルム |
|-------------|-----------|-----------|
| ORB, AKAZE  | バイナリ (0/1の列) | `NORM_HAMMING` |
| SIFT        | float 配列 | `NORM_L2` |

## NumPy で対応点の座標を取り出す

マッチング結果から座標を取り出すとホモグラフィ推定などに使えます。

```python
src_pts = np.float32([kp1[m.queryIdx].pt for m in matches]).reshape(-1, 1, 2)
dst_pts = np.float32([kp2[m.trainIdx].pt for m in matches]).reshape(-1, 1, 2)

H, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
```

## SIFT を使いたいとき

SIFT は `opencv-contrib-python` が必要です。

```bash
pip install opencv-contrib-python
```

```python
sift = cv2.SIFT_create()   # opencv-contrib が入っていれば使える
```

## 一言まとめ

特徴点マッチングは **「目立つ点と、その近所の見た目を覚えて、別の画像と照らし合わせる方法」**。Python では `detectAndCompute` → `BFMatcher.match` → `drawMatches` の 3 ステップがほぼ定型です。
