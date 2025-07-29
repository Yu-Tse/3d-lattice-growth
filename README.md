## 🧬 3D Lattice Growth Simulator

### 🔍 Project Description

This repository implements a 3D lattice growth simulator inspired by recent advances in atomistic modeling of crystal structures. The framework can be adapted for simulating grain growth, defect propagation, and morphological evolution in FCC or other crystal systems.

The code is based on concepts discussed in the following reference:

> **Tiwary, C.S., Srivastava, V., & Sharma, A.** (2022). *On the structure of polycrystals formed in an atomistic simulation of crystal growth*. Nature Computational Materials, 8, Article 54. [https://doi.org/10.1038/s41524-022-00824-5](https://doi.org/10.1038/s41524-022-00824-5)

### 🧠 Key Features

* 3D lattice generation using simple rule-based logic
* Customizable lattice size, growth direction, and seeding logic
* Visualization of growth states using Matplotlib (2D/3D)
* Potential to integrate with physical models (e.g., thermal gradients, grain boundaries, nucleation)

### 🗂 Repository Structure

```
3d-lattice-growth/
├── lattice_growth.py     # Core lattice simulation logic
├── visualize.py          # Visualization tools
├── utils.py              # Helper functions
├── main.py               # Run simulation and plot results
├── figures/              # Output images or analysis plots
├── requirements.txt
└── README.md
```

### ⚙️ Requirements

* Python 3.7+
* NumPy
* Matplotlib

Install dependencies:

```bash
pip install -r requirements.txt
```

### 🚀 How to Run

```bash
python main.py
```

This runs a default growth simulation and generates visual output in the `figures/` directory.

You may customize simulation parameters (e.g., lattice size, growth rules, iterations) by modifying `main.py` or extending `lattice_growth.py`.

### 📄 Example Output

Sample plots and growth snapshots will be saved under the `figures/` folder. You can include screenshots or lattice evolution plots here.

### 📚 Reference

This work draws inspiration from the following publication:

> Tiwary, C.S., Srivastava, V., & Sharma, A. (2022). On the structure of polycrystals formed in an atomistic simulation of crystal growth. *Nature Computational Materials*, 8, 54. [https://doi.org/10.1038/s41524-022-00824-5](https://doi.org/10.1038/s41524-022-00824-5)

Please cite this paper if your derivative work is based on this model.

### 📝 License

[MIT License](LICENSE)

## 🙋‍♂️ Author

**Yu-Tse Wu** (吳雨澤)  
*Master’s Student at the Institute of Innovation and Semiconductor Manufacturing, National Sun Yat-sen University*
