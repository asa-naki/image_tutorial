# 11_features — 特徴点検出とマッチング

> はじめての方は [GUIDE.md](GUIDE.md) (中学生向けやさしい解説) もどうぞ。

## 目的

- ORB / AKAZE / SIFT で keypoint と descriptor を検出する。
- BFMatcher + Lowe's ratio test で良好な対応を選び、RANSAC でホモグラフィ推定する。

## ポイント

- バイナリ記述子 (ORB / AKAZE) は `NORM_HAMMING`、float 記述子 (SIFT) は `NORM_L2`。
- Lowe's ratio test:

$$
\text{accept } m_1 \iff \frac{d(m_1)}{d(m_2)} < 0.75
$$

- `cv::findHomography(..., cv::RANSAC, 3.0, mask)` で外れ値除去。`mask` を `drawMatches` に渡せばインライアのみ強調できる。
- OpenCV 4.4 以降は SIFT が main に統合されており `cv::SIFT::create()` で使える。

## ビルド・実行

```bash
cmake --build build -j 11_features
./build/11_features/11_features ../data/book1.jpg ../data/book2.jpg
```

## 期待される出力

- ORB / AKAZE / SIFT の対応マッチ画像 (RANSAC インライアのみ表示)。
- 標準出力に検出キーポイント数と良好マッチ数。

## 参考

- [OpenCV: Feature Matching](https://docs.opencv.org/4.x/dc/dc3/tutorial_py_matcher.html)
