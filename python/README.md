# Python 画像処理チュートリアル

C++ 版 ([../cpp](../cpp)) と同じセクション番号で、NumPy + OpenCV の Python 実装です。

## 構成

```
python/
├── README.md
├── requirements.txt
├── utils.py              # 共通ヘルパ (load_image / show_nb / show_cli)
├── 01_io/
│   ├── main.py           # CLI スクリプト
│   └── notebook.ipynb    # Jupyter Notebook
├── 02_color/
│   ├── main.py
│   └── notebook.ipynb
...
└── 14_dnn/
    ├── main.py
    ├── notebook.ipynb
    └── models/           # ONNX モデル置き場
```

## セクション一覧

| #   | テーマ                 | スクリプト                            | Notebook                                  |
| --- | ---------------------- | ------------------------------------- | ----------------------------------------- |
| 01  | 画像入出力・表示       | [01_io/main.py](01_io/main.py)         | [01_io/notebook.ipynb](01_io/notebook.ipynb) |
| 02  | 色空間変換             | [02_color/main.py](02_color/main.py)   | [02_color/notebook.ipynb](02_color/notebook.ipynb) |
| 03  | 幾何変換               | [03_geometry/main.py](03_geometry/main.py) | [03_geometry/notebook.ipynb](03_geometry/notebook.ipynb) |
| 04  | 閾値処理・二値化       | [04_threshold/main.py](04_threshold/main.py) | [04_threshold/notebook.ipynb](04_threshold/notebook.ipynb) |
| 05  | 平滑化フィルタ         | [05_smoothing/main.py](05_smoothing/main.py) | [05_smoothing/notebook.ipynb](05_smoothing/notebook.ipynb) |
| 06  | エッジ検出             | [06_edge/main.py](06_edge/main.py)     | [06_edge/notebook.ipynb](06_edge/notebook.ipynb) |
| 07  | モルフォロジー演算     | [07_morphology/main.py](07_morphology/main.py) | [07_morphology/notebook.ipynb](07_morphology/notebook.ipynb) |
| 08  | ヒストグラム           | [08_histogram/main.py](08_histogram/main.py) | [08_histogram/notebook.ipynb](08_histogram/notebook.ipynb) |
| 09  | 輪郭検出               | [09_contours/main.py](09_contours/main.py) | [09_contours/notebook.ipynb](09_contours/notebook.ipynb) |
| 10  | テンプレートマッチング | [10_template_matching/main.py](10_template_matching/main.py) | [10_template_matching/notebook.ipynb](10_template_matching/notebook.ipynb) |
| 11  | 特徴点検出・マッチング | [11_features/main.py](11_features/main.py) | [11_features/notebook.ipynb](11_features/notebook.ipynb) |
| 12  | 動画・カメラ入力       | [12_video/main.py](12_video/main.py)   | [12_video/notebook.ipynb](12_video/notebook.ipynb) |
| 13  | カメラキャリブレーション | [13_calibration/main.py](13_calibration/main.py) | [13_calibration/notebook.ipynb](13_calibration/notebook.ipynb) |
| 14  | DNN 推論               | [14_dnn/main.py](14_dnn/main.py)       | [14_dnn/notebook.ipynb](14_dnn/notebook.ipynb) |

## セットアップ

```bash
cd image_tutorial/python
pip install -r requirements.txt
```

## 実行方法

### CLI スクリプト

各 `main.py` は単独で実行できます。

```bash
# 基本 (lena.png が data/ に必要)
python 01_io/main.py ../data/lena.png

# 結果ウィンドウを出さずに保存のみ
python 01_io/main.py ../data/lena.png out.png --no-show

# 動画再生 (12_video)
python 12_video/main.py --video ../data/sample.mp4
python 12_video/main.py --camera 0          # カメラ
python 12_video/main.py --video ../data/sample.mp4 --no-show  # Notebook 風表示

# カメラキャリブレーション (画像ディレクトリ省略 → 合成チェスボードでデモ)
python 13_calibration/main.py

# DNN 推論 (モデル省略 → エッジデモにフォールバック)
python 14_dnn/main.py ../data/lena.png
```

### Jupyter Notebook

```bash
cd image_tutorial/python
jupyter notebook
```

各セクションの `notebook.ipynb` を開いてセルを上から順に実行してください。

## 共通ヘルパ (utils.py)

| 関数 | 説明 |
|------|------|
| `load_image(path, flags)` | 読み込み失敗時に分かりやすいエラーで終了 |
| `show_nb(pairs, cols)` | Notebook 用 matplotlib 表示 |
| `show_cli(pairs)` | CLI 用 cv2.imshow 表示 (ESC/q で閉じる) |
| `show(pairs, cols)` | 環境を自動判定して適切な方を呼ぶ |
| `bgr2rgb(img)` | BGR → RGB 変換 (matplotlib に渡す前に使う) |

## 14_dnn モデルの準備

```bash
pip install ultralytics
yolo export model=yolov8n.pt format=onnx
mkdir -p python/14_dnn/models
mv yolov8n.onnx python/14_dnn/models/
```

## サンプルデータ

`../data/` に画像・動画を配置してください。詳細は [../data/README.md](../data/README.md) を参照。
