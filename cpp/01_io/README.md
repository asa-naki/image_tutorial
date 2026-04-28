# 01_io — 画像入出力・表示

> はじめての方は [GUIDE.md](GUIDE.md) (中学生向けやさしい解説) もどうぞ。

## 目的

- `cv::imread` / `cv::imwrite` / `cv::imshow` / `cv::waitKey` の基本的な使い方を学ぶ。
- `cv::Mat` の `cols`, `rows`, `channels()`, `type()` を確認する。

## ポイント

- OpenCV のチャネル順は **BGR** (RGB ではない)。
- `cv::IMREAD_COLOR` で 3ch、`cv::IMREAD_GRAYSCALE` で 1ch。
- 保存形式は拡張子で決まる (`.png`, `.jpg`, ...)。
- `cv::waitKey(0)` はキー入力待ち (戻り値はキーコード)。

## ビルド・実行

```bash
cd image_tutorial/cpp
cmake -S . -B build && cmake --build build -j 01_io
./build/01_io/01_io ../data/lena.png 01_io_out.png
```

## 期待される出力

- 標準出力に画像のサイズ・チャネル数・型情報。
- `01_io_out.png` がカレントディレクトリに保存される。
- ウィンドウに `color` と `gray` が表示される。ESC または `q` で終了。

## 参考

- [OpenCV: imread](https://docs.opencv.org/4.x/d4/da8/group__imgcodecs.html#gab32ee19e22660912565f8140d0f675a8)
- [OpenCV: Mat の基本](https://docs.opencv.org/4.x/d3/d63/classcv_1_1Mat.html)
