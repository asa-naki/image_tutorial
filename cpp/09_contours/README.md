# 09_contours — 輪郭検出と形状特徴

> はじめての方は [GUIDE.md](GUIDE.md) (中学生向けやさしい解説) もどうぞ。

## 目的

- `cv::findContours` で輪郭を抽出する。
- `cv::contourArea`, `cv::boundingRect`, `cv::moments`, `cv::approxPolyDP` で形状特徴を取り出す。

## ポイント

- 入力は通常二値画像 (背景 0、対象 255)。Otsu + `THRESH_BINARY_INV` で対象を白くする。
- `RETR_EXTERNAL` は最外輪郭のみ。階層が必要なら `RETR_TREE`。
- 重心は 0次/1次モーメントから

$$
\bar x = M_{10}/M_{00}, \quad \bar y = M_{01}/M_{00}
$$

## ビルド・実行

```bash
cmake --build build -j 09_contours
./build/09_contours/09_contours ../data/lena.png
```

## 期待される出力

- 元画像 / 二値化 / 輪郭描画 / 外接矩形+重心 の 4 ウィンドウ。
- 標準出力に各輪郭の面積と近似頂点数。

## 参考

- [OpenCV: Contour Features](https://docs.opencv.org/4.x/dd/d49/tutorial_py_contour_features.html)
