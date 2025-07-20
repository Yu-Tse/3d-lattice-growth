import numpy as np
from numba import cuda
from .constants import DIRECTIONS, FCC_PATTERN
from .kernels import update_grid
from .viz import plot_fcc, save_stats

def run_sim(grid_size=20, frames=50, gpu=True, seed=None, out_dir="output"):
    rng = np.random.default_rng(seed)
    cur = np.zeros((grid_size,)*3, dtype=np.int16)

    # Randomly Input 15 Points
    pts = rng.integers(1, grid_size, size=(15,3), dtype=np.int16)
    for x,y,z in pts: cur[x,y,z] = 1

    # GPU/CPU
    if gpu:
        d_cur = cuda.to_device(cur)
        d_nxt = cuda.device_array_like(cur)
        d_dir = cuda.to_device(DIRECTIONS)
        d_fcc = cuda.to_device(FCC_PATTERN)
        threads = (8,8,8)
        blocks  = tuple((grid_size+threads[i]-1)//threads[i] for i in range(3))

    defect_prob, grown_tot, defects = [], [], []

    for f in range(frames):
        defect_num = rng.integers(12, 15)

        if gpu:
            update_grid[blocks, threads](d_cur, d_nxt, d_dir, d_fcc, defect_num)
            d_cur, d_nxt = d_nxt, d_cur
            d_cur.copy_to_host(cur)
        else:
            raise NotImplementedError("CPU 跑太慢，僅示範 GPU")

        tot  = np.count_nonzero(cur)
        bad  = np.count_nonzero(cur == -1)
        prob = bad / tot if tot else 0

        defect_prob.append(prob)
        grown_tot.append(tot)
        defects.append(bad)

        plot_fcc(cur, f, out_dir)

    save_stats(defect_prob, grown_tot, defects, out_dir)
