#!/usr/bin/env bash
# OpenCV 公式リポジトリからサンプルデータを取得し data/ に配置する補助スクリプト。
# 任意実行。/tmp 以外には書き込みません。
set -euo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"
SRC=/tmp/opencv-src

if [ ! -d "$SRC" ]; then
    echo "[fetch] cloning OpenCV samples to $SRC ..."
    git clone --depth 1 https://github.com/opencv/opencv.git "$SRC"
else
    echo "[fetch] reusing existing $SRC"
fi

cp "$SRC/samples/data/lena.jpg"        "$HERE/lena.png"
cp "$SRC/samples/data/building.jpg"    "$HERE/building.jpg"
cp "$SRC/samples/data/box.png"         "$HERE/template.png"
cp "$SRC/samples/data/box_in_scene.png" "$HERE/scene.png"
cp "$SRC/samples/data/vtest.avi"       "$HERE/video.mp4"
cp "$SRC/samples/data/HappyFish.jpg"   "$HERE/coins.png" 2>/dev/null || true

# 特徴点マッチング用ペア
cp "$SRC/samples/data/graf1.png" "$HERE/book1.jpg" 2>/dev/null || true
cp "$SRC/samples/data/graf3.png" "$HERE/book2.jpg" 2>/dev/null || true

# チェスボード画像
mkdir -p "$HERE/chessboard"
for i in $(seq -w 1 14); do
    f="$SRC/samples/data/left${i}.jpg"
    [ -f "$f" ] && cp "$f" "$HERE/chessboard/left${i}.jpg" || true
done

echo "[fetch] done. files placed under $HERE"
ls -1 "$HERE"
