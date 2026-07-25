import os
import time

def main():
    print("="*40)
    print(" STARTING JOB ANALYSIS PIPELINE")
    print("="*40)

    print("\n[1/3] Fetching latest jobs from API...")
    os.system("python main.py")
    time.sleep(1)

    print("\n[2/3] Analyzing market trends...")
    os.system("python analyzer.py")
    time.sleep(1)

    print("\n[3/3] Generating your personalized Top 3...")
    os.system("python recommender.py")

    print("\n" + "="*40)
    print("✅ PIPELINE COMPLETE. Check your CSV files for details.")
    print("="*40)

if __name__ == "__main__":
    main()