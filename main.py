from job_analyzer import fetch_job_listings
from filters import filter_remote_jobs
from exporter import save_to_csv 

if __name__ == "__main__":
    target_job = "Developer"
    target_location = "Rwanda"
    
    print(f"--- Fetching and Exporting Jobs in {target_location} ---")
    
    # 1. Fetch
    raw_jobs = fetch_job_listings(query=target_job, location=target_location)
    
    if raw_jobs:
        # 2. Display summary in terminal
        print(f"✅ {len(raw_jobs)} jobs found.")
        
        # 3. Export to CSV
        save_to_csv(raw_jobs, "all_jobs_rwanda.csv")
        
        # 4. Export Remote jobs only
        remote_jobs = filter_remote_jobs(raw_jobs)
        if remote_jobs:
            save_to_csv(remote_jobs, "remote_only_rwanda.csv")
            print(f" {len(remote_jobs)} remote jobs isolated in a separate file.")
    else:
        print("No data found.")