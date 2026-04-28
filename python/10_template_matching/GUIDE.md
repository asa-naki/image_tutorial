# やさしい解説: テンプレートマッチング (Python 版)

## どんな処理？

「探したい絵 (= **テンプレート**)」を用意して、それを **大きい画像の上で少しずつスライドさせ**、いちばん **似ている場所** を見つける方法です。

身近な例: 「ウォーリーをさがせ」のように、画面のあちこちにテンプレを当てて、ぴったり重なる場所を探していくイメージ。

## 「似ている」をどう測るの？

各位置でテンプレと画像を重ね合わせて色の差を比べることで点数 (スコア) を計算します。

| メソッド | スコアが最良のとき | 特徴 |
|---------|-------------------|------|
| `TM_SQDIFF` | 最小 | シンプルな差の二乗 |
| `TM_SQDIFF_NORMED` | 最小 | 正規化あり |
| `TM_CCORR_NORMED` | 最大 | 正規化相互相関 |
| `TM_CCOEFF_NORMED` | 最大 | **正規化相関係数。明るさの違いに強い。推奨** |

## Python での書き方と注意点

```python
result = cv2.matchTemplate(gray_src, gray_tmpl, cv2.TM_CCOEFF_NORMED)
min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

# TM_CCOEFF_NORMED は最大値が最良
top_left = max_loc
bottom_right = (top_left[0] + tw, top_left[1] + th)
cv2.rectangle(src, top_left, bottom_right, (0, 0, 255), 3)
```

### スコアマップは NumPy 配列

`matchTemplate` の戻り値 `result` は `float32` の NumPy 配列です。matplotlib の `imshow` でそのまま可視化できます。

```python
import matplotlib.pyplot as plt
plt.imshow(result, cmap='hot')
plt.colorbar()
plt.show()
```

ヒートマップにすると「どこで最もよくマッチしているか」が視覚的にわかります。

## 弱点と対策

テンプレートマッチングは **サイズや向きが違うと急に当たらなく** なります。

- **マルチスケール**: テンプレをループで拡大・縮小して複数回試す
- **特徴点マッチング** (次のセクション): 回転・スケール変化にも強い

## 使い道の例

- ゲーム画面で特定のアイコンを探す自動操作
- 工場のラインで基準マークの位置を測る
- 印刷物の中からロゴを探す

## 一言まとめ

テンプレートマッチングは **「お手本をすべらせて、いちばん似てる場所を探す」** 処理。スコアマップが NumPy 配列なので matplotlib で可視化しながら閾値を調整しやすいのが Python の強みです。
