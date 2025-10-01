# Power BI Dashboard Development Guide
## Student Performance Analysis and Prediction System

This development guide outlines the step-by-step implementation of the interactive Power BI dashboard for the **Student Performance Analysis and Prediction System**. It serves as the design blueprint for recreating the dashboard in Power BI Desktop.

---

## 1. Dashboard Color Theme & Visual Aesthetics
To create a premium and professional user experience, the dashboard uses a custom cohesive palette:
* **Primary Deep Slate**: `#1E293B` (Used for headers, text, and main navigation)
* **Academic Teal**: `#0D9488` (Used to represent positive metrics, passing grades, and normal ranges)
* **Accent Terracotta**: `#F97316` (Used for warning elements, failing grades, and risk indications)
* **Background Light Gray**: `#F8FAFC` (Used for page backgrounds)
* **Card Background White**: `#FFFFFF` (Used for visual container boxes with a subtle drop shadow)
* **Typography**: **Segoe UI** or **Segoe UI Semibold** (Clean, modern system font)

---

## 2. Data Modeling & Star Schema
The dataset should be structured into a clean star schema to ensure optimal DAX performance:

```mermaid
classDiagram
    class Fact_Student_Performance {
        +Student_ID (FK)
        +Attendance_Percentage
        +Study_Hours
        +Previous_Grades
        +Final_Exam_Score
        +Pass_Fail_Status
        +Study_Efficiency_Index
    }
    class Dim_Student_Demographics {
        +Student_ID (PK)
        +Gender
        +Age
    }
    class Dim_Socioeconomic_Factors {
        +Student_ID (PK)
        +Parent_Education
        +Internet_Access
        +Family_Income
        +Extra_Activities
        +School_Type
        +Risk_Level
        +Attendance_Category
    }
    Fact_Student_Performance --> Dim_Student_Demographics : "1:1 (Student_ID)"
    Fact_Student_Performance --> Dim_Socioeconomic_Factors : "1:1 (Student_ID)"
```

---

## 3. DAX Calculated Measures
Create a dedicated table named `_Measures` and implement the following business formulas:

### KPI Core Metrics
```dax
Total Students = DISTINCTCOUNT(Fact_Student_Performance[Student_ID])
```
```dax
Average Score = AVERAGE(Fact_Student_Performance[Final_Exam_Score])
```
```dax
Pass Rate % = 
DIVIDE(
    CALCULATE(COUNT(Fact_Student_Performance[Student_ID]), Fact_Student_Performance[Pass_Fail_Status] = "Pass"),
    [Total Students],
    0
)
```
```dax
Average Attendance % = AVERAGE(Fact_Student_Performance[Attendance_Percentage])
```

### Risk & Segment Metrics
```dax
At-Risk Students Count = 
CALCULATE(
    COUNT(Fact_Student_Performance[Student_ID]), 
    Dim_Socioeconomic_Factors[Risk_Level] IN {"High", "Medium"}
)
```
```dax
At-Risk Rate % = DIVIDE([At-Risk_Students_Count], [Total Students], 0)
```
```dax
Average Study Hours = AVERAGE(Fact_Student_Performance[Study_Hours])
```
```dax
Study Efficiency Index = AVERAGE(Fact_Student_Performance[Study_Efficiency_Index])
```

### Advanced What-If Analysis
Create a numeric parameter table `WhatIfStudyHours` with a range of `0` to `12`, incrementing by `0.5`. Define the parameter value as `[Study Hours Value]`.
```dax
Projected Score = 
[Average Score] + (([Study Hours Value] - [Average Study Hours]) * 2.8)
```
*This utilizes the beta coefficient from our linear regression model (2.8 points gained per daily study hour) to perform dynamic, interactive projections.*

---

## 4. Dashboard Pages & Layout

### Page 1: Executive Overview (The Recruiter Wow Page)
* **Goal**: High-level visual summary of institutional performance.
* **Top Header Row**: Contains a dark navy sidebar/title card and 4 main KPI Cards (Total Students, Average Score, Pass Rate %, Average Attendance %).
* **Left Visual**: **Donut Chart** – "Enrollment by Gender" (using Slate Blue and Teal colors).
* **Middle Visual**: **Clustered Bar Chart** – "Pass Rate % by Family Income Level" (compares Low, Medium, and High income).
* **Right Visual**: **KPI Card Overlay** – "Average Study Hours vs Study Efficiency".
* **Bottom Panel**: **Card Grid** of the Top 5 Performing Students (Table sorted by Exam Score descending, displaying Student_ID, Grade, Attendance, and Score).

### Page 2: Academic Insights
* **Goal**: Uncover key drivers of high exam grades.
* **Slicers (Top Panel)**: School Type (Public vs Private), Gender, and Parent Education.
* **Visual 1: Scatter Plot** – "Attendance % vs Final Exam Score" with a trend line. Points colored by Pass/Fail status (Teal/Orange).
* **Visual 2: Box Plot / Bar Chart** – "Average Score by Parent Education Level". Shows clear linear trend: Master's > Bachelor's > Associate's > High School.
* **Visual 3: Area Chart** – "Study Hours vs Final Score Trendline" showing scores rising as study hours increase.
* **Visual 4: Heatmap Matrix** – "Gender vs School Type" displaying average scores.

### Page 3: Student Risk Analysis (Intervention Hub)
* **Goal**: Identify vulnerable students and flag them for school counseling.
* **Main KPI Indicator**: "At-Risk Rate %" (large card with conditional formatting: red if > 25%, orange if 15%-25%, green if < 15%).
* **Visual 1: Stacked Column Chart** – "Risk Classification by Attendance Category" (revealing that "Critical" attendance directly maps to "High" risk).
* **Visual 2: Pie Chart** – "Students needing Intervention by Risk Level" (High vs Medium vs Low risk).
* **Visual 3: Interactive Table (The Intervention Registry)**:
  * Columns: `Student_ID`, `Attendance_Percentage`, `Study_Hours`, `Previous_Grades`, `Risk_Level`, `Predicted_Exam_Score`.
  * *Conditional Formatting*: Apply light red background fill to rows where `Risk_Level = "High"`.
  * Add a button: "Export Intervention List" to CSV.

### Page 4: Interactive What-If Simulation
* **Goal**: Empower school principals to simulate policy changes (e.g. mandatory study halls).
* **Interactive Slicer**: Numeric Slider representing the "Study Hours Parameter" (0 to 12 hours).
* **KPI Comparison Cards**:
  1. "Current Average Score" vs "Projected Average Score".
  2. "Current Pass Rate" vs "Projected Pass Rate" (heuristically modeled).
* **Visual 1: Line Chart** – "Impact of Study Hours on Projected Grades by School Type".
* **Visual 2: Bullet Visual** – Comparing current vs projected scores across demographic segments.

---

## 5. Case Study Integration: Student BM EXCEL BLAZE
To highlight an individual student success story or run diagnostic tests:
* Implement a **Search Slicer** linked to `Fact_Student_Performance[Student_ID]` or a custom text filter.
* When searching for student **`22D41A7210` (BM EXCEL BLAZE)**, the dashboard highlights:
  * CGPA: `7.30`
  * Academic trajectory: SGPAs rising from `6.10` in Sem 2 to `8.10` in Sem 7.
  * Risk Classification: **Low Risk** (indicated by green light).
  * Predicted Sem 8 SGPA: **`8.31`** (calculated from his historical performance).
