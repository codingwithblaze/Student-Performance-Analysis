# Data Dictionary - Student Performance Analysis System

This document outlines the fields in the student performance datasets: the raw student performance data (`Dataset/student_data.csv`), the engineered dataset (`Dataset/student_data_engineered.csv`), and BM EXCEL BLAZE's academic records (`Dataset/blaze_academic_records.csv`).

---

## 1. Student Performance Dataset (Primary Data)

| Field Name | Data Type | Description | Values/Range | Example |
| :--- | :--- | :--- | :--- | :--- |
| **Student_ID** | Categorical (String) | Unique alphanumeric identifier for each student. | STU1001 – STU2000 | `STU1054` |
| **Gender** | Categorical (String) | Gender of the student. | `Male`, `Female` | `Female` |
| **Age** | Numerical (Integer) | Age of the student at the time of academic tracking. | 15 – 18 | `16` |
| **Attendance_Percentage** | Numerical (Float) | Percentage of classes attended during the academic semester. | 60.0% – 100.0% | `92.56` |
| **Study_Hours** | Numerical (Float) | Average hours spent by the student studying outside of class per day. | 1.0 – 12.0 hours | `4.25` |
| **Previous_Grades** | Numerical (Float) | Average academic score obtained in previous examinations. | 40.0 – 100.0 | `76.40` |
| **Parent_Education** | Categorical (String) | Highest educational attainment of either parent. | `High School`, `Associate's`, `Bachelor's`, `Master's` | `Bachelor's` |
| **Internet_Access** | Categorical (String) | Availability of high-speed internet connection at home. | `Yes`, `No` | `Yes` |
| **Family_Income** | Categorical (String) | General level of household income. | `Low`, `Medium`, `High` | `Medium` |
| **Extra_Activities** | Categorical (String) | Student's participation in extracurricular school activities. | `Yes`, `No` | `No` |
| **School_Type** | Categorical (String) | The administration type of the school. | `Public`, `Private` | `Public` |
| **Final_Exam_Score** | Numerical (Integer) | The final exam grade obtained by the student (Target Variable). | 0 – 100 | `78` |
| **Pass_Fail_Status** | Categorical (String) | Binary classification of exam outcome (Passing Threshold = 60). | `Pass`, `Fail` | `Pass` |

---

## 2. Engineered Features (`student_data_engineered.csv`)

These features are derived by the data preprocessing and feature engineering script (`Python_Scripts/ml_modeling.py`) to improve model performance and enable advanced dashboard filtering.

| Feature Name | Data Type | Formula/Rules | Values/Range |
| :--- | :--- | :--- | :--- |
| **Attendance_Category** | Categorical (String) | Segmented categories of student attendance. | `Critical` (<75%), `Borderline` (75%–85%), `Good` (85%–95%), `Excellent` (>=95%) |
| **Study_Efficiency_Index** | Numerical (Float) | Active engagement metric, combining study hours weighted by attendance rate.<br>$\text{Study Hours} \times \frac{\text{Attendance Percentage}}{100.0}$ | 0.6 – 12.0 |
| **Risk_Level** | Categorical (String) | Heuristic score reflecting academic vulnerability using baseline features (prior to exam score prediction). | `High` (Score >= 3), `Medium` (Score 1-2), `Low` (Score 0)<br>*Based on attendance, study hours, and previous grades.* |
| **Performance_Grade** | Categorical (String) | Standard US educational grading scale mapped from `Final_Exam_Score`. | `O` (>=90), `A+` (80–89), `A` (70–79), `B+` (60–69), `B` (50–59), `C` (40–49), `F` (<40) |

---

## 3. Case Study: BM EXCEL BLAZE B.Tech Records (`blaze_academic_records.csv`)

This dataset captures the historical academic records of student **BM EXCEL BLAZE** across Semesters 1 through 7, used to showcase individual trajectory analytics.

| Field Name | Data Type | Description | Example |
| :--- | :--- | :--- | :--- |
| **Semester** | Numerical (Integer) | The college academic semester. | `1` to `7` |
| **Course_Code** | Categorical (String) | Alphanumeric unique identifier for each academic subject. | `R22MTH1111` |
| **Course_Name** | Categorical (String) | Name of the subject/course. | `MATRICES AND CALCULUS` |
| **Int_Marks** | Numerical (Integer) | Internal evaluation marks secured (Out of 40 or 50). | `26` |
| **Ext_Marks** | Numerical (Integer) | External (end-semester exam) marks secured (Out of 60 or 50). | `22` |
| **Total_Marks** | Numerical (Integer) | Total course marks secured (Sum of Internal and External). | `48` |
| **Grade** | Categorical (String) | Academic grade assigned for course performance. | `C`, `B`, `B+`, `A`, `A+`, `O`, `P` (Pass in non-credit courses) |
| **Status** | Categorical (String) | Pass/Fail status for the specific course. | `P` (Pass), `F` (Fail - *Note: Transcript contains only pass status as BM EXCEL BLAZE cleared all credits*) |
