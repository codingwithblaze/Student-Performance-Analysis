import os
import numpy as np
import pandas as pd

def generate_student_data(num_records=1000, seed=42):
    np.random.seed(seed)
    
    # 1. Generate core features
    student_ids = [f"STU{i:04d}" for i in range(1001, 1001 + num_records)]
    genders = np.random.choice(["Male", "Female"], size=num_records, p=[0.48, 0.52])
    ages = np.random.choice([15, 16, 17, 18], size=num_records, p=[0.25, 0.35, 0.25, 0.15])
    
    # Continuous features with realistic distributions
    attendance = np.random.beta(a=8, b=2, size=num_records) * 40 + 60 # range 60 to 100, skewed towards higher attendance
    study_hours = np.random.gamma(shape=3, scale=1.5, size=num_records) # peak around 4.5 hours, right-skewed
    study_hours = np.clip(study_hours, 1, 10) # limit to 1-10 hours
    
    previous_grades = np.random.normal(loc=72, scale=12, size=num_records)
    previous_grades = np.clip(previous_grades, 40, 100)
    
    parent_edu_options = ["High School", "Associate's", "Bachelor's", "Master's"]
    parent_education = np.random.choice(parent_edu_options, size=num_records, p=[0.4, 0.3, 0.2, 0.1])
    
    internet_access = np.random.choice(["Yes", "No"], size=num_records, p=[0.85, 0.15])
    family_income = np.random.choice(["Low", "Medium", "High"], size=num_records, p=[0.3, 0.5, 0.2])
    extra_activities = np.random.choice(["Yes", "No"], size=num_records, p=[0.45, 0.55])
    school_type = np.random.choice(["Public", "Private"], size=num_records, p=[0.75, 0.25])
    
    # Create pandas DataFrame
    df = pd.DataFrame({
        "Student_ID": student_ids,
        "Gender": genders,
        "Age": ages,
        "Attendance_Percentage": attendance,
        "Study_Hours": study_hours,
        "Previous_Grades": previous_grades,
        "Parent_Education": parent_education,
        "Internet_Access": internet_access,
        "Family_Income": family_income,
        "Extra_Activities": extra_activities,
        "School_Type": school_type
    })
    
    # 2. Define target variable: Final Exam Score
    # Base formula with coefficients representing feature impact
    # Standardised/scaled impact:
    # Score = 25 + 0.3 * Attendance + 2.5 * Study_Hours + 0.35 * Previous_Grades + offsets...
    score_base = (
        20.0 
        + 0.35 * df["Attendance_Percentage"]
        + 2.8 * df["Study_Hours"]
        + 0.32 * df["Previous_Grades"]
    )
    
    # Categorical offsets
    edu_offsets = {"High School": 0.0, "Associate's": 2.0, "Bachelor's": 4.5, "Master's": 6.5}
    income_offsets = {"Low": 0.0, "Medium": 2.0, "High": 4.0}
    
    score_edu = df["Parent_Education"].map(edu_offsets)
    score_income = df["Family_Income"].map(income_offsets)
    score_internet = (df["Internet_Access"] == "Yes").astype(float) * 3.0
    score_activities = (df["Extra_Activities"] == "Yes").astype(float) * 1.5
    score_school = (df["School_Type"] == "Private").astype(float) * 2.0
    
    # Add everything together plus normal noise
    noise = np.random.normal(loc=0, scale=4.0, size=num_records)
    final_score = score_base + score_edu + score_income + score_internet + score_activities + score_school + noise
    
    # Clip and round to integer
    df["Final_Exam_Score"] = np.clip(np.round(final_score), 0, 100).astype(int)
    
    # Calculate Pass/Fail Status (Pass = Score >= 60)
    df["Pass_Fail_Status"] = df["Final_Exam_Score"].apply(lambda s: "Pass" if s >= 60 else "Fail")
    
    # 3. Inject Data Anomalies for Phase 3 Data Cleaning demo
    # Introduce missing values in 2-3% of rows for key columns
    null_idx_att = np.random.choice(df.index, size=25, replace=False)
    null_idx_study = np.random.choice(df.index, size=20, replace=False)
    null_idx_edu = np.random.choice(df.index, size=15, replace=False)
    
    df.loc[null_idx_att, "Attendance_Percentage"] = np.nan
    df.loc[null_idx_study, "Study_Hours"] = np.nan
    df.loc[null_idx_edu, "Parent_Education"] = np.nan
    
    # Introduce outliers
    # Case A: Study hours > 24 (impossible)
    outlier_idx_study = np.random.choice(df.index, size=5, replace=False)
    df.loc[outlier_idx_study, "Study_Hours"] = [25.0, 30.0, 48.0, 18.0, 22.0]
    
    # Case B: Attendance > 100% (anomalous)
    outlier_idx_att = np.random.choice(df.index, size=3, replace=False)
    df.loc[outlier_idx_att, "Attendance_Percentage"] = [110.0, 120.0, 105.0]
    
    # Case C: Extreme scores (final exam score > 100 or negative)
    outlier_idx_score = np.random.choice(df.index, size=4, replace=False)
    df.loc[outlier_idx_score, "Final_Exam_Score"] = [150, 120, -10, 105]
    
    # Introduce duplicate rows (say, 10 records duplicated)
    dup_idx = np.random.choice(df.index, size=10, replace=False)
    dup_df = df.loc[dup_idx].copy()
    # Change Student ID slightly or keep identical to simulate raw entries
    df = pd.concat([df, dup_df], ignore_index=True)
    
    # Shuffle dataframe
    df = df.sample(frac=1.0, random_state=101).reset_index(drop=True)
    
    return df

if __name__ == "__main__":
    os.makedirs("Dataset", exist_ok=True)
    df = generate_student_data(num_records=1000)
    df.to_csv("Dataset/student_data.csv", index=False)
    print(f"Dataset generated successfully at 'Dataset/student_data.csv'.")
    print(f"Shape: {df.shape}")
    print(f"Duplicates: {df.duplicated().sum()}")
    print(f"Missing Values:\n{df.isnull().sum()}")
