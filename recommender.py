import csv

def score_jobs(filename="all_jobs_rwanda.csv"):
    scored_list = []
    
    try:
        with open(filename, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for job in reader:
                score = 0
                title = job.get('job_title', '').lower()
                desc = job.get('job_description', '').lower()
                is_remote = job.get('job_is_remote', 'False') == 'True'

                if 'python' in title or 'python' in desc: score += 5
                if is_remote: score += 3
                if 'git' in desc: score += 2
                if 'api' in desc: score += 1
                if 'junior' in title or 'intern' in title: score += 2 # Plus accessible !

                job['relevance_score'] = score
                scored_list.append(job)

        scored_list.sort(key=lambda x: x['relevance_score'], reverse=True)

        print("\n---  Top Job Recommendations for You ---")
        for job in scored_list[:3]: # On affiche le Top 3
            print(f"Score: {job['relevance_score']}/10 | {job['job_title']}")
            print(f"Company: {job['employer_name']} | Link: {job['job_apply_link'][:40]}...")
            print("-" * 40)

    except FileNotFoundError:
        print("Run main.py first to generate the data!")

if __name__ == "__main__":
    score_jobs()