# 06_edge — エッジ検出

> はじめての方は [GUIDE.md](GUIDE.md) (やさしい解説) もどうぞ。

## 目的

- `cv2.Sobel` / `cv2.Scharr` で勾配を求める。
- `cv2.Laplacian` で 2 次微分エッジを検出する。
- `cv2.Canny` で Non-Maximum Suppression + ヒステリシス閾値による高精度エッジを得る。

## ポイント

- Sobel / Laplacian の出力は **負の値を含む**。`cv2.CV_64F` で受け取り `cv2.convertScaleAbs` で `uint8` に変換する。
- 勾配の大きさ: `cv2.magnitude(Gx, Gy)` → `np.clip(..., 0, 255).astype(np.uint8)`。
- Canny は入力に **グレースケール + ガウシアンブラー** を先に適用するとノイズが減る。
- `threshold2 ≈ threshold1 × 2〜3` が目安。

## Canny のアルゴリズム概要

1. ガウシアンブラーでノイズ除去
2. Sobel で勾配の大きさ・方向を計算
3. Non-Maximum Suppression (勾配方向で最大値だけ残す)
4. ヒステリシス閾値で弱いエッジの接続を判断

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

gray / Sobel X / Sobel Y / Sobel magnitude / Scharr magnitude / Laplacian / Canny (2種) の各画像が表示される。

## 参考

- [OpenCV: Canny Edge Detector](https://docs.opencv.org/4.x/da/d22/tutorial_py_canny.html)
- [OpenCV: Sobel Derivatives](https://docs.opencv.org/4.x/d2/d2c/tutorial_sobel_derivatives.html)
