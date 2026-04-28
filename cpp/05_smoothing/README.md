# 05_smoothing — 平滑化フィルタ

> はじめての方は [GUIDE.md](GUIDE.md) (中学生向けやさしい解説) もどうぞ。

## 目的

- 4 種類の平滑化フィルタを比較する: Box / Gaussian / Median / Bilateral。

## 特徴

| フィルタ    | 概要                                      | 強み                  | 弱み                |
| ----------- | ----------------------------------------- | --------------------- | ------------------- |
| Box         | 単純平均                                  | 高速                  | エッジが甘くなる    |
| Gaussian    | 重み $G(x,y) = e^{-(x^2+y^2)/(2\sigma^2)}$ | 自然なぼかし          | エッジが甘くなる    |
| Median      | カーネル内中央値                          | 塩胡椒ノイズに強い    | テクスチャを潰す    |
| Bilateral   | 距離 + 輝度差で重み付け                   | エッジ保存            | 計算が重い          |

## ビルド・実行

```bash
cmake --build build -j 05_smoothing
./build/05_smoothing/05_smoothing ../data/lena.png
```

## 期待される出力

- 元画像 / ノイズ付加 / 各フィルタ結果 の 6 ウィンドウ。

## 参考

- [OpenCV: Smoothing Images](https://docs.opencv.org/4.x/dc/dd3/tutorial_gausian_median_blur_bilateral_filter.html)
