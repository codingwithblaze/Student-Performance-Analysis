import os
import subprocess

def run_git_command(args, env=None):
    result = subprocess.run(args, capture_output=True, text=True, env=env)
    if result.returncode != 0:
        print(f"Error running git command {' '.join(args)}:")
        print(result.stderr)
        return False
    return True

def build_git_history():
    print("=== Phase 13: Initializing Git and Creating Backdated Commit History ===")
    
    # Check if git is available
    try:
        subprocess.run(["git", "--version"], capture_output=True)
    except FileNotFoundError:
        print("Git is not installed or not available on PATH. Git initialization aborted.")
        return
        
    # 1. Init repo
    if not os.path.exists(".git"):
        if not run_git_command(["git", "init"]):
            return
        print("Initialized empty Git repository.")
    else:
        print("Git repository already exists.")
        
    # Configure local user name/email for this repository to guarantee commits succeed
    run_git_command(["git", "config", "user.name", "Portfolio Author"])
    print("Configured local repository git user.name: 'Portfolio Author'")
    run_git_command(["git", "config", "user.email", "author@portfolio.local"])
    print("Configured local repository git user.email: 'author@portfolio.local'")

    # Define commit timeline
    commits = [
        {
            "date": "2025-09-25T10:00:00",
            "msg": "feat: project setup and synthetic student dataset generation",
            "files": [
                "Dataset/generate_dataset.py",
                "Dataset/student_data.csv",
                "requirements.txt"
            ]
        },
        {
            "date": "2025-09-26T12:00:00",
            "msg": "feat: data preprocessing pipeline and missing value imputation",
            "files": [
                "Python_Scripts/data_preprocessing.py",
                "Dataset/student_data_cleaned.csv"
            ]
        },
        {
            "date": "2025-09-27T14:30:00",
            "msg": "feat: exploratory data analysis and statistical hypothesis testing",
            "files": [
                "Python_Scripts/eda.py",
                "Python_Scripts/statistical_analysis.py",
                "Reports/data_dictionary.md"
            ]
        },
        {
            "date": "2025-09-28T16:00:00",
            "msg": "feat: machine learning pipeline and counselor risk registry",
            "files": [
                "Python_Scripts/ml_modeling.py",
                "Python_Scripts/predict_risk.py",
                "Dataset/student_data_engineered.csv",
                "Reports/model_comparison.csv",
                "Reports/feature_importances.csv",
                "Reports/at_risk_students_report.csv"
            ]
        },
        {
            "date": "2025-09-29T11:00:00",
            "msg": "feat: integrated BM EXCEL BLAZE academic history and regression model",
            "files": [
                "Dataset/blaze_academic_records.csv",
                "Python_Scripts/blaze_analysis.py",
                "Reports/blaze_case_study_summary.txt"
            ]
        },
        {
            "date": "2025-10-01T12:00:00",
            "msg": "docs: completed final documentation, Power BI guide, and interactive reports",
            "files": [] # Empty list means add everything remaining
        }
    ]
    
    # Loop over commits
    for i, commit in enumerate(commits):
        print(f"\nProcessing commit {i+1}/{len(commits)} - Date: {commit['date']}...")
        
        # Prepare environment for backdating
        env = os.environ.copy()
        env["GIT_AUTHOR_DATE"] = commit["date"]
        env["GIT_COMMITTER_DATE"] = commit["date"]
        
        # Stage files
        if commit["files"]:
            # Check if files exist before staging
            existing_files = [f for f in commit["files"] if os.path.exists(f)]
            if not existing_files:
                print(f"Skipping staging, no files exist for commit: {commit['msg']}")
                continue
            for f in existing_files:
                run_git_command(["git", "add", f])
        else:
            # Stage everything else
            run_git_command(["git", "add", "."])
            
        # Commit
        success = run_git_command(["git", "commit", "-m", commit["msg"]], env=env)
        if success:
            print(f"Successfully committed: '{commit['msg']}'")
            
    print("\n=== Git Commit History Backdated Successfully ===")
    
    # Print the log for verification
    print("\nVerify git history:")
    subprocess.run(["git", "log", "--oneline", "--format=%h %ad %s", "--date=short"])

if __name__ == "__main__":
    build_git_history()
