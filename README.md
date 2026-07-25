# 🇷🇼 Rwanda Job Market Explorer

Welcome to the **Rwanda Job Market Explorer**, a Flask-based web application that lets users search, filter, and export real-time job listings in Rwanda. Built as part of my **System Engineering & DevOps** curriculum at ALU/Holberton.

🎥 **Demo video:** https://youtu.be/pcPO2MM3JEw
🌐 **Live site:** https://35.175.242.143 (self-signed certificate, click "Advanced > Proceed" to view)

---

## ✨ Features

- Real-time job search powered by the [JSearch API](https://rapidapi.com/letscrape-6bRBa3QguO5/api/jsearch) (RapidAPI)
- Filter by remote-only and employment type (Full-time, Part-time, Contractor, Intern)
- Sort results by relevance score or job title
- Bilingual interface (English / French) with instant switching
- Export search results to CSV
- Modern, responsive UI inspired by leading job board platforms
- Deployed on a high-availability infrastructure with load balancing

---

## 📁 Project Structure

```
job_analyzer_project/
├── app.py                    # Flask web application (main entry point)
├── job_analyzer.py           # Core function: fetches job listings from the JSearch API
├── filters.py                 # Filtering functions (remote jobs, employment type, keyword)
├── analyzer.py                 # CLI helper for analyzing fetched job data
├── recommender.py             # CLI tool: scores and ranks jobs from a saved CSV
├── exporter.py                 # Reusable CSV export function (used by web app and CLI)
├── main.py                     # CLI entry point: fetches and saves job data
├── run_all.py                  # Runs the full CLI pipeline (fetch → filter → export)
├── all_jobs_rwanda.csv         # Sample exported dataset
├── remote_only_rwanda.csv      # Sample filtered dataset (remote jobs only)
├── requirements.txt             # Python dependencies
└── README.md                    # This file
```

## 🌐 Infrastructure & Deployment

The application runs on a redundant infrastructure to ensure uptime:

| Role | Address |
|---|---|
| Load Balancer (Lb01) | `35.175.242.143` (single entry point) |
| Web Server 01 | `32.192.231.221` |
| Web Server 02 | `98.93.200.142` |

**How it works:**
- Each web server runs the Flask app on port `5000`, managed via `nohup` in the background.
- Nginx runs on port `80` on each server and reverse-proxies requests to `localhost:5000`.
- HAProxy on Lb01 load-balances traffic between both web servers using the **round-robin** algorithm, and terminates SSL for the domain `51karmenbohouri.tech`.

To verify load balancing is working, you can check the `X-Served-By` response header — it alternates between `7059-web-01` and `7059-web-02` on successive requests.

---

## 🛠️ Local Installation

1. **Clone the repository**
```bash
   git clone https://github.com/karmenbohouri/rwanda-job-explorer.git
   cd rwanda-job-explorer
```

2. **Create a virtual environment and install dependencies**
```bash
   python -m venv .venv
   source .venv/bin/activate   # On Windows: .venv\Scripts\activate
   pip install -r requirements.txt
```

3. **Set up your API key**

   Create a `.env` file at the root of the project: