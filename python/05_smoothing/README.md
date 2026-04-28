# 05_smoothing — 平滑化フィルタ

> はじめての方は [GUIDE.md](GUIDE.md) (やさしい解説) もどうぞ。

## 目的

- Box / Gaussian / Median / Bilateral の 4 種を比較する。
- `cv2.filter2D` でカスタムカーネルを適用する。
- NumPy でノイズ画像を生成してフィルタ効果を確認する。

## ポイント

- `cv2.GaussianBlur` の `ksize` は **タプル (奇数, 奇数)** で渡す。
- `cv2.medianBlur` の ksize は **奇数の整数** (タプル不可)。
- `cv2.add` は飽和演算 (255 超えで丸め)。NumPy の `+` はラップアラウンド — 画像処理では `cv2.add` を使う。
- バイラテラルは処理が重い (`sigmaColor=75, sigmaSpace=75` あたりが出発点)。

## フィルタ比較

| フィルタ | エッジ保持 | S&P ノイズ | 速度 |
|---------|----------|-----------|------|
| Box     | ×        | 弱        | 速   |
| Gaussian| △        | 中        | 速   |
| Median  | △        | **強い**  | 中   |
| Bilateral| ○       | 中        | 遅   |

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

src / noisy / box / Gaussian / median / bilateral / sharpened の各画像が表示される。

## 参考

- [OpenCV: Smoothing Images](https://docs.opencv.org/4.x/d4/d13/tutorial_py_filtering.html)
