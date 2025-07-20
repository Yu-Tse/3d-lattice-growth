from setuptools import setup, find_packages

setup(
    name="cuda-fcc-growth-sim",
    version="0.1.0",
    description="GPU‑accelerated 3‑D FCC lattice growth & defect simulation",
    packages=find_packages(where="src"),
    package_dir={"": "src"},          # 告訴 setuptools 程式碼在 src/
    install_requires=[
        "numpy",
        "matplotlib",
        "numba",
    ],
)