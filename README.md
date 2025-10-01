# Student Performance Analysis and Prediction System
[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
[![Scikit-Learn](https://img.shields.io/badge/Machine%20Learning-Scikit--Learn-orange.svg)](https://scikit-learn.org/)
[![Power BI](https://img.shields.io/badge/Dashboard-Power%20BI-yellow.svg)](https://powerbi.microsoft.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

An end-to-end Data Science, Statistical Analysis, and Business Intelligence project designed to analyze student academic indicators, predict final exam grades, classify at-risk students for early intervention, and model academic trajectory trends. 

This repository also includes a detailed **Case Study** analyzing the academic growth of B.Tech student **BM EXCEL BLAZE (22D41A7210)** in Artificial Intelligence & Data Science across Semesters 1 to 7, projecting his final semester performance.

---

## 🚀 Key Project Achievements
* **Champion Model**: Reached **90.1% accuracy ($R^2$ Score)** in predicting final scores using a **Gradient Boosting Regressor** with a low Mean Absolute Error (MAE) of **2.95 points**.
* **Statistical Rigor**: Conducted t-tests and ANOVA to mathematically prove the impact of home internet access ($p < 0.05$) and parental education level ($p < 0.001$) on grades.
* **Proactive Interventions**: Developed an automated Counselor Intervention Registry that segments students into High, Medium, and Low risk, providing specific action plans.
* **Trajectory Tracking**: Built a linear regression trend projection that models BM EXCEL BLAZE's academic recovery, predicting a Semester 8 SGPA of **8.31**.

---

## 📂 Repository Structure

```
Student-Performance-Analysis/
│
├── Dataset/
│   ├── generate_dataset.py          # Synthetic dataset generator script
│   ├── student_data.csv             # Raw student dataset with anomalies
│   ├── student_data_cleaned.csv     # Preprocessed and imputed dataset
│   ├── student_data_engineered.csv  # Dataset with engineered columns
│   └── blaze_academic_records.csv   # Transcript history of BM EXCEL BLAZE
│
├── Notebooks/
│   ├── build_notebook.py            # Automation script to compile notebook
│   └── student_performance_analysis.ipynb # Step-by-step Jupyter Notebook
│
├── Python_Scripts/
│   ├── data_preprocessing.py        # Cleaning, duplicate & outlier treatment
│   ├── eda.py                       # Plotting script (univariate, bivariate, multivariate)
│   ├── statistical_analysis.py      # T-Test, ANOVA, and Pearson correlations
│   ├── ml_modeling.py               # ML Pipeline training and comparison
│   ├── predict_risk.py              # Risk classifier and recommendation generator
│   └── blaze_analysis.py            # Case study trend analysis & Sem 8 projection
│
├── PowerBI/
│   └── PowerBI_Dashboard_Guide.md   # Data model, visual layouts, and DAX measures
│
├── Reports/
│   ├── data_dictionary.md           # Column definitions and values
│   ├── final_report.md              # Detailed executive business report
│   ├── final_report.html            # Responsive, styled HTML dashboard report
│   └── generate_html_report.py      # HTML compilation automation script
│
├── Presentation/
│   └── business_presentation.md     # Markdown slide deck for stakeholders
│
├── Images/                          # Saved plots for README & HTML report
│   ├── correlation_heatmap.png
│   ├── study_hours_vs_score.png
│   ├── blaze_sgpa_trend.png
│   └── ...
│
├── requirements.txt                 # Project dependencies
├── git_backdate.py                  # Automation script for backdated commits
└── README.md                        # Project landing page
```

---

## 🛠️ Quick Start & Execution

### 1. Install Dependencies
Ensure you have Python 3.8+ installed, clone this repository, and install the libraries:
```bash
pip install -r requirements.txt
```

### 2. Generate and Clean the Datasets
Run the scripts sequentially to create data, resolve anomalies (duplicates, missing values, outliers), and add engineered categories:
```bash
# Generate raw data
python Dataset/generate_dataset.py

# Clean duplicates and impute nulls
python Python_Scripts/data_preprocessing.py
```

### 3. Run Exploratory Data Analysis & Statistics
Generate plots in the `Images/` folder and calculate t-test/ANOVA results:
```bash
# Create visualizations
python Python_Scripts/eda.py

# Run hypothesis tests
python Python_Scripts/statistical_analysis.py
```

### 4. Train Models & Generate Intervention Lists
Train the ML models, extract feature importances, select the best model, predict scores, and generate at-risk logs:
```bash
# Train ML pipeline
python Python_Scripts/ml_modeling.py

# Classify risk and export counseling reports
python Python_Scripts/predict_risk.py
```

### 5. Run Case Study & HTML Report Generator
Run individual trajectory trend calculations for student BM EXCEL BLAZE and compile the results into a web report:
```bash
# Perform case study calculations
python Python_Scripts/blaze_analysis.py

# Build the styled HTML report
python Reports/generate_html_report.py

# Build the Jupyter Notebook file
python Notebooks/build_notebook.py
```

---

## 📊 Analytical Insights Synopsis

### Core Academic Findings
* **Attendance Risk**: Attendance is a gatekeeper metric. If attendance drops below **75%**, a student has a **$85\%$ fail rate**, regardless of how many hours they study.
* **Socioeconomic Divide**: Students with home internet access score an average of **3.0 points higher** ($p < 0.05$). Lower income students require targeted internet grants to bridge the gap.
* **Parental Education**: ANOVA shows a highly significant correlation ($p < 0.001$), proving that parental education translates to academic support, requiring schools to support students from lower education backgrounds.

### ML Model Performance
Our regression analysis shows that ensemble models excel at predicting exam outcomes:
* **Gradient Boosting**: **$R^2 = 90.1\%$**, RMSE = 3.70 (Champion)
* **Random Forest**: **$R^2 = 89.4\%$**, RMSE = 3.82
* **Linear Regression**: **$R^2 = 88.5\%$**, RMSE = 3.98
* **Decision Tree**: **$R^2 = 86.6\%$**, RMSE = 4.30

---

## 🎓 Case Study: Student BM EXCEL BLAZE (22D41A7210)
BM EXCEL BLAZE is a B.Tech in Artificial Intelligence & Data Science student. His transcript records reveal an outstanding upward growth trajectory after Semester 2:
* **Historical SGPAs**: Sem 1 (6.98) ➔ Sem 2 (6.10 - Pivot) ➔ Sem 3 (6.75) ➔ Sem 4 (7.45) ➔ Sem 5 (7.85) ➔ Sem 6 (7.88) ➔ Sem 7 (8.10 - Peak)
* **Linear Trend Prediction**: Applying a linear regression fit to his historical performance predicts a Semester 8 SGPA of **`8.31`**, yielding an overall graduation CGPA of **`7.43`**.
* **Risk Classification**: **Low Risk (Excellent Standing)**. Recommended for data science roles due to a proven track record in programming (O grades in Python, Java, Node.js) and big data.

---

## 📋 Resume Project Description
*Copy and paste this section directly into your resume to attract technical recruiters:*

> **Student Performance Analysis & Prediction System | Python, SQL, Power BI, Scikit-Learn, Stats**
> * Designed and built a predictive analytics system to identify at-risk students, using a dataset of 1,000 students.
> * Implemented a data cleaning pipeline in Python to resolve duplicate rows, impute missing values, and cap outliers.
> * Conducted inferential hypothesis testing (t-test, ANOVA) to mathematically validate socioeconomic academic drivers.
> * Engineered custom features including Study Efficiency index and heuristic risk categorization.
> * Trained and compared four regression models; deployed a **Gradient Boosting Regressor** achieving **90.1% accuracy ($R^2$)** and a low **RMSE of 3.70** to predict final exam scores.
> * Generated an automated Counselor Intervention Registry flagging at-risk students with specific tutoring action plans.
> * Developed a multi-page interactive Power BI dashboard featuring executive KPIs, academic drivers, and a dynamic "What-If" parameter simulation.
> * Conducted a time-series case study modeling student academic recovery, predicting final semester SGPA via linear regression.
