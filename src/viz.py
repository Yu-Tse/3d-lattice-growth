import os, numpy as np, matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def plot_fcc(grid, frame, out_dir):
    os.makedirs(f"{out_dir}/frames", exist_ok=True)
    fig = plt.figure(figsize=(6,6))
    ax = fig.add_subplot(111, projection='3d')
    x,y,z = np.where(grid == 1)
    ax.scatter(x,y,z,c='blue',s=10)
    x,y,z = np.where(grid == -1)
    ax.scatter(x,y,z,c='red',s=10)
    x,y,z = np.where(grid == 2)
    ax.scatter(x,y,z,c='green',s=10)
    ax.set(xlim=(0,grid.shape[0]-1),ylim=(0,grid.shape[1]-1),zlim=(0,grid.shape[2]-1))
    plt.title(f"Frame {frame}")
    plt.savefig(f"{out_dir}/frames/frame_{frame:03d}.png")
    plt.close()

def save_stats(prob, grown, bad, out_dir):
    os.makedirs(out_dir, exist_ok=True)
    x = np.arange(len(prob))
    for data, title, fname, ylabel in [
        (prob,  "Defect Probability", "prob.png",   "Probability"),
        (bad,   "Defect Number",      "defect.png", "Count"),
        (grown, "Total Number",       "total.png",  "Count"),
    ]:
        plt.figure(); plt.plot(x,data)
        plt.title(title); plt.xlabel("Frame"); plt.ylabel(ylabel); plt.grid()
        plt.savefig(f"{out_dir}/{fname}"); plt.close()
