import os
import pandas as pd
import numpy as np

def clean_data(input_path="Dataset/student_data.csv", output_path="Dataset/student_data_cleaned.csv"):
    print("=== Phase 3: Starting Data Cleaning Process ===")
    
    # Check if dataset exists
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Source file {input_path} not found.")
        
    df = pd.read_csv(input_path)
    print(f"Initial raw dataset shape: {df.shape}")
    
    # 1. Duplicate Removal
    duplicates_count = df.duplicated().sum()
    print(f"Number of duplicate rows found: {duplicates_count}")
    if duplicates_count > 0:
        df = df.drop_duplicates().reset_index(drop=True)
        print("Duplicates removed successfully.")
    
    # 2. Outlier Detection & Handling
    print("\n--- Outlier Detection & Handling ---")
    
    # Attendance Percentage: Cap at 100% since it cannot logically exceed 100%
    att_outliers = df[df["Attendance_Percentage"] > 100.0]
    print(f"Attendance outliers (>100%): {len(att_outliers)}")
    if not att_outliers.empty:
        print(f"Capping attendance values above 100% to 100.0. Affects indexes: {att_outliers.index.tolist()}")
        df.loc[df["Attendance_Percentage"] > 100.0, "Attendance_Percentage"] = 100.0
        
    # Study Hours: Cap at 12 hours per day as a logical limit, or use IQR
    # Let's inspect values above 12 hours
    study_outliers = df[df["Study_Hours"] > 12.0]
    print(f"Study Hours outliers (>12 hrs/day): {len(study_outliers)}")
    if not study_outliers.empty:
        # We will replace them with the median of normal study hours (<= 12)
        study_median = df.loc[df["Study_Hours"] <= 12.0, "Study_Hours"].median()
        print(f"Replacing excessive study hours with median value of normal range: {study_median:.2f} hours")
        df.loc[df["Study_Hours"] > 12.0, "Study_Hours"] = study_median

    # Final Exam Score: Limit to [0, 100]
    score_low_outliers = df[df["Final_Exam_Score"] < 0]
    score_high_outliers = df[df["Final_Exam_Score"] > 100]
    print(f"Final Exam Score outliers (<0): {len(score_low_outliers)}")
    print(f"Final Exam Score outliers (>100): {len(score_high_outliers)}")
    
    if not score_low_outliers.empty:
        df.loc[df["Final_Exam_Score"] < 0, "Final_Exam_Score"] = 0
    if not score_high_outliers.empty:
        df.loc[df["Final_Exam_Score"] > 100, "Final_Exam_Score"] = 100
    print("Final Exam Score outliers capped to range [0, 100].")

    # 3. Missing Value Treatment
    print("\n--- Missing Value Treatment ---")
    print(f"Missing values before treatment:\n{df.isnull().sum()}")
    
    # Attendance Percentage: Impute with Median
    att_median = df["Attendance_Percentage"].median()
    df["Attendance_Percentage"] = df["Attendance_Percentage"].fillna(att_median)
    print(f"Imputed missing Attendance_Percentage with median: {att_median:.2f}%")
    
    # Study Hours: Impute with Median
    study_median = df["Study_Hours"].median()
    df["Study_Hours"] = df["Study_Hours"].fillna(study_median)
    print(f"Imputed missing Study_Hours with median: {study_median:.2f} hours")
    
    # Parent Education: Impute with Mode (most frequent category)
    edu_mode = df["Parent_Education"].mode()[0]
    df["Parent_Education"] = df["Parent_Education"].fillna(edu_mode)
    print(f"Imputed missing Parent_Education with mode: '{edu_mode}'")
    
    # 4. Data Consistency & Integrity Checks
    print("\n--- Data Consistency & Integrity Checks ---")
    
    # Re-verify Pass/Fail Status based on the cleaned Final Exam Score (Pass if Score >= 60, else Fail)
    # This is critical because some scores were corrected (e.g. from -10 to 0, or 120 to 100)
    print("Recalculating Pass_Fail_Status based on cleaned Final_Exam_Score (threshold >= 60)...")
    expected_status = df["Final_Exam_Score"].apply(lambda s: "Pass" if s >= 60 else "Fail")
    mismatches = (df["Pass_Fail_Status"] != expected_status).sum()
    print(f"Number of Pass/Fail status mismatches found: {mismatches}")
    df["Pass_Fail_Status"] = expected_status
    
    # Verify Age range
    print(f"Age range in cleaned data: {df['Age'].min()} to {df['Age'].max()}")
    
    # Check if there are any remaining nulls
    remaining_nulls = df.isnull().sum().sum()
    print(f"Remaining missing values in cleaned dataset: {remaining_nulls}")
    
    # 5. Save Cleaned Dataset
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"\nCleaned dataset saved successfully to '{output_path}'. Shape: {df.shape}\n")
    return df

if __name__ == "__main__":
    clean_data()
