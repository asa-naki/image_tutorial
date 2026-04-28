# 11_features — 特徴点検出・マッチング

> はじめての方は [GUIDE.md](GUIDE.md) (やさしい解説) もどうぞ。

## 目的

- `cv2.ORB_create` / `cv2.AKAZE_create` で特徴点を検出・記述する。
- `cv2.BFMatcher` でブルートフォースマッチングを行う。
- `cv2.drawMatches` で対応点を可視化する。

## ポイント

- バイナリ記述子 (ORB / AKAZE) には `NORM_HAMMING`、float 記述子 (SIFT) には `NORM_L2` を使う。
- `crossCheck=True` にすると双方向でマッチングが成立した組のみ残る (精度向上)。
- SIFT は `opencv-contrib-python` が必要: `pip install opencv-contrib-python`。
- `findHomography` + `RANSAC` で誤対応を除去し、カメラ間の変換行列を推定できる。

## アルゴリズム比較

| 手法 | 記述子 | ノルム | contrib 必須 |
|------|-------|--------|-------------|
| ORB | Binary (256bit) | NORM_HAMMING | 不要 |
| AKAZE | Binary (486bit) | NORM_HAMMING | 不要 |
| SIFT | float (128次元) | NORM_L2 | **必要** |

## 実行

# Linux / Ubuntu
```bash
# 1枚の画像を回転させて自己マッチング
python3 main.py ../data/lena.png
# 2枚の画像でマッチング
python3 main.py ../data/img1.png ../data/img2.png
python3 main.py ../data/lena.png --no-show
```

# Windows / macOS
```bash
# 1枚の画像を回転させて自己マッチング
python main.py ../data/lena.png
# 2枚の画像でマッチング
python main.py ../data/img1.png ../data/img2.png
python main.py ../data/lena.png --no-show
```

## 期待される出力

img1 / img2 (回転済) / ORB keypoints / ORB matches / AKAZE matches の各画像が表示される。標準出力に各手法の検出数・マッチング数。

## 参考

- [OpenCV: Feature Detection and Description](https://docs.opencv.org/4.x/db/d27/tutorial_py_table_of_contents_feature2d.html)
