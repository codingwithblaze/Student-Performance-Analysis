import os
import pickle
import numpy as np
import pandas as pd

def run_risk_prediction(data_path="Dataset/student_data_engineered.csv", model_path="Python_Scripts/best_model.pkl"):
    print("=== Phase 9: Starting Student Risk Prediction & Intervention Logging ===")
    
    # Load dataset
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Engineered dataset not found at {data_path}. Run ML pipeline first.")
    df = pd.read_csv(data_path)
    
    # Load model
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Best model pickle not found at {model_path}. Run ML pipeline first.")
    with open(model_path, "rb") as f:
        model = pickle.load(f)
        
    print(f"Loaded trained pipeline: {model.steps[-1][0]} model.")
    
    # Prepare data for prediction (dropping columns that aren't features)
    drop_cols = ["Student_ID", "Final_Exam_Score", "Pass_Fail_Status", "Performance_Grade"]
    features_df = df.drop(columns=drop_cols)
    
    # Generate predictions using the model
    predicted_scores = model.predict(features_df)
    df["Predicted_Exam_Score"] = np.clip(np.round(predicted_scores), 0, 100).astype(int)
    
    # Determine risk category based on predicted score and actual metrics
    # High Risk: Predicted Score < 55 or Attendance < 75%
    # Medium Risk: Predicted Score 55-65
    # Low Risk: Predicted Score >= 65
    def classify_risk(row):
        score = row["Predicted_Exam_Score"]
        att = row["Attendance_Percentage"]
        prev = row["Previous_Grades"]
        
        if score < 55.0 or att < 75.0 or prev < 55.0:
            return "High"
        elif score < 65.0 or att < 85.0 or prev < 65.0:
            return "Medium"
        else:
            return "Low"
            
    df["Risk_Intervention_Level"] = df.apply(classify_risk, axis=1)
    
    # Generate risk factors and action recommendations
    def generate_recommendations(row):
        factors = []
        actions = []
        
        # Check attendance
        if row["Attendance_Percentage"] < 75.0:
            factors.append("Critical low attendance (<75%)")
            actions.append("Mandatory attendance review meeting with parents. Daily attendance check-ins.")
        elif row["Attendance_Percentage"] < 85.0:
            factors.append("Borderline attendance (75%-85%)")
            actions.append("Counselor check-in to identify attendance obstacles. Attendance target set.")
            
        # Check study hours
        if row["Study_Hours"] < 2.5:
            factors.append("Low study hours (<2.5 hrs/day)")
            actions.append("Enroll in supervised study hall (2 hours/week). Provide study planning guide.")
            
        # Check previous grades
        if row["Previous_Grades"] < 60.0:
            factors.append("Weak academic foundation (Previous grade <60)")
            actions.append("Provide remedial tutoring in core subjects. Assign peer study group.")
            
        # Overall predictions
        if row["Predicted_Exam_Score"] < 60:
            factors.append("Predicted to fail exam (<60 score)")
            actions.append("Diagnostic test to identify learning gaps. Weekly progress review by subject teachers.")
            
        if not factors:
            factors.append("None identified")
            actions.append("Maintain current study routines. Continue participation in extra-curricular activities.")
            
        return "; ".join(factors), " | ".join(actions)

    rec_tuples = df.apply(generate_recommendations, axis=1)
    df["Primary_Risk_Drivers"] = [t[0] for t in rec_tuples]
    df["Action_Plan"] = [t[1] for t in rec_tuples]
    
    # Filter for at-risk students (High and Medium risk levels)
    at_risk_df = df[df["Risk_Intervention_Level"].isin(["High", "Medium"])].copy()
    
    # Sort by Predicted Exam Score ascending (lowest score first = higher priority)
    at_risk_df = at_risk_df.sort_values(by="Predicted_Exam_Score").reset_index(drop=True)
    
    # Export full risk registry
    columns_to_export = [
        "Student_ID", "Gender", "Age", "Attendance_Percentage", "Study_Hours", 
        "Previous_Grades", "Parent_Education", "Risk_Intervention_Level", 
        "Predicted_Exam_Score", "Primary_Risk_Drivers", "Action_Plan"
    ]
    
    os.makedirs("Reports", exist_ok=True)
    at_risk_df[columns_to_export].to_csv("Reports/at_risk_students_report.csv", index=False)
    print(f"Risk analysis complete. Flagged {len(at_risk_df)} students at risk (High/Medium).")
    print(f"At-risk student intervention report saved to 'Reports/at_risk_students_report.csv'.")
    
    # Summary printing
    risk_counts = df["Risk_Intervention_Level"].value_counts()
    print("\n--- Summary of Student Risk Distribution ---")
    for r_level in ["High", "Medium", "Low"]:
        cnt = risk_counts.get(r_level, 0)
        pct = (cnt / len(df)) * 100
        print(f"  {r_level:6s} Risk: {cnt:4d} students ({pct:.1f}%)")
        
    print("\nSample of At-Risk Students requiring intervention:")
    print(at_risk_df[columns_to_export].head(5).to_string())
    
    print("=== Risk Prediction & Intervention Logging Completed ===")
    return df

if __name__ == "__main__":
    run_risk_prediction()
