import csv

def save_to_csv(job_list, filename="jobs_rwanda.csv"):
    """
    Saves a list of job dictionaries to a CSV file.
    """
    if not job_list:
        print("No data available to save.")
        return

    fieldnames = [
        'job_title', 
        'employer_name', 
        'job_city', 
        'job_is_remote', 
        'job_apply_link', 
        'job_description' # <-- INDISPENSABLE pour l'analyse
    ]

    try:
        with open(filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames, extrasaction='ignore')
            writer.writeheader()
            writer.writerows(job_list)
        print(f"✅ Data successfully saved to {filename}")
    except Exception as e:
        print(f"❌ Error during export: {e}")