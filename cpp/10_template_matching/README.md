# 10_template_matching — テンプレートマッチング

> はじめての方は [GUIDE.md](GUIDE.md) (中学生向けやさしい解説) もどうぞ。

## 目的

- `cv::matchTemplate` で最良一致位置を求める。
- スケール違いに対応するため、テンプレートサイズを変えてマルチスケール探索する。

## ポイント

- メソッドは複数 (`TM_SQDIFF`, `TM_CCORR_NORMED`, `TM_CCOEFF_NORMED` など)。NCC は照度変化に比較的強い。
- `TM_SQDIFF` は最小、それ以外は最大が最良。
- 結果マップは入力画像とテンプレートのサイズ差分: `(W - w + 1) x (H - h + 1)`。

## ビルド・実行

```bash
cmake --build build -j 10_template_matching
./build/10_template_matching/10_template_matching ../data/scene.png ../data/template.png
```

## 期待される出力

- scene / template / スコアマップ / single-scale 結果 / multi-scale 結果 の 5 ウィンドウ。
- 標準出力に NCC 値とマルチスケールの最良スケール。

## 参考

- [OpenCV: Template Matching](https://docs.opencv.org/4.x/d4/dc6/tutorial_py_template_matching.html)
