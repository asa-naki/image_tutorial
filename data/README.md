# data/

各セクションが参照するサンプル画像・動画・モデルを配置するディレクトリです。リポジトリには同梱せず、利用者が用意してください。

## 推奨ファイル名

| ファイル                      | 用途                                  | セクション |
| ----------------------------- | ------------------------------------- | ---------- |
| `lena.png`                    | 一般的なテスト画像 (カラー)           | 01-08      |
| `building.jpg`                | エッジ・特徴点向け (構造物)           | 06,11      |
| `coins.png` (グレースケール) | 輪郭・モルフォロジー向け              | 07,09      |
| `template.png`                | テンプレートマッチング用テンプレート  | 10         |
| `scene.png`                   | テンプレートマッチング用検索対象画像  | 10         |
| `book1.jpg`, `book2.jpg`      | 特徴点マッチングのペア                | 11         |
| `video.mp4`                   | 動画読み込み・背景差分用              | 12         |
| `chessboard/*.jpg`            | キャリブレーション用チェスボード画像  | 13         |
| `model.onnx`, `labels.txt`    | DNN 推論用モデルとラベル              | 14         |

## 入手案内

OpenCV 公式のサンプルデータが手早いです。

```bash
# OpenCV 公式 sample/data の例 (lena.jpg は OpenCV 同梱)
git clone --depth 1 https://github.com/opencv/opencv.git /tmp/opencv-src
cp /tmp/opencv-src/samples/data/lena.jpg ./lena.png  # 拡張子合わせは任意
cp /tmp/opencv-src/samples/data/building.jpg ./
cp /tmp/opencv-src/samples/data/box.png ./template.png
cp /tmp/opencv-src/samples/data/box_in_scene.png ./scene.png
cp /tmp/opencv-src/samples/data/vtest.avi ./video.mp4  # コンテナ違うが imread/VideoCapture は対応
```

チェスボード画像 (`left01.jpg` 〜 `left14.jpg`) も `samples/data/` にあります。`data/chessboard/` に配置してください。

DNN モデルは [14_dnn/README.md](../cpp/14_dnn/README.md) を参照してください。

## 補助スクリプト

`fetch_samples.sh` を任意実行で起動すると、上記の主要画像のみコピーします。

```bash
bash fetch_samples.sh
```

スクリプトは `git clone` で OpenCV のソースを `/tmp` に取得し、必要ファイルだけ `data/` にコピーします。利用者環境を変更しないよう、`/tmp` 以外には書き込みません。
