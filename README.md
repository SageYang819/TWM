# Time with Mom Simulator

A Monte Carlo-based simulation tool for modeling long-term family time under uncertainty.

This project quantifies how life decisions — such as working abroad — impact total time spent with family, transforming an emotional question into a data-driven decision problem.

---

## 🚀 Overview

Most people intuitively understand that “time is limited,” but few can quantify how different life choices affect long-term family time.

This project provides a structured way to evaluate:

* How often to visit vs. how long to stay
* Trade-offs between working abroad and staying domestic
* The impact of aging on future time availability

---

## ✨ Features

* **Monte Carlo simulation** for uncertainty modeling
* **Aging decay function** to reflect declining interaction capacity
* **Stochastic visit frequency (Poisson process)**
* **Multi-phase life modeling** (abroad vs domestic)
* **Decision insights** (gap vs domestic baseline)
* **Multiple interfaces**:

  * Python API
  * CLI tool
  * Interactive web app (Streamlit)

---

## 📦 Installation

```bash
pip install time-with-mom
```

---

## 🧠 Usage

### 1. Python API

```python
from time_with_mom import simulate

data = simulate(
    n_sim=1000,
    mom_age=60,
    life_mean=85,
    life_std=5,
    abroad_years=10,
    visits_per_year=1,
    days_per_visit=30,
    domestic_days=120,
    decay_rate=0.03,
    meals_per_day=2
)

print(data["total_days_mean"])
```

---

### 2. CLI (Command Line Interface)

Run directly in terminal:

```bash
time-with-mom simulate --visits 2 --days 30
```

Example output:

```
=== Simulation Result ===
Avg total days: 1572
10%-90% range: 1156 - 1968
Ratio vs domestic: 50.00%
→ Moderate gap
```

---

### 3. Web App (Interactive Dashboard)

```bash
streamlit run app/streamlit_app.py
```

This launches an interactive UI for scenario exploration and visualization.

---

## 📊 Key Insights

This model reveals several important patterns:

* **Frequency dominates duration**
  Increasing visit frequency often has a larger impact than extending individual visits

* **Time value decays with age**
  Early-life interactions contribute disproportionately more

* **Uncertainty matters**
  Lifetime outcomes vary significantly — planning based on averages alone is misleading

---

## 🧩 Project Structure

```
time-with-mom/
├── src/time_with_mom/     # core simulation package
├── app/                   # Streamlit UI
├── pyproject.toml         # packaging config
└── README.md
```

---

## 🛠 Tech Stack

* Python
* NumPy
* Streamlit
* Matplotlib
* setuptools / PyPI

---

## 🎯 Positioning

This project sits at the intersection of:

* **Data Science** (simulation, uncertainty modeling)
* **Decision Science** (trade-off analysis)
* **Product Thinking** (CLI + UI + package distribution)

---

## 👤 Author

Sijie Yang

---

## 📌 Notes

This project is intended for educational and exploratory purposes.
It demonstrates how quantitative modeling can be applied to real-life decision making.

---
