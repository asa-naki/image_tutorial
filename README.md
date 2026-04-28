# image_tutorial

OpenCV を中心とした画像処理チュートリアル集です。C++ 版を `cpp/` に、Python 版  を `python/` に置き、セクション番号 (`01_io` 〜 `14_dnn`) を両言語で揃えます。

## 構成

```
image_tutorial/
├── README.md            # このファイル
├── data/                # サンプル画像/動画/モデル置き場 (各自配置)
├── cpp/                 # C++ チュートリアル (OpenCV 4 + 一部 Eigen)
└── python/              # Python チュートリアル (プレースホルダ)
```

## セクション一覧

| #   | テーマ                       | C++                                                              | Python |
| --- | ---------------------------- | ---------------------------------------------------------------- | ------ |
| 01  | 画像入出力・表示             | [cpp/01_io](cpp/01_io)                                           | [python/01_io](python/01_io) |
| 02  | 色空間変換                   | [cpp/02_color](cpp/02_color)                                     | [python/02_color](python/02_color) |
| 03  | 幾何変換                     | [cpp/03_geometry](cpp/03_geometry)                               | [python/03_geometry](python/03_geometry) |
| 04  | 閾値処理・二値化             | [cpp/04_threshold](cpp/04_threshold)                             | [python/04_threshold](python/04_threshold) |
| 05  | 平滑化フィルタ               | [cpp/05_smoothing](cpp/05_smoothing)                             | [python/05_smoothing](python/05_smoothing) |
| 06  | エッジ検出                   | [cpp/06_edge](cpp/06_edge)                                       | [python/06_edge](python/06_edge) |
| 07  | モルフォロジー演算           | [cpp/07_morphology](cpp/07_morphology)                           | [python/07_morphology](python/07_morphology) |
| 08  | ヒストグラム                 | [cpp/08_histogram](cpp/08_histogram)                             | [python/08_histogram](python/08_histogram) |
| 09  | 輪郭検出                     | [cpp/09_contours](cpp/09_contours)                               | [python/09_contours](python/09_contours) |
| 10  | テンプレートマッチング       | [cpp/10_template_matching](cpp/10_template_matching)             | [python/10_template_matching](python/10_template_matching) |
| 11  | 特徴点検出・マッチング       | [cpp/11_features](cpp/11_features)                               | [python/11_features](python/11_features) |
| 12  | 動画・カメラ入力             | [cpp/12_video](cpp/12_video)                                     | [python/12_video](python/12_video) |
| 13  | カメラキャリブレーション     | [cpp/13_calibration](cpp/13_calibration)                         | [python/13_calibration](python/13_calibration) |
| 14  | DNN 推論                     | [cpp/14_dnn](cpp/14_dnn)                                         | [python/14_dnn](python/14_dnn) |

## 前提環境

共通要件:

- OpenCV ≥ 4.5 (contrib 同梱で SIFT も利用可)
- Eigen3 (`03_geometry`, `13_calibration` で使用)
- CMake ≥ 3.16
- C++17 対応コンパイラ (GCC 9+ / Clang 10+ / MSVC 2019+)
- Python 3.9+ (Python 版を使う場合)

### Ubuntu (22.04 / 24.04)

#### 1. システムパッケージのインストール

```bash
sudo apt update
sudo apt install -y build-essential cmake pkg-config git \
    libopencv-dev libopencv-contrib-dev libeigen3-dev \
    python3 python3-pip python3-venv
```

apt 版 OpenCV のバージョンを確認:

```bash
pkg-config --modversion opencv4
```

> Ubuntu 22.04 の apt は OpenCV 4.5 系、24.04 は 4.6 系です。より新しい版や CUDA / 独自モジュールが必要な場合はソースビルドを検討してください (例: `git clone https://github.com/opencv/opencv` と `opencv_contrib` を取得し `-DOPENCV_EXTRA_MODULES_PATH=...` でビルド)。

#### 2. リポジトリ取得とビルド (C++)

```bash
git clone https://github.com/asa-naki/image_tutorial.git
cd image_tutorial/cpp
cmake -S . -B build
cmake --build build -j$(nproc)
./build/01_io/01_io ../data/lena.png
```

#### 3. Python 環境 (任意)

```bash
cd image_tutorial/python
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python 01_io/main.py ../data/lena.png
```

### Windows 10 / 11

ここでは「Visual Studio + vcpkg」を推奨ルートとして案内します。WSL2 を使う場合は Ubuntu 手順がそのまま利用できます。

#### 1. 必要ツールのインストール

[winget](https://learn.microsoft.com/windows/package-manager/winget/) で一括導入できます (PowerShell を管理者で起動):

```powershell
winget install --id Git.Git -e
winget install --id Kitware.CMake -e
winget install --id Microsoft.VisualStudio.2022.Community -e --override "--add Microsoft.VisualStudio.Workload.NativeDesktop --includeRecommended"
winget install --id Python.Python.3.12 -e
```

Visual Studio Installer から「C++ によるデスクトップ開発」ワークロードが入っていることを確認してください (MSVC, Windows SDK, CMake が含まれます)。

#### 2. vcpkg で OpenCV / Eigen を導入

```powershell
cd C:\dev
git clone https://github.com/microsoft/vcpkg.git
cd vcpkg
.\bootstrap-vcpkg.bat
.\vcpkg integrate install
.\vcpkg install opencv4[contrib]:x64-windows eigen3:x64-windows
```

> `opencv4[contrib]` のビルドには時間がかかります。SIFT/特徴量モジュールが不要な場合は `opencv4:x64-windows` でも構いません。

#### 3. リポジトリ取得とビルド (C++)

「Developer PowerShell for VS 2022」を開き、vcpkg のツールチェーンを指定して構成します:

```powershell
git clone <this-repo-url> image_tutorial
cd image_tutorial\cpp
cmake -S . -B build `
  -DCMAKE_TOOLCHAIN_FILE=C:\dev\vcpkg\scripts\buildsystems\vcpkg.cmake `
  -DVCPKG_TARGET_TRIPLET=x64-windows
cmake --build build --config Release -j
.\build\01_io\Release\01_io.exe ..\data\lena.png
```

> 実行時に `opencv_world*.dll` が見つからないと言われた場合は、`C:\dev\vcpkg\installed\x64-windows\bin` を PATH に追加するか、`vcpkg integrate install` を実行してください。

#### 4. Python 環境 (任意)

```powershell
cd image_tutorial\python
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python 01_io\main.py ..\data\lena.png
```

> PowerShell でスクリプト実行が拒否される場合は `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` を一度実行してください。

### macOS (参考)

```bash
brew install cmake opencv eigen python@3.12
```

以降は Ubuntu と同じ手順でビルドできます。

## クイックスタート (C++)

```bash
cd image_tutorial/cpp
cmake -S . -B build
cmake --build build -j
# 個別実行例
./build/01_io/01_io ../data/lena.png
```

詳細は [cpp/README.md](cpp/README.md) を参照してください。

## クイックスタート (Python)

```bash
cd image_tutorial/python
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
# 個別実行例
python 01_io/main.py ../data/lena.png
```

詳細は [python/README.md](python/README.md) を参照してください。

## サンプルデータ

`data/` に画像・動画・モデルを配置します。推奨ファイル名と入手案内は [data/README.md](data/README.md) にまとめています。

## ライセンス

[LICENSE](LICENSE) を参照してください。サンプル画像/モデルは利用者側で各々のライセンスに従って取得してください。
