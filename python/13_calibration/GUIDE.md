# やさしい解説: カメラキャリブレーション (Python 版)

## カメラには「クセ」がある

スマホや Web カメラのレンズには **個体差や歪み** があります。とくに広角レンズで撮ると、画像の端のほうが **ゆるく曲がって** 見えます (魚眼っぽい感じ)。

この「カメラのクセ」を **数字で測ってあげる** のが、カメラキャリブレーション (校正) です。

## 何を測るの？

ざっくり 2 つ。

- **内部パラメータ (カメラ行列 K)**: 焦点距離や画像の中心の位置
- **歪み係数 (dist)**: レンズの曲がり具合

```
K = [[fx,  0, cx],
     [ 0, fy, cy],
     [ 0,  0,  1]]
dist = [k1, k2, p1, p2, k3]
```

これらが分かれば、画像の **歪みを補正**したり **3D 位置を計算** することができます。

## なぜ「チェスボード」なの？

校正にはふつう白黒のチェス盤の写真を使います。マスのカドの位置が **正確に分かっている** ので、「実際の格子の位置」と「画像上で見える位置」のズレからカメラのクセを計算できます。

## Python での流れ

```python
# 1) 3D 世界座標 (チェスボードの格子点)
objp = np.zeros((cols * rows, 3), np.float32)
objp[:, :2] = np.mgrid[0:cols, 0:rows].T.reshape(-1, 2) * square_m

# 2) コーナー検出
ret, corners = cv2.findChessboardCorners(gray, (cols, rows), None)
if ret:
    # サブピクセル精度で精密化
    corners = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)

# 3) キャリブレーション
rms, K, dist, rvecs, tvecs = cv2.calibrateCamera(
    obj_points, img_points, img_size, None, None)

# 4) 歪み補正
undistorted = cv2.undistort(img, K, dist)
```

## NumPy で結果を保存・読み込みする

```python
np.savez("camera_matrix.npz", K=K, dist=dist)

data = np.load("camera_matrix.npz")
K    = data["K"]
dist = data["dist"]
```

`np.savez` を使うと複数の NumPy 配列を 1 ファイルにまとめて保存できます。

## チェスボードがなくても試せる

このセクションの `main.py` には **合成チェスボード画像を自動生成する** 機能があります。引数を省略するだけでデモが動くので、実際のカメラがなくてもキャリブレーションの流れを体験できます。

## 「再投影誤差」って何？

校正の精度を測る数字。**測ったカメラ行列で格子点の位置を再計算したとき、もとの観測点とどれだけズレているか** の平均。**1 ピクセル以下** に収まれば良い結果です。

## 一言まとめ

カメラキャリブレーションは **「カメラの個性 (行列 K と歪み係数) を NumPy 配列として測る作業」**。結果を `np.savez` で保存しておけば、後のプログラムでも再利用できます。
