# image_tutorial

OpenCV を中心とした画像処理チュートリアル集です。C++ 版を `cpp/` に、Python 版 (後日追加予定) を `python/` に置き、セクション番号 (`01_io` 〜 `14_dnn`) を両言語で揃えます。

## 構成

```
image_tutorial/
├── README.md            # このファイル
├── data/                # サンプル画像/動画/モデル置き場 (各自配置)
├── cpp/                 # C++ チュートリアル (OpenCV 4 + 一部 Eigen)
└── python/              # Python チュートリアル (プレースホルダ)
```

## セクション一覧

| #   | テーマ                       | C++                                                              | Python (予定) |
| --- | ---------------------------- | ---------------------------------------------------------------- | ------------- |
| 01  | 画像入出力・表示             | [cpp/01_io](cpp/01_io)                                           | python/01_io  |
| 02  | 色空間変換                   | [cpp/02_color](cpp/02_color)                                     | python/02_color |
| 03  | 幾何変換                     | [cpp/03_geometry](cpp/03_geometry)                               | python/03_geometry |
| 04  | 閾値処理・二値化             | [cpp/04_threshold](cpp/04_threshold)                             | python/04_threshold |
| 05  | 平滑化フィルタ               | [cpp/05_smoothing](cpp/05_smoothing)                             | python/05_smoothing |
| 06  | エッジ検出                   | [cpp/06_edge](cpp/06_edge)                                       | python/06_edge |
| 07  | モルフォロジー演算           | [cpp/07_morphology](cpp/07_morphology)                           | python/07_morphology |
| 08  | ヒストグラム                 | [cpp/08_histogram](cpp/08_histogram)                             | python/08_histogram |
| 09  | 輪郭検出                     | [cpp/09_contours](cpp/09_contours)                               | python/09_contours |
| 10  | テンプレートマッチング       | [cpp/10_template_matching](cpp/10_template_matching)             | python/10_template_matching |
| 11  | 特徴点検出・マッチング       | [cpp/11_features](cpp/11_features)                               | python/11_features |
| 12  | 動画・カメラ入力             | [cpp/12_video](cpp/12_video)                                     | python/12_video |
| 13  | カメラキャリブレーション     | [cpp/13_calibration](cpp/13_calibration)                         | python/13_calibration |
| 14  | DNN 推論                     | [cpp/14_dnn](cpp/14_dnn)                                         | python/14_dnn |

## 前提環境 (Ubuntu 24.04 想定)

```bash
sudo apt update
sudo apt install -y build-essential cmake pkg-config \
    libopencv-dev libopencv-contrib-dev libeigen3-dev
```

- OpenCV ≥ 4.5 (contrib 同梱で SIFT も利用可)
- Eigen3 (`03_geometry`, `13_calibration` で使用)
- CMake ≥ 3.16

## クイックスタート (C++)

```bash
cd image_tutorial/cpp
cmake -S . -B build
cmake --build build -j
# 個別実行例
./build/01_io/01_io ../data/lena.png
```

詳細は [cpp/README.md](cpp/README.md) を参照してください。

## サンプルデータ

`data/` に画像・動画・モデルを配置します。推奨ファイル名と入手案内は [data/README.md](data/README.md) にまとめています。

## ライセンス

[LICENSE](LICENSE) を参照してください。サンプル画像/モデルは利用者側で各々のライセンスに従って取得してください。
