import os
import pickle
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# Try to import xgboost, fall back if not available
try:
    import xgboost as xgb
    XGBOOST_AVAILABLE = True
except ImportError:
    XGBOOST_AVAILABLE = False

def engineer_features(df):
    """
    Applies custom feature engineering to the raw dataset.
    """
    df = df.copy()
    
    # 1. Attendance Category
    def get_attendance_category(p):
        if p < 75.0: return "Critical"
        elif p < 85.0: return "Borderline"
        elif p < 95.0: return "Good"
        else: return "Excellent"
        
    df["Attendance_Category"] = df["Attendance_Percentage"].apply(get_attendance_category)
    
    # 2. Study Efficiency Index (study hours weighted by attendance percentage)
    df["Study_Efficiency_Index"] = df["Study_Hours"] * (df["Attendance_Percentage"] / 100.0)
    
    # 3. Risk Level (heuristic based on pre-exam features)
    def get_risk_level(row):
        score = 0
        if row["Attendance_Percentage"] < 75.0: score += 2
        elif row["Attendance_Percentage"] < 85.0: score += 1
        
        if row["Previous_Grades"] < 55.0: score += 2
        elif row["Previous_Grades"] < 65.0: score += 1
        
        if row["Study_Hours"] < 2.0: score += 1
        
        if score >= 3: return "High"
        elif score >= 1: return "Medium"
        else: return "Low"
        
    df["Risk_Level"] = df.apply(get_risk_level, axis=1)
    
    # 4. Performance Grade (derived from exam score, used for target-profile classification)
    def get_grade(score):
        if score >= 90: return "O"
        elif score >= 80: return "A+"
        elif score >= 70: return "A"
        elif score >= 60: return "B+"
        elif score >= 50: return "B"
        elif score >= 40: return "C"
        else: return "F"
        
    df["Performance_Grade"] = df["Final_Exam_Score"].apply(get_grade)
    
    return df

def run_ml_pipeline(input_path="Dataset/student_data_cleaned.csv"):
    print("=== Phase 7 & 8: Starting Feature Engineering & ML Pipeline ===")
    
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Cleaned dataset not found at {input_path}")
        
    df_raw = pd.read_csv(input_path)
    
    # Apply feature engineering
    df = engineer_features(df_raw)
    df.to_csv("Dataset/student_data_engineered.csv", index=False)
    print("Feature engineering completed. Saved dataset to 'Dataset/student_data_engineered.csv'.")
    
    # Define features and target
    # We drop Student_ID (identifier), Final_Exam_Score (target), Pass_Fail_Status (directly derived from target),
    # and Performance_Grade (directly derived from target)
    target = "Final_Exam_Score"
    drop_cols = ["Student_ID", "Final_Exam_Score", "Pass_Fail_Status", "Performance_Grade"]
    
    X = df.drop(columns=drop_cols)
    y = df[target]
    
    # Identify numerical and categorical columns
    num_features = X.select_dtypes(include=['int64', 'float64']).columns.tolist()
    cat_features = X.select_dtypes(include=['object']).columns.tolist()
    
    print(f"Numerical Features ({len(num_features)}): {num_features}")
    print(f"Categorical Features ({len(cat_features)}): {cat_features}")
    
    # Split training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    print(f"Train size: {X_train.shape[0]}, Test size: {X_test.shape[0]}")
    
    # Define Preprocessor using Pipeline & ColumnTransformer
    # Scale numerical columns, One-hot encode categorical columns
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), num_features),
            ('cat', OneHotEncoder(handle_unknown='ignore', sparse_output=False), cat_features)
        ])
    
    # Define Models to Evaluate
    models = {
        "Linear Regression": LinearRegression(),
        "Decision Tree": DecisionTreeRegressor(random_state=42, max_depth=6),
        "Random Forest": RandomForestRegressor(random_state=42, n_estimators=100, max_depth=10),
        "Gradient Boosting": GradientBoostingRegressor(random_state=42, n_estimators=100, learning_rate=0.1)
    }
    
    if XGBOOST_AVAILABLE:
        print("XGBoost library detected. Adding XGBoost to model evaluation list.")
        models["XGBoost"] = xgb.XGBRegressor(random_state=42, n_estimators=100, max_depth=5, learning_rate=0.1)
    else:
        print("XGBoost library not found. Falling back to Scikit-Learn Gradient Boosting.")
        
    results = {}
    best_r2 = -float('inf')
    best_model_name = None
    best_pipeline = None
    
    print("\n--- Model Evaluation and Training ---")
    for name, model in models.items():
        # Create pipeline with preprocessing and estimator
        pipeline = Pipeline(steps=[
            ('preprocessor', preprocessor),
            ('regressor', model)
        ])
        
        # Train model
        pipeline.fit(X_train, y_train)
        
        # Make predictions
        y_pred = pipeline.predict(X_test)
        
        # Calculate metrics
        mae = mean_absolute_error(y_test, y_pred)
        mse = mean_squared_error(y_test, y_pred)
        rmse = np.sqrt(mse)
        r2 = r2_score(y_test, y_pred)
        
        results[name] = {
            "MAE": mae,
            "RMSE": rmse,
            "R2_Score": r2
        }
        
        print(f"{name:20s} | MAE: {mae:6.3f} | RMSE: {rmse:6.3f} | R2 Score: {r2:6.3f}")
        
        # Select best model based on R2 Score
        if r2 > best_r2:
            best_r2 = r2
            best_model_name = name
            best_pipeline = pipeline
            
    print(f"\n>>> Best Model: {best_model_name} with R2 Score of {best_r2:.4f} <<<")
    
    # Save the best model pipeline
    os.makedirs("Python_Scripts", exist_ok=True)
    with open("Python_Scripts/best_model.pkl", "wb") as f:
        pickle.dump(best_pipeline, f)
    print("Best model pipeline saved to 'Python_Scripts/best_model.pkl'.")
    
    # Create Comparison DataFrame and save
    comparison_df = pd.DataFrame(results).T
    os.makedirs("Reports", exist_ok=True)
    comparison_df.to_csv("Reports/model_comparison.csv")
    print("Model comparison metrics saved to 'Reports/model_comparison.csv'.")
    
    # Extract Feature Importances if available (from Random Forest or Gradient Boosting)
    print("\n--- Feature Importance Analysis ---")
    # Fit preprocessor on X_train to extract encoded feature names
    preprocessor.fit(X_train)
    # Extract feature names from encoder
    encoded_cat_names = preprocessor.named_transformers_['cat'].get_feature_names_out(cat_features).tolist()
    feature_names = num_features + encoded_cat_names
    
    if best_model_name in ["Random Forest", "Gradient Boosting", "XGBoost", "Decision Tree"]:
        importances = best_pipeline.named_steps['regressor'].feature_importances_
        imp_df = pd.DataFrame({
            "Feature": feature_names,
            "Importance": importances
        }).sort_values(by="Importance", ascending=False).reset_index(drop=True)
        
        print(imp_df.head(10).to_string())
        imp_df.to_csv("Reports/feature_importances.csv", index=False)
        print("Feature importances saved to 'Reports/feature_importances.csv'.")
    else:
        # If best is Linear Regression, get coefficients
        coefs = best_pipeline.named_steps['regressor'].coef_
        imp_df = pd.DataFrame({
            "Feature": feature_names,
            "Coefficient": coefs
        }).sort_values(by=lambda df: df["Coefficient"].abs(), ascending=False).reset_index(drop=True)
        print(imp_df.head(10).to_string())
        imp_df.to_csv("Reports/feature_importances.csv", index=False)
        print("Model coefficients saved to 'Reports/feature_importances.csv'.")
        
    print("=== Machine Learning Pipeline Execution Completed ===")
    return best_model_name, results

if __name__ == "__main__":
    run_ml_pipeline()
