def filter_remote_jobs(job_list):
    """
    Returns only jobs where 'job_is_remote' is True.
    """
    return [job for job in job_list if job.get('job_is_remote') is True]

def filter_by_employment_type(job_list, emp_type="FULLTIME"):
    """
    Filters jobs by type. 
    Options: 'FULLTIME', 'PARTTIME', 'CONTRACTOR', 'INTERN'.
    """
    return [job for job in job_list if job.get('job_employment_type') == emp_type]

def filter_by_keyword(job_list, keyword):
    """
    Search for a specific keyword in the job title or description.
    """
    keyword = keyword.lower()
    return [job for job in job_list if keyword in job.get('job_title', '').lower() or keyword in job.get('job_description', '').lower()]

import re

def clean_text(text):
    """
    Removes HTML tags and special characters from a string.
    """
    if not text:
        return ""
    # Remove HTML tags
    clean = re.compile('<.*?>')
    text = re.sub(clean, '', text)
    # Replace common HTML entities
    text = text.replace('&nbsp;', ' ').replace('&amp;', '&')
    return text.strip()