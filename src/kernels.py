from numba import cuda
import numpy as np

@cuda.jit
def update_grid(cur, nxt, directions, pattern, defect_num):
    x, y, z = cuda.grid(3)
    if x >= cur.shape[0] or y >= cur.shape[1] or z >= cur.shape[2]:
        return

    # Is it in Straght Line
    straight = False
    for d in range(directions.shape[0]):
        dx, dy, dz = directions[d]
        cnt = 1
        for step in range(-defect_num // 2 - 1, defect_num // 2 + 1):
            xi, yi, zi = x + dx*step, y + dy*step, z + dz*step
            if 0 <= xi < cur.shape[0] and 0 <= yi < cur.shape[1] and 0 <= zi < cur.shape[2]:
                v = cur[xi, yi, zi]
                if v == 1 or v == 2:
                    cnt += 1
                else:
                    break
            else:
                break
        if cnt >= defect_num:
            straight = True
            break

    # Count Neighbors
    grow_cnt = 0
    for i in range(pattern.shape[0]):
        nx, ny, nz = x + pattern[i, 0], y + pattern[i, 1], z + pattern[i, 2]
        if 0 <= nx < cur.shape[0] and 0 <= ny < cur.shape[1] and 0 <= nz < cur.shape[2]:
            if cur[nx, ny, nz] == 1:
                grow_cnt += 1

    # Irritate
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
