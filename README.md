# 📊 Sales Data Analysis with Python and Pandas

This project aims to analyze a retail store's sales data using Python. It extracts key insights from raw CSV data using `pandas` and creates clear visualizations with `matplotlib`.

The goal is to simulate a real-world business scenario where sales data is provided monthly and needs to be processed for insights such as:
- Top-selling products
- Monthly revenue
- Sales performance by seller
- Revenue comparison by category

---

## 🧰 Technologies Used

- **Python** — Main programming language
- **Pandas** — Data analysis and manipulation
- **Matplotlib** — Data visualization (charts and graphs)
- **CSV Files** — As the raw data source

---

## 📁 Folder Structure

```
projeto-analisevendasloja/
├── classes/                    <- Business logic and reusable classes
├── data/                       <- Raw data files (.csv)
├── database/                   <- Optional SQLite or DB-related files
├── graficos/                   <- Output folder for generated charts
├── logs/                       <- Application log files
├── meta/                       <- Metadata for project packaging
├── notebooks/                 <- Jupyter Notebooks (optional exploratory analysis)
├── projetoanalise.egg-info/   <- Distribution metadata (auto-generated)
├── utils/                      <- Utility/helper functions
├── venv/                       <- Virtual environment folder
├── README.md                   <- Project description (you're here!)
├── main.py                     <- Main execution file
├── requirements.txt            <- Python dependencies
└── setup.py                    <- Project packaging file (optional)
```

---

## 🚀 What This Project Does

- Loads sales data from a CSV file
- Cleans and processes the data
- Groups data by seller, product, and category
- Calculates revenue and quantity sold
- Identifies best sellers and top-performing items
- Generates visual charts: bar plots, pie charts, etc.

---

## 🖼️ Sample Output (Graphs)

*(Insert example graphs here as screenshots)*

---

## 📦 How to Run

1. Clone this repository:
   ```bash
   git clone https://github.com/emanuelsoares97/projeto-analisevendasloja.git
   cd projeto-analisevendasloja
   ```
2. Create and activate a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # or venv\Scripts\activate on Windows
   ```
3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the analysis:
   ```bash
   python main.py
   ```

---

## 💡 What I Learned

- Manipulating datasets using `pandas`
- Creating visualizations with `matplotlib`
- Extracting insights from raw data
- Writing clean and modular code

---

> Built with 💻 and ☕ by Emanuel Soares — aspiring backend developer and data enthusiast.
