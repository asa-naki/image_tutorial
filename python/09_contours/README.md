# 09_contours — 輪郭検出・形状特徴

> はじめての方は [GUIDE.md](GUIDE.md) (やさしい解説) もどうぞ。

## 目的

- `cv2.findContours` で輪郭の点列を取得する。
- `cv2.drawContours` で輪郭・凸包・近似多角形を描画する。
- `cv2.moments` で面積・重心を計算する。
- バウンディングボックス / 最小外接円 / 最小外接矩形 (回転あり) を求める。

## ポイント

- `findContours` の返り値は **(contours, hierarchy)**。OpenCV 4 では常に 2 値。
- `contours` の各要素は `shape = (N, 1, 2)` の `int32` 配列。`reshape(-1, 2)` で `(N, 2)` に変換すると NumPy 演算がしやすい。
- 小さな輪郭はリスト内包表記 `[c for c in contours if cv2.contourArea(c) > 100]` でフィルタする。
- `approxPolyDP` の `epsilon` は `0.01〜0.05 × arcLength` が目安。大きいほど頂点が少なくなる。

## 主な関数

| 関数 | 返り値の意味 |
|------|------------|
| `contourArea(c)` | 面積 (ピクセル²) |
| `arcLength(c, True)` | 周長 |
| `boundingRect(c)` | `(x, y, w, h)` |
| `minEnclosingCircle(c)` | `((cx, cy), r)` |
| `minAreaRect(c)` | 回転あり矩形 → `boxPoints` で頂点取得 |

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

src / binary / all contours / bounding box / min circle / min area rect / convex hull / approx poly の各画像が表示される。標準出力に最大輪郭の面積・重心。

## 参考

- [OpenCV: Contours in OpenCV](https://docs.opencv.org/4.x/d3/d05/tutorial_py_table_of_contents_contours.html)
