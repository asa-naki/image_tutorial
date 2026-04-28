# 12_video — 動画・カメラ入力

> はじめての方は [GUIDE.md](GUIDE.md) (中学生向けやさしい解説) もどうぞ。

## 目的

- `cv::VideoCapture` でファイルおよびカメラから映像を読む。
- `cv::VideoWriter` で動画を書き出す。
- `cv::BackgroundSubtractorMOG2` で前景マスクを作る。

## ポイント

- ファイル: パス文字列、カメラ: 整数 (`0`) を `open` に渡す。
- ループ内で `cap.read(frame)` が `false` になったら終了。
- 書き出しは `fourcc('m','p','4','v')` を用いると `.mp4` で保存できる (OS/ビルド依存)。
- カメラが無い環境では引数にビデオファイルを渡してください。

## ビルド・実行

```bash
cmake --build build -j 12_video

# ファイルを処理
./build/12_video/12_video ../data/video.mp4

# カメラ 0 から
./build/12_video/12_video 0
```

## 期待される出力

- `frame` と `fg mask` の 2 ウィンドウ。ESC で終了。
- カレントディレクトリに `12_video_out.mp4` が作成される。

## 参考

- [OpenCV: Video I/O](https://docs.opencv.org/4.x/dd/de7/group__videoio.html)
- [OpenCV: Background Subtraction](https://docs.opencv.org/4.x/d1/dc5/tutorial_background_subtraction.html)
