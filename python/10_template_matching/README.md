# 10_template_matching — テンプレートマッチング

> はじめての方は [GUIDE.md](GUIDE.md) (やさしい解説) もどうぞ。

## 目的

- `cv2.matchTemplate` でスライディングウィンドウの類似度マップを計算する。
- `cv2.minMaxLoc` で最良マッチ位置を取得する。
- 4 種類のマッチング手法を比較する。

## ポイント

- `matchTemplate` の返り値は `float32` の NumPy 配列。`imshow` でそのまま表示可能。
- `TM_SQDIFF` 系は **最小値** が最良。`TM_CCORR_NORMED` / `TM_CCOEFF_NORMED` は **最大値** が最良。
- 通常は **`TM_CCOEFF_NORMED` を使う** (明るさの違いに強い)。
- テンプレートマッチングは **サイズ・回転の違いに弱い**。次セクションの特徴点マッチングと使い分ける。

## 実行

# Linux / Ubuntu
```bash
# テンプレートを自動生成 (画像中央 1/4)
python3 main.py ../data/lena.png
# テンプレートを別ファイルで指定
python3 main.py ../data/lena.png ../data/template.png
python3 main.py ../data/lena.png --no-show
```

# Windows / macOS
```bash
# テンプレートを自動生成 (画像中央 1/4)
python main.py ../data/lena.png
# テンプレートを別ファイルで指定
python main.py ../data/lena.png ../data/template.png
python main.py ../data/lena.png --no-show
```

## 期待される出力

src / template / 4 手法それぞれの結果画像 (赤矩形でマッチ位置を表示) が表示される。標準出力に各手法のスコアと座標。

## 参考

- [OpenCV: Template Matching](https://docs.opencv.org/4.x/d4/dc6/tutorial_py_template_matching.html)
