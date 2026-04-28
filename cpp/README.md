# C++ 画像処理チュートリアル

OpenCV 4 + 一部 Eigen ベースの C++ チュートリアルです。各セクションは独立した CMake プロジェクトで、ルートの `CMakeLists.txt` でまとめてビルドできます。

## ビルド

```bash
cd image_tutorial/cpp
cmake -S . -B build
cmake --build build -j
```

特定のセクションだけビルドする場合:

```bash
cmake -S . -B build -DBUILD_SECTIONS="01_io;05_smoothing"
cmake --build build -j
```

## 実行

`build/<section>/<section>` が生成されます。サンプル画像は `image_tutorial/data/` に配置してください ([../data/README.md](../data/README.md))。

```bash
./build/01_io/01_io ../data/lena.png
./build/05_smoothing/05_smoothing ../data/lena.png
```

各セクションの詳細・引数は各 `README.md` を参照してください。

## セクション

各セクションには技術リファレンスの `README.md` に加えて、画像処理が初めての方向けに **やさしい解説** `GUIDE.md` を併設しています。まずは `GUIDE.md` を読み、それから `README.md` の手順でビルド・実行すると分かりやすいです。

| #   | dir                      | 概要                           |
| --- | ------------------------ | ------------------------------ |
| 01  | [01_io](01_io)           | imread/imwrite/imshow          |
| 02  | [02_color](02_color)     | 色空間変換 (BGR/HSV/Gray)      |
| 03  | [03_geometry](03_geometry) | 幾何変換 (resize/affine/perspective) |
| 04  | [04_threshold](04_threshold) | 閾値処理・二値化              |
| 05  | [05_smoothing](05_smoothing) | 平滑化フィルタ                |
| 06  | [06_edge](06_edge)       | エッジ検出 (Sobel/Canny)       |
| 07  | [07_morphology](07_morphology) | モルフォロジー演算           |
| 08  | [08_histogram](08_histogram) | ヒストグラム・等化            |
| 09  | [09_contours](09_contours) | 輪郭検出・形状特徴            |
| 10  | [10_template_matching](10_template_matching) | テンプレートマッチング |
| 11  | [11_features](11_features) | ORB/AKAZE + マッチング        |
| 12  | [12_video](12_video)     | 動画・カメラ入力               |
| 13  | [13_calibration](13_calibration) | カメラキャリブレーション      |
| 14  | [14_dnn](14_dnn)         | DNN 推論 (ONNX)                |

## 共通ヘルパ

`common/utils.hpp` に画像ロードとウィンドウ表示のヘルパを置いています。各セクションから `#include "common/utils.hpp"` で利用します。

## コードスタイル

`.clang-format` (LLVM ベース) を同梱しています。

```bash
clang-format -i $(find . -name '*.cpp' -o -name '*.hpp')
```
