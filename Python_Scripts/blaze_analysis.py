import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def analyze_blaze_records(input_path="Dataset/blaze_academic_records.csv", output_dir="Images"):
    print("=== Phase 13: Starting BM EXCEL BLAZE Trajectory Analysis ===")
    
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Academic records not found at {input_path}")
        
    df = pd.read_csv(input_path)
    os.makedirs(output_dir, exist_ok=True)
    
    # 1. Calculate General Statistics
    total_courses = len(df)
    # Ignore labs/courses with -- ext marks or 0 ext marks where appropriate
    # but let's calculate general sums
    avg_internal = df[df["Int_Marks"] > 0]["Int_Marks"].mean()
    avg_external = df[df["Ext_Marks"] > 0]["Ext_Marks"].mean()
    
    print(f"Total B.Tech Courses Analyzed (Sem 1-7): {total_courses}")
    print(f"Average Internal Marks: {avg_internal:.2f}")
    print(f"Average External Marks: {avg_external:.2f}")
    
    # Grade Counts
    grade_counts = df["Grade"].value_counts()
    print(f"Grade Distribution:\n{grade_counts}")
    
    # 2. SGPA Trend Analysis & Semester 8 Prediction
    # Exact SGPAs from transcript
    semesters = np.array([1, 2, 3, 4, 5, 6, 7])
    sgpas = np.array([6.98, 6.10, 6.75, 7.45, 7.85, 7.88, 8.10])
    
    # Linear Regression for Semester 8 Prediction
    slope, intercept = np.polyfit(semesters, sgpas, 1)
    predicted_sem8_sgpa = slope * 8 + intercept
    
    # Calculate overall CGPA from the SGPAs
    overall_cgpa = sgpas.mean() # simple average or weighted average of credits. Since each semester has 20 credits, the CGPA is simply the mean.
    print(f"Calculated CGPA: {overall_cgpa:.2f} (Transcript CGPA: 7.30)")
    print(f"Trend slope: {slope:.3f} grade points/semester")
    print(f"Predicted Semester 8 SGPA: {predicted_sem8_sgpa:.2f}")
    
    # Set professional plotting style
    sns.set_theme(style="whitegrid")
    colors = {
        'primary': '#1A365D',     # Navy Blue
        'secondary': '#319795',   # Deep Teal
        'accent': '#DD6B20',      # Deep Orange
        'neutral_dark': '#2D3748',
        'neutral_light': '#EDF2F7',
        'highlight': '#E53E3E'    # Red
    }
    
    # Plot 1: SGPA Trend & Projection
    plt.figure(figsize=(9, 5.5))
    # Plot historical SGPAs
    plt.plot(semesters, sgpas, marker='o', linewidth=3, color=colors['secondary'], markersize=8, label="Historical SGPA")
    for i, sgpa in enumerate(sgpas):
        plt.text(semesters[i], sgpa + 0.1, f"{sgpa:.2f}", ha='center', fontweight='bold', color=colors['neutral_dark'])
        
    # Plot Trend line
    x_trend = np.array([1, 2, 3, 4, 5, 6, 7, 8])
    y_trend = slope * x_trend + intercept
    plt.plot(x_trend, y_trend, linestyle='--', color=colors['accent'], linewidth=1.5, label=f"Performance Trend (Slope: {slope:.2f})")
    
    # Plot predicted Semester 8 SGPA
    plt.scatter([8], [predicted_sem8_sgpa], color=colors['highlight'], marker='*', s=200, zorder=5, label=f"Predicted Sem 8 SGPA ({predicted_sem8_sgpa:.2f})")
    plt.text(8, predicted_sem8_sgpa + 0.15, f"{predicted_sem8_sgpa:.2f}*", ha='center', fontweight='bold', color=colors['highlight'], fontsize=12)
    
    # Shade regions
    plt.axhspan(7.5, 10, alpha=0.1, color='green', label="Excellent Standing (SGPA >= 7.5)")
    plt.axhspan(6.0, 7.5, alpha=0.1, color='orange', label="Good Standing (6.0 - 7.5)")
    
    plt.title("Academic Journey & Semester 8 Prediction: BM EXCEL BLAZE", fontsize=14, fontweight='bold', pad=15, color=colors['primary'])
    plt.xlabel("Semester", fontsize=12)
    plt.ylabel("SGPA", fontsize=12)
    plt.xlim(0.5, 8.5)
    plt.ylim(5.0, 9.0)
    plt.xticks(x_trend, [f"Sem {x}" for x in x_trend])
    plt.legend(loc='lower right', frameon=True, facecolor='white', edgecolor='#e2e8f0')
    plt.tight_layout()
    plt.savefig(f"{output_dir}/blaze_sgpa_trend.png", dpi=300)
    plt.close()
    print("Saved blaze_sgpa_trend.png")

    # Plot 2: Grade Distribution
    plt.figure(figsize=(8, 5))
    grade_order = ['O', 'A+', 'A', 'B+', 'B', 'C', 'P']
    # Filter for grades that actually exist
    existing_grades = [g for g in grade_order if g in grade_counts]
    existing_counts = [grade_counts[g] for g in existing_grades]
    
    # Custom colors for grades (Greenish for good, yellowish/blue for average)
    grade_colors = []
    for g in existing_grades:
        if g in ['O', 'A+']:
            grade_colors.append('#2F855A') # Dark Green
        elif g in ['A', 'B+']:
            grade_colors.append('#319795') # Teal
        elif g in ['B']:
            grade_colors.append('#3182CE') # Blue
        else:
            grade_colors.append('#D69E2E') # Amber/Yellow
            
    bars = plt.bar(existing_grades, existing_counts, color=grade_colors, width=0.55, edgecolor='black', linewidth=0.7)
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height + 0.3, f"{int(height)}", ha='center', va='bottom', fontweight='bold')
        
    plt.title("B.Tech Subject Grade Distribution: BM EXCEL BLAZE", fontsize=14, fontweight='bold', pad=15, color=colors['primary'])
    plt.xlabel("Grade Secured", fontsize=12)
    plt.ylabel("Subject Count", fontsize=12)
    plt.ylim(0, max(existing_counts) + 2)
    plt.tight_layout()
    plt.savefig(f"{output_dir}/blaze_grade_distribution.png", dpi=300)
    plt.close()
    print("Saved blaze_grade_distribution.png")
    
    print("=== BM EXCEL BLAZE Case Study Visualizations Generated ===")
    
    # Write a quick text log of insights for reference
    with open("Reports/blaze_case_study_summary.txt", "w") as f:
        f.write(f"=== CASE STUDY REPORT: STUDENT BM EXCEL BLAZE (22D41A7210) ===\n")
        f.write(f"Program: B.Tech in Artificial Intelligence & Data Science\n")
        f.write(f"Historical SGPAs:\n")
        for sem, sgpa in zip(semesters, sgpas):
            f.write(f"  Semester {sem}: {sgpa:.2f}\n")
        f.write(f"Current CGPA: {overall_cgpa:.2f}\n")
        f.write(f"Predicted Semester 8 SGPA: {predicted_sem8_sgpa:.2f}\n")
        f.write(f"Historical Course Stats:\n")
        f.write(f"  Total Courses Completed: {total_courses}\n")
        f.write(f"  Average Internal Marks: {avg_internal:.2f}\n")
        f.write(f"  Average External Marks: {avg_external:.2f}\n")
        f.write(f"Grade Breakdown:\n")
        for g, count in grade_counts.items():
            f.write(f"  {g}: {count}\n")
            
    print("Saved blaze_case_study_summary.txt")

if __name__ == "__main__":
    analyze_blaze_records()
