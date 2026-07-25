import csv
from collections import Counter

def analyze_skills(filename="all_jobs_rwanda.csv"):
    # Une liste plus large de compétences à traquer
    skills_to_track = [
        'Python', 'JavaScript', 'React', 'Node', 'SQL', 'PostgreSQL',
        'Java', 'PHP', 'Docker', 'AWS', 'Mobile', 'API', 'Odoo', 
        'Django', 'Flask', 'Git', 'HTML', 'CSS', 'NoSQL', 'Linux'
    ]
    
    skill_counts = Counter()
    total_jobs = 0

    try:
        with open(filename, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                total_jobs += 1
                content = (row.get('job_title', '') + " " + row.get('job_description', '')).lower()
                
                for skill in skills_to_track:
                    if skill.lower() in content:
                        skill_counts[skill] += 1
        
        print(f"\n---  Deep Market Analysis: {total_jobs} jobs scanned ---")
        if not skill_counts:
            print("No specific skills detected. Check if descriptions are empty.")
        else:
            print("Top Skills Demanded in Rwanda (Title + Description):")
            for skill, count in skill_counts.most_common():
                percentage = (count / total_jobs) * 100
                print(f"- {skill}: {count} jobs ({percentage:.1f}%)")
                
    except FileNotFoundError:
        print(f"❌ Error: {filename} not found. Run main.py first!")

if __name__ == "__main__":
    analyze_skills()