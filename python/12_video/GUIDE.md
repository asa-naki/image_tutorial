# やさしい解説: 動画・カメラ入力 (Python 版)

## 動画は「画像のつながり」

動画は **パラパラ漫画** と同じで、1 秒間に何十枚もの絵 (= フレーム) を順番に見せているだけです。1 枚 1 枚は、これまで扱ってきた **ふつうの画像 (NumPy 配列)** と同じです。

「30 fps」と書いてあれば、1 秒に 30 枚のフレームが流れているという意味です。

## やることはシンプル

```python
cap = cv2.VideoCapture("sample.mp4")   # または cv2.VideoCapture(0) でカメラ

while True:
    ret, frame = cap.read()   # 1 フレーム取得
    if not ret:
        break
    # frame は普通の NumPy 配列 (BGR)
    processed = my_function(frame)
    cv2.imshow("result", processed)
    if cv2.waitKey(1) & 0xFF in (27, ord('q')):
        break

cap.release()
cv2.destroyAllWindows()
```

## Jupyter Notebook での注意

`cv2.imshow` のウィンドウは Jupyter Notebook では正しく動かないことがあります。Notebook ではフレームを静止画として取得し、`matplotlib` で表示するのがおすすめです。

```python
cap.set(cv2.CAP_PROP_POS_FRAMES, 100)   # 100 フレーム目に移動
ret, frame = cap.read()
plt.imshow(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
plt.show()
```

このチュートリアルの `main.py` では `--no-show` フラグを使うと、フレームを複数取得して matplotlib で表示する Notebook モードに切り替わります。

## 動画ファイルの情報を取得する

```python
cap = cv2.VideoCapture("video.mp4")
total  = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
fps    = cap.get(cv2.CAP_PROP_FPS)
width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
```

## 処理結果を動画に保存する

```python
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
writer = cv2.VideoWriter("out.mp4", fourcc, fps, (width, height))
writer.write(processed_frame)
writer.release()
```

コーデック (`mp4v`, `XVID` など) は OS によって使えるものが違います。うまくいかないときはコーデックを変えてみてください。

## オプティカルフロー (動くものを追う)

```python
p0 = cv2.goodFeaturesToTrack(gray1, 100, 0.3, 7)
p1, status, _ = cv2.calcOpticalFlowPyrLK(gray1, gray2, p0, None)
# status が 1 の点だけが追跡成功
```

Lucas-Kanade 法で特徴点を追いかけることで、物体の動きをベクトルとして得られます。

## 一言まとめ

動画処理は **「ふつうの画像処理を 1 フレームずつ繰り返す」** だけ。Notebook では `CAP_PROP_POS_FRAMES` で飛び飛びにフレームを取得して matplotlib で確認するのがコツです。
