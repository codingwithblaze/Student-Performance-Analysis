import os
import pandas as pd
import numpy as np
from scipy import stats

def run_statistical_analysis(input_path="Dataset/student_data_cleaned.csv"):
    print("=== Phase 5: Starting Statistical Analysis ===")
    
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Cleaned dataset not found at {input_path}")
        
    df = pd.read_csv(input_path)
    
    # 1. Descriptive Statistics
    num_cols = ['Age', 'Attendance_Percentage', 'Study_Hours', 'Previous_Grades', 'Final_Exam_Score']
    desc_stats = {}
    
    for col in num_cols:
        mean_val = df[col].mean()
        median_val = df[col].median()
        mode_val = df[col].mode()[0]
        var_val = df[col].var()
        std_val = df[col].std()
        
        desc_stats[col] = {
            "Mean": mean_val,
            "Median": median_val,
            "Mode": mode_val,
            "Variance": var_val,
            "Std_Dev": std_val
        }
        
    desc_df = pd.DataFrame(desc_stats).T
    print("\n--- Descriptive Statistics ---")
    print(desc_df.to_string())
    
    # 2. Hypothesis Testing: T-Test (Internet Access vs Score)
    print("\n--- Hypothesis Testing: T-Test ---")
    internet_yes = df[df["Internet_Access"] == "Yes"]["Final_Exam_Score"]
    internet_no = df[df["Internet_Access"] == "No"]["Final_Exam_Score"]
    
    t_stat, p_val_t = stats.ttest_ind(internet_yes, internet_no, equal_var=False)
    print(f"Null Hypothesis (H0): Internet access has no impact on Final Exam Scores.")
    print(f"Internet Yes Mean Score: {internet_yes.mean():.2f}")
    print(f"Internet No Mean Score: {internet_no.mean():.2f}")
    print(f"T-Statistic: {t_stat:.4f}")
    print(f"P-Value: {p_val_t:.4e}")
    
    if p_val_t < 0.05:
        print("Conclusion: Reject the Null Hypothesis (p < 0.05). There is a statistically significant difference in final exam scores between students with internet access and those without.")
    else:
        print("Conclusion: Fail to reject the Null Hypothesis (p >= 0.05). There is no statistically significant difference in exam scores based on internet access.")

    # 3. Hypothesis Testing: ANOVA (Parent Education vs Score)
    print("\n--- Hypothesis Testing: ANOVA ---")
    edu_groups = []
    edu_names = df["Parent_Education"].unique()
    for name in edu_names:
        edu_groups.append(df[df["Parent_Education"] == name]["Final_Exam_Score"])
        
    f_stat, p_val_f = stats.f_oneway(*edu_groups)
    print(f"Null Hypothesis (H0): Parent education level has no impact on Final Exam Scores.")
    for name, group in zip(edu_names, edu_groups):
        print(f"  Parent Education '{name}' Mean Score: {group.mean():.2f} (n={len(group)})")
    print(f"F-Statistic: {f_stat:.4f}")
    print(f"P-Value: {p_val_f:.4e}")
    
    if p_val_f < 0.05:
        print("Conclusion: Reject the Null Hypothesis (p < 0.05). There is a statistically significant difference in exam scores based on the parent's level of education.")
    else:
        print("Conclusion: Fail to reject the Null Hypothesis (p >= 0.05). There is no statistically significant difference in exam scores based on parent education.")

    # 4. Correlation Analysis
    print("\n--- Correlation Analysis (Pearson & Spearman) ---")
    for col in ['Attendance_Percentage', 'Study_Hours', 'Previous_Grades']:
        pearson_r, p_pearson = stats.pearsonr(df[col], df['Final_Exam_Score'])
        spearman_r, p_spearman = stats.spearmanr(df[col], df['Final_Exam_Score'])
        print(f"Feature: {col}")
        print(f"  Pearson r: {pearson_r:.4f} (p-val: {p_pearson:.4e})")
        print(f"  Spearman r: {spearman_r:.4f} (p-val: {p_spearman:.4e})")

    # Save summary report
    os.makedirs("Reports", exist_ok=True)
    with open("Reports/statistical_analysis_results.txt", "w") as f:
        f.write("=== STATISTICAL ANALYSIS RESULTS ===\n\n")
        f.write("--- DESCRIPTIVE STATISTICS ---\n")
        f.write(desc_df.to_string())
        f.write("\n\n--- HYPOTHESIS TESTING: T-TEST (Internet Access vs Score) ---\n")
        f.write(f"Internet Yes Mean Score: {internet_yes.mean():.2f}\n")
        f.write(f"Internet No Mean Score: {internet_no.mean():.2f}\n")
        f.write(f"T-Statistic: {t_stat:.4f}, P-Value: {p_val_t:.4e}\n")
        f.write(f"Significant: {p_val_t < 0.05}\n\n")
        
        f.write("--- HYPOTHESIS TESTING: ANOVA (Parent Education vs Score) ---\n")
        for name, group in zip(edu_names, edu_groups):
            f.write(f"  '{name}' Mean Score: {group.mean():.2f}\n")
        f.write(f"F-Statistic: {f_stat:.4f}, P-Value: {p_val_f:.4e}\n")
        f.write(f"Significant: {p_val_f < 0.05}\n\n")
        
        f.write("--- CORRELATION ANALYSIS WITH FINAL SCORE ---\n")
        for col in ['Attendance_Percentage', 'Study_Hours', 'Previous_Grades']:
            pearson_r, _ = stats.pearsonr(df[col], df['Final_Exam_Score'])
            f.write(f"  {col} Pearson r: {pearson_r:.4f}\n")
            
    print("\nStatistical results saved to 'Reports/statistical_analysis_results.txt'.")
    print("=== Statistical Analysis Process Completed ===")

if __name__ == "__main__":
    run_statistical_analysis()
