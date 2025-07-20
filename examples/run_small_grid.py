from src.simulation import run_sim

if __name__ == "__main__":
    # 小網格＋20 帧示範，CPU / GPU 自動判斷
    run_sim(grid_size=10, frames=20, gpu=True, seed=42, out_dir="demo_output")
