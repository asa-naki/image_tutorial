# 07_morphology — モルフォロジー演算

> はじめての方は [GUIDE.md](GUIDE.md) (中学生向けやさしい解説) もどうぞ。

## 目的

- 構造要素 (kernel) と 7 種類のモルフォロジー演算を理解する。

## 定義

二値画像 $A$ に対する構造要素 $B$ で:

- 収縮 (erode): $A \ominus B$ — 細らせる
- 膨張 (dilate): $A \oplus B$ — 太らせる
- 開く (opening): $(A \ominus B) \oplus B$ — 小さなノイズ除去
- 閉じる (closing): $(A \oplus B) \ominus B$ — 小さな穴埋め
- 勾配 (gradient): $(A \oplus B) - (A \ominus B)$ — エッジ抽出
- トップハット: $A - \text{open}(A)$ — 局所明部
- ブラックハット: $\text{close}(A) - A$ — 局所暗部

## ビルド・実行

```bash
cmake --build build -j 07_morphology
./build/07_morphology/07_morphology ../data/lena.png
```

## 期待される出力

- 二値画像と各演算結果 8 ウィンドウ。

## 参考

- [OpenCV: Morphological Operations](https://docs.opencv.org/4.x/d9/d61/tutorial_py_morphological_ops.html)
