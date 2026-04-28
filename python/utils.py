"""共通ユーティリティ — 各セクションの main.py / notebook から import して使う。"""
import sys
import cv2
import numpy as np
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"


def load_image(path, flags=cv2.IMREAD_COLOR):
    img = cv2.imread(str(path), flags)
    if img is None:
        print(f"[error] 画像を読み込めません: {path}")
        print("        image_tutorial/data/ にサンプルを配置してください (data/README.md 参照)")
        sys.exit(1)
    return img


def bgr2rgb(img):
    return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)


def show_cli(pairs):
    """CLI 用: 複数画像を名前付きウィンドウに表示し ESC/q を待つ。"""
    for title, img in pairs:
        if img is not None:
            cv2.imshow(title, img)
    print("[info] ESC または 'q' でウィンドウを閉じます")
    while True:
        key = cv2.waitKey(0) & 0xFF
        if key in (27, ord('q')):
            break
    cv2.destroyAllWindows()


def show_nb(pairs, cols=3, cell_size=4):
    """Jupyter Notebook 用: matplotlib で画像をインライン表示する。"""
    import matplotlib.pyplot as plt
    n = len(pairs)
    c = min(cols, n)
    r = (n + c - 1) // c
    fig, axes = plt.subplots(r, c, figsize=(cell_size * c, cell_size * r))
    axes = np.array(axes).reshape(-1)
    for i, (title, img) in enumerate(pairs):
        ax = axes[i]
        if img is None:
            ax.set_visible(False)
            continue
        if img.ndim == 2 or (img.ndim == 3 and img.shape[2] == 1):
            ax.imshow(img.squeeze(), cmap='gray', vmin=0, vmax=255)
        else:
            ax.imshow(bgr2rgb(img))
        ax.set_title(title, fontsize=10)
        ax.axis('off')
    for i in range(n, len(axes)):
        axes[i].set_visible(False)
    plt.tight_layout()
    plt.show()


def is_notebook():
    """Jupyter 環境かどうかを判定する。"""
    try:
        shell = get_ipython().__class__.__name__  # noqa: F821
        return shell in ('ZMQInteractiveShell', 'Shell')
    except NameError:
        return False


def show(pairs, cols=3):
    """環境を自動判定して適切な表示関数を呼ぶ。"""
    if is_notebook():
        show_nb(pairs, cols=cols)
    else:
        show_cli(pairs)
