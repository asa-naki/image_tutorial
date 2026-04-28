# 13_calibration — カメラキャリブレーション

> はじめての方は [GUIDE.md](GUIDE.md) (やさしい解説) もどうぞ。

## 目的

- `cv2.findChessboardCorners` + `cv2.cornerSubPix` でサブピクセル精度のコーナーを検出する。
- `cv2.calibrateCamera` でカメラ行列 K と歪み係数 dist を推定する。
- `cv2.undistort` で歪み補正画像を生成する。
- 結果を `np.savez` で保存する。

## ポイント

- チェスボード画像は **10〜20 枚** 以上、様々な角度・距離で撮影する。
- `findChessboardCorners` の `patternSize = (cols, rows)` は **内側のコーナー数** (白黒の境目の数)。9×6 のボードなら `(9, 6)`。
- `cornerSubPix` で精密化するとキャリブレーション誤差が減る。
- 再投影誤差 (RMS) が **1 ピクセル以下** を目安にする。

## パラメータ

| 引数 | 説明 |
|------|------|
| `--cols` | 内側コーナーの列数 (デフォルト 9) |
| `--rows` | 内側コーナーの行数 (デフォルト 6) |
| `--square` | 1 マスの実サイズ [m] (デフォルト 0.025) |

## 実行

# Linux / Ubuntu
```bash
# 実際のチェスボード画像ディレクトリを指定
python3 main.py /path/to/chessboard_images/ --cols 9 --rows 6
# 合成チェスボードでデモ (引数省略)
python3 main.py
python3 main.py --no-show
```

# Windows / macOS
```bash
# 実際のチェスボード画像ディレクトリを指定
python main.py /path/to/chessboard_images/ --cols 9 --rows 6
# 合成チェスボードでデモ (引数省略)
python main.py
python main.py --no-show
```

## 期待される出力

- コーナー描画済み画像 × 最大 4 枚を表示。
- 元画像と補正済み画像を並べて表示。
- `camera_matrix.npz` にカメラ行列 / 歪み係数 / RMS を保存。
- 標準出力に RMS・K・dist。

## 参考

- [OpenCV: Camera Calibration](https://docs.opencv.org/4.x/dc/dbb/tutorial_py_calibration.html)
