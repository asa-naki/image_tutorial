# 03_geometry — 幾何変換

> はじめての方は [GUIDE.md](GUIDE.md) (やさしい解説) もどうぞ。

## 目的

- `cv2.resize` でスケーリング (INTER_AREA / INTER_LINEAR)。
- `cv2.getRotationMatrix2D` + `cv2.warpAffine` で回転。
- 3 点対応アフィン変換 (`cv2.getAffineTransform`)。
- 3×3 ホモグラフィ行列を NumPy で組んで `cv2.warpPerspective` に渡す。
- `cv2.flip` で反転。

## ポイント

- アフィン変換行列は **2×3 の NumPy 配列** (float64)。
- 射影変換行列は **3×3 の NumPy 配列** (float64)。
- リサイズ縮小時は `INTER_AREA`、拡大時は `INTER_LINEAR` or `INTER_CUBIC` を使う。
- `fx=0.5, fy=0.5` のように倍率指定もできる (この場合 `dsize=(0,0)`)。

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

src / resize×0.5 / rotate 30° / affine (3pt) / perspective / flip-h / flip-v が表示される。

## 参考

- [OpenCV: Geometric Transformations](https://docs.opencv.org/4.x/da/d6e/tutorial_py_geometric_transformations.html)
