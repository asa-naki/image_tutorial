# 07_morphology — モルフォロジー演算

> はじめての方は [GUIDE.md](GUIDE.md) (やさしい解説) もどうぞ。

## 目的

- `cv2.erode` / `cv2.dilate` で基本演算を行う。
- `cv2.morphologyEx` で opening / closing / gradient / top hat / black hat を適用する。
- `cv2.getStructuringElement` で構造要素 (カーネル) の形を選ぶ。

## ポイント

- 入力は通常 **二値化済み (uint8)** の画像。グレースケールにも適用可。
- 構造要素の形: `MORPH_RECT` (四角) / `MORPH_CROSS` (十字) / `MORPH_ELLIPSE` (楕円)。
- `iterations` を増やすと効果が強くなる (erode/dilate)。
- `MORPH_GRADIENT` = dilation − erosion (輪郭抽出と同等)。

## 演算まとめ

| 演算 | 定義 | 効果 |
|------|------|------|
| erosion | min フィルタ | 前景縮小 |
| dilation | max フィルタ | 前景拡大 |
| opening | erosion→dilation | 細突起除去 |
| closing | dilation→erosion | 小穴埋め |
| gradient | dilation−erosion | 輪郭 |
| top hat | src−opening | 明るい小物体 |
| black hat | closing−src | 暗い小物体 |

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

gray / binary / erode / dilate / opening / closing / gradient / top hat / black hat の各画像が表示される。

## 参考

- [OpenCV: Morphological Transformations](https://docs.opencv.org/4.x/d9/d61/tutorial_py_morphological_ops.html)
