# 12_video — 動画・カメラ入力

> はじめての方は [GUIDE.md](GUIDE.md) (やさしい解説) もどうぞ。

## 目的

- `cv2.VideoCapture` で動画ファイル・カメラを開き、フレームを逐次取得する。
- フレームごとに画像処理 (Canny エッジ + オーバーレイ) を適用する。
- `cv2.VideoWriter` で処理済み動画を保存する。
- Lucas-Kanade オプティカルフローでフレーム間の動きを追う。

## ポイント

- `cap.read()` は **(ret, frame)** のタプルを返す。`ret=False` でストリーム終端または読み取り失敗。
- `cap.get(cv2.CAP_PROP_FPS)` などでメタ情報を取得する。
- Jupyter では `cv2.imshow` が動かないことが多いため、`--no-show` フラグで matplotlib モードに切り替える。
- `VideoWriter` のコーデックは OS 依存。`mp4v` (Mac/Linux) や `XVID` (Windows) を試す。

## 実行

# Linux / Ubuntu
```bash
# 動画ファイル (ウィンドウ表示)
python3 main.py --video ../data/sample.mp4
# カメラ
python3 main.py --camera 0
# 処理結果を保存
python3 main.py --video ../data/sample.mp4 --output processed.mp4
# Notebook 風 (フレーム静止画を matplotlib 表示)
python3 main.py --video ../data/sample.mp4 --no-show
```

# Windows / macOS
```bash
# 動画ファイル (ウィンドウ表示)
python main.py --video ../data/sample.mp4
# カメラ
python main.py --camera 0
# 処理結果を保存
python main.py --video ../data/sample.mp4 --output processed.mp4
# Notebook 風 (フレーム静止画を matplotlib 表示)
python main.py --video ../data/sample.mp4 --no-show
```

## 期待される出力

- CLI モード: リアルタイムウィンドウ表示。ESC / `q` で終了。
- `--no-show` モード: 等間隔フレームの元画像と処理済み画像を並べて表示。

## 参考

- [OpenCV: Video Capture](https://docs.opencv.org/4.x/dd/d43/tutorial_py_video_display.html)
- [OpenCV: Optical Flow](https://docs.opencv.org/4.x/d4/dee/tutorial_optical_flow.html)
