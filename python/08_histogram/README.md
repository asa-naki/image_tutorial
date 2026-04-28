# 08_histogram — ヒストグラム

> はじめての方は [GUIDE.md](GUIDE.md) (やさしい解説) もどうぞ。

## 目的

- `cv2.calcHist` でヒストグラムを計算し、matplotlib で可視化する。
- `cv2.equalizeHist` でグローバルヒストグラム均一化を行う。
- `cv2.createCLAHE` + `apply` で局所的なコントラスト強調 (CLAHE) を行う。

## ポイント

- `calcHist` の返り値は `shape=(256, 1)` の `float32` 配列。`flatten()` or `ravel()` で 1D に変換してからプロット。
- `equalizeHist` はグレースケール画像専用。カラー画像には **Lab の L チャネルだけ** に適用する。
- CLAHE の `clipLimit`: 大きいほどコントラスト強調が強い。`tileGridSize`: 小さいほど局所的。

## CLAHE のパラメータ目安

| `clipLimit` | `tileGridSize` | 適した用途 |
|-------------|----------------|-----------|
| 2.0 | (8, 8) | 一般的な用途 |
| 4.0 | (4, 4) | 医療・暗所画像 |

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

gray / hist / equalizeHist / hist-eq / CLAHE / hist-CLAHE / color CLAHE (Lab) の各画像・グラフが表示される。標準出力に mean / std を出力。

## 参考

- [OpenCV: Histograms](https://docs.opencv.org/4.x/d1/db7/tutorial_py_histogram_begins.html)
- [OpenCV: Histogram Equalization](https://docs.opencv.org/4.x/d5/daf/tutorial_py_histogram_equalization.html)
