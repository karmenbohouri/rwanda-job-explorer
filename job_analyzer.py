import os
import requests
from dotenv import load_dotenv

load_dotenv(override=True)

def fetch_job_listings(query="Python Developer", location="Rwanda"):
    """
    Connects to JSearch API to retrieve job postings based on query and location.
    """
    api_key = os.getenv('RAPIDAPI_KEY')
    api_host = "jsearch.p.rapidapi.com"
    url = f"https://{api_host}/search-v2"

    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": api_host
    }

    params = {
        "query": f"{query} in {location}",
        "num_pages": "1",
        "date_posted": "all",
        "country": "us"
    }

    try:
        print(f"Connecting to API for: {query} in {location}...")
        response = requests.get(url, headers=headers, params=params)

        response.raise_for_status()

        data = response.json()
        return data.get('data', {}).get('jobs', [])

    except Exception as error:
        print(f"An error occurred: {error}")
        try:
            print(f"Response body: {response.text}")
        except Exception:
            pass
        return []

if __name__ == "__main__":
    # Test with a broader search to get more results
    job_results = fetch_job_listings(query="Developer", location="Rwanda")

    if job_results:
        print(f"\n✅ Success! Found {len(job_results)} jobs.")
        print("-" * 50)

        for index, job in enumerate(job_results, 1):
            title = job.get('job_title', 'N/A')
            company = job.get('employer_name', 'N/A')
            is_remote = "Yes" if job.get('job_is_remote') else "No"
            link = job.get('job_apply_link', 'No link available')

            print(f"{index}. {title}")
            print(f"   Company: {company}")
            print(f"   Remote:  {is_remote}")
            print(f"   Link:    {link}")
            print("-" * 50)
    else:
        print("❌ No jobs found for this search.")