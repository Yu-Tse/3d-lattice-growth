import sys, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[1]  # 回到專案根
sys.path.insert(0, str(ROOT))
import numpy as np
import pytest

try:
    from numba import cuda
    GPU_AVAILABLE = cuda.is_available()
except Exception:
    GPU_AVAILABLE = False

from src.constants import DIRECTIONS, FCC_PATTERN
from src.kernels import update_grid


# ---------- Utilities ---------- #
def update_grid_cpu(cur, directions, pattern, defect_num):
    """簡化版 CPU 參考實作（僅小網格用於測試）。"""
    nxt = cur.copy()
    N = cur.shape[0]

    def in_range(a):  # 巢狀函式做邊界檢查
        return 0 <= a < N

    for x in range(N):
        for y in range(N):
            for z in range(N):
                # ① 判斷連續直線
                straight = False
                for dx, dy, dz in directions:
                    cnt = 1
                    for step in range(-defect_num // 2 - 1, defect_num // 2 + 1):
                        xi, yi, zi = x + dx * step, y + dy * step, z + dz * step
                        if in_range(xi) and in_range(yi) and in_range(zi):
                            v = cur[xi, yi, zi]
                            if v in (1, 2):
                                cnt += 1
                            else:
                                break
                        else:
                            break
                    if cnt >= defect_num:
                        straight = True
                        break

                # ② 最近鄰生長數
                grow_cnt = 0
                for px, py, pz in pattern:
                    nx, ny, nz = x + px, y + py, z + pz
                    if in_range(nx) and in_range(ny) and in_range(nz):
                        if cur[nx, ny, nz] == 1:
                            grow_cnt += 1

                # ③ 狀態轉移（與 kernels.py 一致）
                if straight:
                    nxt[x, y, z] = 2
                else:
                    v = cur[x, y, z]
                    if v == 1:
                        nxt[x, y, z] = -1 if grow_cnt >= 2 else 1
                    elif v == 0 and grow_cnt >= 1:
                        nxt[x, y, z] = 1
                    elif v == -1 and grow_cnt >= 4:
                        nxt[x, y, z] = 1
                    elif v == 2:
                        nxt[x, y, z] = 2
    return nxt


def random_grid(seed=0, size=6, density=0.05):
    """產生稀疏隨機初始網格。"""
    rng = np.random.default_rng(seed)
    g = np.zeros((size, size, size), dtype=np.int16)
    mask = rng.random(g.shape) < density
    g[mask] = 1
    return g


# ---------- Test Cases ---------- #
@pytest.mark.parametrize("defect_num", [12, 13])
def test_kernel_matches_cpu(defect_num):
    grid_size = 6
    cur = random_grid(seed=42, size=grid_size)

    # --- CPU 參考結果 --- #
    ref_next = update_grid_cpu(cur, DIRECTIONS, FCC_PATTERN, defect_num)

    # --- CUDA kernel （若有 GPU；否則跳過）--- #
    if GPU_AVAILABLE:
        d_cur = cuda.to_device(cur)
        d_nxt = cuda.device_array_like(cur)
        threads = (4, 4, 4)
        blocks = tuple((grid_size + t - 1) // t for t in threads)
        d_dir = cuda.to_device(DIRECTIONS)
        d_pat = cuda.to_device(FCC_PATTERN)

        update_grid[blocks, threads](d_cur, d_nxt, d_dir, d_pat, defect_num)
        nxt = d_nxt.copy_to_host()
        # 和 CPU 參考比對
        assert np.array_equal(nxt, ref_next)
    else:
        pytest.skip("CUDA not available; only CPU logic verified")

    # 額外簡單性質檢查（總 cell 數不變或增加）
    assert np.count_nonzero(ref_next) >= np.count_nonzero(cur)
