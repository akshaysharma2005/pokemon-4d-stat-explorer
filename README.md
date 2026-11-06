# ⚡ Pokémon 4D Stat Explorer & Arena Simulation

[![Streamlit](https://img.shields.io/badge/Streamlit-1.30+-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)](https://streamlit.io/)
[![Plotly](https://img.shields.io/badge/Plotly-5.18+-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)](https://plotly.com/)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

> **Next-Generation Exploratory Data Analysis, 3D Convex Hull Morphospaces, and 4D Spatio-Temporal Battle Simulations for 800+ Pokémon.**

---

## 🌟 Overview

The **Pokémon 4D Stat Explorer** transforms traditional static exploratory data analysis into an interactive, multi-dimensional visual intelligence system. Utilizing modern geometric projections, unsupervised manifold learning (PCA & K-Means), and dynamic combat simulation, this application lets researchers, competitive players, and data enthusiasts dissect the statistical anatomy of Pokémon across all six generations.

```
                              ┌───────────────────────────────────┐
                              │     Pokémon Raw Attributes        │
                              │  (HP, Atk, Def, SpA, SpD, Speed)  │
                              └─────────────────┬─────────────────┘
                                                │
                 ┌──────────────────────────────┼──────────────────────────────┐
                 ▼                              ▼                              ▼
      ┌─────────────────────┐        ┌─────────────────────┐        ┌─────────────────────┐
      │   2D Analytics &    │        │  3D Continuous      │        │  4D Hyper-          │
      │   Comparative Radar │        │  Stat Morphospace   │        │  Dimensional Space  │
      └──────────┬──────────┘        └──────────┬──────────┘        └──────────┬──────────┘
                 │                              │                              │
                 ▼                              ▼                              ▼
     • Dual Polar Overlays           • 3-Axis Custom Spatial       • Gen 1-6 Time Evolution
     • 18x18 Combat Heatmap          • 3D Convex Hull Envelopes    • 3D Turn Health Drain
     • Gen Distribution Boxplots     • 3D PCA Archetype Manifold   • Real-Time Combat Logs
```

---

## ✨ Key Dimensions & Visual Innovations

### 📊 1. 2D Multi-Dimensional EDA
- **Dual Head-to-Head Polar Radar**: Compare any two Pokémon simultaneously across all 6 core combat metrics with alpha-channel polygon overlays, real PokeAPI artwork sprites, and automated stat delta calculations.
- **18x18 Type Combat Effectiveness Matrix**: Interactive heatmap highlighting offensive vs. defensive multipliers (0x Immune, 0.5x Resistant, 2.0x Super Effective).
- **Generation & Typology Boxplots**: Distribution curves highlighting power creep and defensive shifts across generations.

### 🌐 2. 3D Continuous Stat Morphospace & Manifolds
- **Custom 3D Axis Projection**: Dynamically project any 3 stats onto spatial X, Y, and Z axes with camera presets and glow markers colored by elemental typing.
- **3D Convex Hull Envelopes**: Automated computation of 3D Delaunay triangulation / convex hull meshes wrapping elite populations (e.g., Legendary specimens).
- **Unsupervised 3D PCA Manifold**: Dimensional reduction projecting all 6 base stats into 3 principal components, exposing 5 emergent combat archetypes (*Physical Tank, Special Sweeper, Speed Striker, Bulky Support, Legendary Juggernaut*).

### ⏳ 3. 4D Hyper-Dimensional Evolution & Dynamic Battle Arena
- **4D Spatio-Temporal Scatter**:
  - **Dim 1 (X)**: Attack
  - **Dim 2 (Y)**: Defense
  - **Dim 3 (Z)**: Speed
  - **Dim 4 (Color)**: Total Base Stat Total (BST)
  - **Dim 5 (Size)**: HP Volume
  - **Dim 6 (Time / Slider)**: Generation Time-Lapse (animate specimens from Gen 1 to Gen 6)
- **4D Dynamic Battle Arena**: Select two combatants and simulate a full turn-based battle adhering to Speed priority, damage formulas, STAB bonuses, and elemental matchups. Observe the real-time **3D health drain vector trajectories** through combat stat space alongside full combat telemetry logs.

### 🛡️ 4. Team Synergy & Polytope Analyzer
- Assemble a competitive 6-member squad.
- Computes the aggregate geometric team stat polytope, archetype diversity ratio, and weakness counter balances.

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10 or higher
- pip package manager

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/akshaysharma2005/pokemon-4d-stat-explorer.git
   cd pokemon-4d-stat-explorer
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Streamlit Dashboard**:
   ```bash
   streamlit run app.py
   ```

4. Open your browser at `http://localhost:8501`.

---

## 📂 Repository Structure

```
pokemon-4d-stat-explorer/
├── app.py                     # Streamlit multi-tab application entry point
├── requirements.txt           # Python package dependencies
├── README.md                  # Comprehensive documentation
├── .gitignore                 # Git ignore rules
├── data/
│   └── pokemon.csv            # 800 Pokémon dataset with sprite URLs & calculated stats
├── src/
│   ├── __init__.py
│   ├── data_loader.py         # Data preprocessing, archetype clustering & PCA
│   ├── visualizer.py          # Plotly 2D, 3D, and 4D animated visual pipelines
│   └── battle_engine.py       # Turn-based battle simulator & trajectory recorder
└── notebooks/
    └── Pokemon_Stats_EDA.ipynb# Original exploratory data analysis notebook
```

---

## 📊 Dataset Attribution
- Dataset source: The classic 800 Pokémon dataset (Generations 1-6) enriched with sprite assets from the [PokéAPI](https://pokeapi.co/).

---

## 👤 Author
- **M Akshay Sharma** ([@akshaysharma2005](https://github.com/akshaysharma2005))
- GitHub: [https://github.com/akshaysharma2005](https://github.com/akshaysharma2005)
