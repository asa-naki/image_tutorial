# 01_io — 画像入出力・表示

> はじめての方は [GUIDE.md](GUIDE.md) (やさしい解説) もどうぞ。

## 目的

- `cv2.imread` / `cv2.imwrite` で画像を読み込み・保存する。
- NumPy 配列の `shape`, `dtype` で画像のサイズ・チャネル・型を確認する。
- matplotlib でインライン表示する (Notebook)。
- `cv2.imshow` / `cv2.waitKey` でウィンドウ表示する (CLI)。

## ポイント

- OpenCV のチャネル順は **BGR** (RGB ではない)。matplotlib に渡す前に `cv2.cvtColor(..., COLOR_BGR2RGB)` が必要。
- `imread` は失敗しても **`None` を返すだけで例外を投げない**。必ず `None` チェックを行う。
- 保存形式は拡張子で決まる (`.png` / `.jpg` / `.bmp` …)。

## 実行

# Linux / Ubuntu
```bash
# CLI (ウィンドウ表示)
python3 main.py ../data/lena.png output.png
# ウィンドウを出さずに保存のみ
python3 main.py ../data/lena.png output.png --no-show
```

# Windows / macOS
```bash
# CLI (ウィンドウ表示)
python main.py ../data/lena.png output.png
# ウィンドウを出さずに保存のみ
python main.py ../data/lena.png output.png --no-show
```

Notebook は `notebook.ipynb` を Jupyter で開いて上から実行してください。

## 期待される出力

- 標準出力に `size / chans / dtype`。
- `01_io_out.png` がカレントディレクトリに保存される。
- color / gray / bgra の 3 種類の画像が表示される。

## 参考

- [OpenCV: imread](https://docs.opencv.org/4.x/d4/da8/group__imgcodecs.html#gab32ee19e22660912565f8140d0f675a8)
- [NumPy: ndarray](https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html)
