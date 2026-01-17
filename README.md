# Aadhaar 360: Massive Dynamics Engine
### *National Strategic Intelligence Grid*

**Aadhaar 360** is a "Massive Solution" designed to transform raw Aadhaar data into a **Decision Support System**. It moves beyond static reports to offer **Interactive, 3D Strategic Intelligence**—predicting migration, flagging security risks, and identifying "Ghost Children" across the nation.

## 🚀 The "Antigravity" Advantage
*   **Massive Dynamics**: Capable of processing millions of records to find specific, actionable anomalies.
*   **Interactive Gravity Maps**: All insights are delivered as high-performance **Plotly HTML Artifacts**—zoomable, clickable, and 3D.

## 📂 Project Structure

```bash
├── processed_data/              # Cleaned & Merged Data
├── results/                     # 📊 INTERACTIVE HTML ARTIFACTS & FORECASTS
│   ├── 1_ghost_child_radar.html
│   ├── 2_border_watch_security.html
│   ├── 3d_antigravity_field.html
│   └── ...
│
├── run_pipeline.py              # ⚡ MASTER ENGINE (Preprocessing + 5 Pillars + Forecasting)
├── forecasting_engine.py        # Logic for SARIMA (Log-Linear) Models
├── utils.py                     # Data Loading Utilities
├── requirements.txt             # Dependencies
└── 3_Executive_Summary.md       # Final Hackathon Report
```

## 🌟 The 5 Strategic Solutions (Massive Insights)

1.  **👻 The Ghost Child Finder**: A Gap Analysis engine that compares child enrolment vs. adult activity to find "missing" children.
2.  **🚧 The Border Watch**: A National Security Tripwire detecting 18+ enrolments where they should be zero.
3.  **📡 The Migration Radar**: A 3D/Treemap visualization of population shifts based on Demographic Updates.
4.  **🛡️ The Integrity Shield**: Using **Isolation Forest (ML)** to detect operational anomalies (e.g., impossible daily throughput).
5.  **🎓 Youth Awareness Tracker**: Correlating biometric updates with enrolment data to ensure 15yo compliance.

## 🛠️ How to Run

1.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

2.  **Ignite the Engine**:
    ```bash
    python run_pipeline.py
    ```
    *   This ONE command cleans data and runs the 5-Pillar Analysis to generate HTML Dashboards in `results/`.

## 📊 Datasets Used
- **Aadhaar Enrolment Dataset**: For age-demographic breakdowns and "Ghost Child" analysis.
- **Aadhaar Demographic Update Dataset**: For tracking address changes (Migration) and mobile links (FinTech).
- **Aadhaar Biometric Update Dataset**: For monitoring mandatory update compliance.
