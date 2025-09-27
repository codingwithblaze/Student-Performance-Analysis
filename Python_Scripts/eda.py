import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go

def run_eda(input_path="Dataset/student_data_cleaned.csv", output_dir="Images"):
    print("=== Phase 4: Starting Exploratory Data Analysis ===")
    
    # Check if cleaned data exists
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Cleaned dataset not found at {input_path}. Run preprocessing first.")
        
    df = pd.read_csv(input_path)
    os.makedirs(output_dir, exist_ok=True)
    
    # Set professional plotting style
    plt.rcParams['font.family'] = 'sans-serif'
    plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial', 'Helvetica']
    sns.set_theme(style="whitegrid")
    
    # Custom harmonious color palette
    colors = {
        'primary': '#2B4C7E',    # Slate Blue
        'secondary': '#2A9D8F',  # Teal
        'accent': '#E76F51',     # Warm Terracotta
        'neutral_dark': '#264653',
        'neutral_light': '#F4F6F9',
        'pass': '#2A9D8F',
        'fail': '#E76F51'
    }
    
    print("\n--- Generating Univariate Plots ---")
    
    # 1. Gender Distribution
    plt.figure(figsize=(7, 5))
    gender_counts = df['Gender'].value_counts()
    plt.bar(gender_counts.index, gender_counts.values, color=[colors['primary'], colors['secondary']], width=0.6, edgecolor='black', linewidth=0.7)
    for i, val in enumerate(gender_counts.values):
        plt.text(i, val + 15, f"{val} ({val/len(df)*100:.1f}%)", ha='center', fontweight='bold', color='#333333')
    plt.title("Gender Distribution of Students", fontsize=14, fontweight='bold', pad=15, color=colors['neutral_dark'])
    plt.xlabel("Gender", fontsize=12)
    plt.ylabel("Number of Students", fontsize=12)
    plt.ylim(0, max(gender_counts.values) * 1.15)
    plt.tight_layout()
    plt.savefig(f"{output_dir}/gender_distribution.png", dpi=300)
    plt.close()
    print("Saved gender_distribution.png")

    # 2. Attendance Distribution
    plt.figure(figsize=(8, 5))
    sns.histplot(df['Attendance_Percentage'], kde=True, color=colors['primary'], bins=20, edgecolor='white')
    plt.title("Distribution of Attendance Percentage", fontsize=14, fontweight='bold', pad=15, color=colors['neutral_dark'])
    plt.xlabel("Attendance Percentage (%)", fontsize=12)
    plt.ylabel("Student Count", fontsize=12)
    plt.tight_layout()
    plt.savefig(f"{output_dir}/attendance_distribution.png", dpi=300)
    plt.close()
    print("Saved attendance_distribution.png")

    # 3. Study Hours Distribution
    plt.figure(figsize=(8, 5))
    sns.histplot(df['Study_Hours'], kde=True, color=colors['secondary'], bins=20, edgecolor='white')
    plt.title("Distribution of Daily Study Hours", fontsize=14, fontweight='bold', pad=15, color=colors['neutral_dark'])
    plt.xlabel("Daily Study Hours", fontsize=12)
    plt.ylabel("Student Count", fontsize=12)
    plt.tight_layout()
    plt.savefig(f"{output_dir}/study_hours_distribution.png", dpi=300)
    plt.close()
    print("Saved study_hours_distribution.png")

    # 4. Score Distribution
    plt.figure(figsize=(8, 5))
    sns.histplot(df['Final_Exam_Score'], kde=True, color=colors['neutral_dark'], bins=25, edgecolor='white')
    plt.axvline(60, color=colors['accent'], linestyle='--', linewidth=2, label='Passing Threshold (60)')
    plt.title("Distribution of Final Exam Scores", fontsize=14, fontweight='bold', pad=15, color=colors['neutral_dark'])
    plt.xlabel("Final Exam Score", fontsize=12)
    plt.ylabel("Student Count", fontsize=12)
    plt.legend()
    plt.tight_layout()
    plt.savefig(f"{output_dir}/score_distribution.png", dpi=300)
    plt.close()
    print("Saved score_distribution.png")

    print("\n--- Generating Bivariate Plots ---")
    
    # 5. Attendance vs Score
    plt.figure(figsize=(8, 6))
    sns.scatterplot(data=df, x='Attendance_Percentage', y='Final_Exam_Score', hue='Pass_Fail_Status', 
                    palette={'Pass': colors['pass'], 'Fail': colors['fail']}, alpha=0.7, s=40)
    # Fit regression line
    sns.regplot(data=df, x='Attendance_Percentage', y='Final_Exam_Score', scatter=False, color='#444444', 
                line_kws={'linestyle': '-', 'linewidth': 1.5})
    plt.title("Attendance Percentage vs Final Exam Score", fontsize=14, fontweight='bold', pad=15, color=colors['neutral_dark'])
    plt.xlabel("Attendance Percentage (%)", fontsize=12)
    plt.ylabel("Final Exam Score", fontsize=12)
    plt.legend(title='Exam Status')
    plt.tight_layout()
    plt.savefig(f"{output_dir}/attendance_vs_score.png", dpi=300)
    plt.close()
    print("Saved attendance_vs_score.png")

    # 6. Study Hours vs Score
    plt.figure(figsize=(8, 6))
    sns.scatterplot(data=df, x='Study_Hours', y='Final_Exam_Score', hue='Pass_Fail_Status', 
                    palette={'Pass': colors['pass'], 'Fail': colors['fail']}, alpha=0.7, s=40)
    sns.regplot(data=df, x='Study_Hours', y='Final_Exam_Score', scatter=False, color='#444444', 
                line_kws={'linestyle': '-', 'linewidth': 1.5})
    plt.title("Daily Study Hours vs Final Exam Score", fontsize=14, fontweight='bold', pad=15, color=colors['neutral_dark'])
    plt.xlabel("Daily Study Hours", fontsize=12)
    plt.ylabel("Final Exam Score", fontsize=12)
    plt.legend(title='Exam Status')
    plt.tight_layout()
    plt.savefig(f"{output_dir}/study_hours_vs_score.png", dpi=300)
    plt.close()
    print("Saved study_hours_vs_score.png")

    # 7. Gender vs Performance (Box Plot)
    plt.figure(figsize=(7, 5))
    sns.boxplot(data=df, x='Gender', y='Final_Exam_Score', palette=[colors['primary'], colors['secondary']], width=0.5)
    plt.title("Final Exam Score Distribution by Gender", fontsize=14, fontweight='bold', pad=15, color=colors['neutral_dark'])
    plt.xlabel("Gender", fontsize=12)
    plt.ylabel("Final Exam Score", fontsize=12)
    plt.tight_layout()
    plt.savefig(f"{output_dir}/gender_vs_performance.png", dpi=300)
    plt.close()
    print("Saved gender_vs_performance.png")

    # 8. Parent Education vs Score (Box Plot)
    plt.figure(figsize=(9, 5))
    edu_order = ["High School", "Associate's", "Bachelor's", "Master's"]
    sns.boxplot(data=df, x='Parent_Education', y='Final_Exam_Score', order=edu_order, palette="viridis", width=0.6)
    plt.title("Final Exam Score by Parent Education Level", fontsize=14, fontweight='bold', pad=15, color=colors['neutral_dark'])
    plt.xlabel("Parent Education Level", fontsize=12)
    plt.ylabel("Final Exam Score", fontsize=12)
    plt.tight_layout()
    plt.savefig(f"{output_dir}/parent_education_vs_score.png", dpi=300)
    plt.close()
    print("Saved parent_education_vs_score.png")

    print("\n--- Generating Multivariate Plots ---")
    
    # 9. Correlation Heatmap
    plt.figure(figsize=(8, 6))
    num_cols = ['Age', 'Attendance_Percentage', 'Study_Hours', 'Previous_Grades', 'Final_Exam_Score']
    corr_matrix = df[num_cols].corr()
    
    # Custom diverging color map
    cmap = sns.diverging_palette(220, 20, as_cmap=True)
    sns.heatmap(corr_matrix, annot=True, cmap=cmap, fmt=".2f", linewidths=0.5, vmin=-1, vmax=1, square=True)
    plt.title("Correlation Matrix of Academic Features", fontsize=14, fontweight='bold', pad=15, color=colors['neutral_dark'])
    plt.tight_layout()
    plt.savefig(f"{output_dir}/correlation_heatmap.png", dpi=300)
    plt.close()
    print("Saved correlation_heatmap.png")

    # 10. Pair Plot
    # Select columns of interest for a cleaner pair plot
    pair_cols = ['Attendance_Percentage', 'Study_Hours', 'Previous_Grades', 'Final_Exam_Score', 'Pass_Fail_Status']
    g = sns.pairplot(df[pair_cols], hue='Pass_Fail_Status', palette={'Pass': colors['pass'], 'Fail': colors['fail']},
                     plot_kws={'alpha': 0.6, 's': 25}, diag_kind='kde')
    g.fig.suptitle("Pairwise Relationships of Academic Metrics", y=1.02, fontsize=16, fontweight='bold', color=colors['neutral_dark'])
    g.savefig(f"{output_dir}/pair_plot.png", dpi=300)
    plt.close()
    print("Saved pair_plot.png")

    print("=== EDA Visualizations Successfully Generated ===")

if __name__ == "__main__":
    run_eda()
