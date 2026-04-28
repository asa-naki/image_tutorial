# やさしい解説: DNN 推論 (Python 版)

## DNN って何？

**Deep Neural Network (ディープ・ニューラル・ネットワーク)** の略。ものすごくざっくり言えば、**たくさんの画像を見せて学習させた "脳のミニ模型"** のことです。学習が終わると、新しい画像を見せて「これはネコです」「ここに人がいます」のように **答えを推測** してくれます。

## 「学習」と「推論」は別物

- **学習 (training)**: データを使って模型を作る。とても重い作業。
- **推論 (inference)**: できあがった模型を **使うだけ**。このセクションはここだけ扱います。

学習済みモデルは研究者がネット上に公開してくれているものを **借りるだけで OK** です。

## ONNX ってなに？

「**学習済みモデルの共通フォーマット**」です。PyTorch や TensorFlow などの学習ツールが ONNX 形式に書き出し、OpenCV はそれをそのまま読み込んで実行できます。

## Python での推論の流れ

```python
# 1) モデルを読み込む
net = cv2.dnn.readNetFromONNX("yolov8n.onnx")

# 2) 前処理: 画像をモデルが期待する形に整える
blob = cv2.dnn.blobFromImage(img, 1/255.0, (640, 640), swapRB=True, crop=False)
# blob.shape = (1, 3, 640, 640)  ← (バッチ, チャネル, 高さ, 幅)

# 3) 推論実行
net.setInput(blob)
outputs = net.forward()  # NumPy 配列が返る

# 4) 後処理: 結果を人間が読める形に直す
# (検出ボックスの座標変換、NMS など)
```

### `blobFromImage` のパラメータ

| パラメータ | 意味 |
|-----------|------|
| `scalefactor=1/255.0` | ピクセル値を 0〜1 に正規化 |
| `size=(640, 640)` | モデルの入力サイズにリサイズ |
| `swapRB=True` | BGR → RGB に変換 |

## 後処理の NumPy 操作

YOLOv8 の出力は `(1, 84, 8400)` という形の NumPy 配列です。

```python
out = outputs[0].T   # (8400, 84) に転置
# 列 0〜3: 中心座標 (cx, cy) と幅・高さ (bw, bh)
# 列 4〜83: 80クラスの信頼度スコア

cls_id = np.argmax(out[:, 4:], axis=1)     # 各候補のクラス
conf   = out[np.arange(len(out)), 4+cls_id]  # 信頼度
```

出力の `shape` を確認してから `reshape` や `T` (転置) で整形するのが後処理の基本です。

## NMS (重複検出の除去)

複数の枠が同じ物体を指してしまうとき、スコアの高い枠だけを残します。

```python
indices = cv2.dnn.NMSBoxes(boxes, scores, score_threshold=0.4, nms_threshold=0.5)
```

## 一言まとめ

DNN 推論は **「学習済みモデルを OpenCV から呼び出して使う」** こと。`blobFromImage` で前処理し、`forward()` で推論し、NumPy で後処理する — この 3 ステップが基本の型です。
