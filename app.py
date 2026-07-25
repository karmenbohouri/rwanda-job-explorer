from flask import Flask, render_template_string, request, send_file
from exporter import save_to_csv
from job_analyzer import fetch_job_listings
from filters import filter_remote_jobs, filter_by_employment_type
import os

app = Flask(__name__)

CATEGORIES = [
    {"name": "Technology", "icon": "&lt;/&gt;", "query": "Developer"},
    {"name": "Finance", "icon": "&#128200;", "query": "Accountant"},
    {"name": "Marketing", "icon": "&#128227;", "query": "Marketing"},
    {"name": "Healthcare", "icon": "&#10084;", "query": "Nurse"},
    {"name": "Education", "icon": "&#127891;", "query": "Teacher"},
    {"name": "Sales", "icon": "&#128722;", "query": "Sales"},
]

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Rwanda Job Market Explorer</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body { font-family: 'Inter', sans-serif; background: #f4f6fb; color: #1a1a2e; }
    a { text-decoration: none; }

    .navbar {
        display: flex; justify-content: space-between; align-items: center;
        padding: 20px 60px; background: #0b0f2b;
    }
    .logo { font-size: 1.3em; font-weight: 800; color: #fff; }
    .logo span { color: #5b7fff; }
    .nav-links { display: flex; gap: 28px; }
    .nav-links a { color: #cfd3e6; font-size: 0.92em; font-weight: 500; }
    .nav-links a.active { color: #5b7fff; }
    .nav-actions { display: flex; gap: 12px; align-items: center; }
    .btn-outline {
        padding: 9px 18px; border: 1px solid #3a3f66; border-radius: 6px;
        color: #fff; font-size: 0.85em; font-weight: 500; cursor: pointer; background: transparent;
    }
    .btn-solid {
        padding: 9px 18px; border: none; border-radius: 6px;
        background: #5b7fff; color: #fff; font-size: 0.85em; font-weight: 600; cursor: pointer;
    }
    .lang-toggle {
        display: flex; background: #171c40; border-radius: 6px; padding: 3px; gap: 2px;
    }
    .lang-toggle button {
        border: none; background: transparent; color: #9096b8; padding: 6px 10px;
        border-radius: 5px; font-size: 0.8em; font-weight: 600; cursor: pointer;
    }
    .lang-toggle button.active { background: #5b7fff; color: #fff; }

    .hero {
        background: radial-gradient(circle at top right, #1c2350 0%, #0b0f2b 60%);
        padding: 60px 60px 40px;
        text-align: center;
        position: relative;
        overflow: hidden;
    }
    .hero h1 { color: #fff; font-size: 2.4em; font-weight: 800; line-height: 1.3; }
    .hero h1 .accent { color: #5b7fff; }
    .hero p.subtitle { color: #a9aecb; margin: 14px 0 30px; font-size: 1em; }

    .search-panel {
        max-width: 980px; margin: 0 auto;
        background: #fff; border-radius: 10px; padding: 14px;
        display: flex; gap: 10px; align-items: center; flex-wrap: wrap;
        box-shadow: 0 20px 50px rgba(0,0,0,0.3);
    }
    .search-panel input[type="text"] {
        flex: 2; min-width: 200px; border: none; padding: 12px; font-size: 0.95em; outline: none;
    }
    .search-panel select {
        flex: 1; min-width: 140px; border: 1px solid #e2e4ee; border-radius: 6px; padding: 12px; font-size: 0.9em; color: #444;
    }
    .search-panel button.search-btn {
        background: #5b7fff; color: #fff; border: none; padding: 13px 24px;
        border-radius: 6px; font-weight: 600; cursor: pointer; font-size: 0.9em;
    }
    .options-row {
        max-width: 980px; margin: 14px auto 0; display: flex; justify-content: space-between; color: #cfd3e6; font-size: 0.85em;
    }
    .options-row label { display: flex; align-items: center; gap: 6px; color: #cfd3e6; }
    .options-row a { color: #cfd3e6; }

    .stats-bar {
        max-width: 980px; margin: 30px auto 0; background: #12173a; border: 1px solid #262c58;
        border-radius: 10px; display: flex; justify-content: space-around; padding: 22px 10px; flex-wrap: wrap;
    }
    .stat { text-align: center; color: #fff; padding: 6px 14px; }
    .stat .num { font-size: 1.4em; font-weight: 800; }
    .stat .label { font-size: 0.78em; color: #a9aecb; }

    .content { max-width: 1080px; margin: 0 auto; padding: 40px 30px 80px; }
    .section-header {
        display: flex; justify-content: space-between; align-items: center; margin-bottom: 18px;
    }
    .section-header h2 { font-size: 1.2em; font-weight: 700; }
    .section-header a { color: #5b7fff; font-size: 0.85em; font-weight: 600; }

    .categories-grid {
        display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
        gap: 14px; margin-bottom: 45px;
    }
    .category-card {
        background: #fff; border: 1px solid #e7e9f2; border-radius: 10px; padding: 16px;
        display: flex; align-items: center; gap: 12px; cursor: pointer; transition: 0.2s;
    }
    .category-card:hover { border-color: #5b7fff; transform: translateY(-2px); }
    .category-icon {
        width: 42px; height: 42px; border-radius: 8px; background: #eef1ff;
        display: flex; align-items: center; justify-content: center; font-size: 1.1em;
    }
    .category-card .cat-name { font-weight: 600; font-size: 0.92em; }
    .category-card .cat-sub { font-size: 0.78em; color: #8a8fa8; }

    .job-card {
        background: #fff; border: 1px solid #e7e9f2; border-radius: 10px;
        padding: 20px; margin-bottom: 14px; display: flex; justify-content: space-between; align-items: center; gap: 16px;
        transition: 0.2s;
    }
    .job-card:hover { border-color: #5b7fff33; box-shadow: 0 8px 20px rgba(91,127,255,0.08); }
    .job-left { display: flex; gap: 14px; align-items: flex-start; }
    .job-logo {
        width: 46px; height: 46px; border-radius: 8px; background: #0b0f2b; color: #fff;
        display: flex; align-items: center; justify-content: center; font-weight: 700; font-size: 0.9em; flex-shrink: 0;
    }
    .job-title { font-weight: 700; font-size: 1em; }
    .job-meta { font-size: 0.82em; color: #8a8fa8; margin-top: 3px; }
    .job-tags { display: flex; gap: 8px; flex-wrap: wrap; margin-top: 8px; }
    .job-tag { background: #eef1ff; color: #5b7fff; font-size: 0.72em; font-weight: 600; padding: 4px 10px; border-radius: 12px; }
    .job-tag.remote { background: #e7f9ee; color: #1e9e5a; }
    .job-right { text-align: right; flex-shrink: 0; }
    .apply-link { color: #5b7fff; font-weight: 600; font-size: 0.85em; }
    .score-badge {
        display: inline-block; background: #fff3d6; color: #a8791a;
        font-size: 0.72em; font-weight: 700; padding: 3px 9px; border-radius: 10px; margin-left: 8px;
    }
    .no-results { text-align: center; color: #8a8fa8; font-style: italic; padding: 40px 0; }
</style>
</head>
<body>

<div class="navbar">
    <div class="logo">Rwanda Job Market <span>Explorer</span></div>
    <div class="nav-links">
        <a href="/" class="active" data-i18n="nav_home">Home</a>
        <a href="#" data-i18n="nav_jobs">Jobs</a>
        <a href="#" data-i18n="nav_companies">Companies</a>
        <a href="#" data-i18n="nav_salaries">Salaries</a>
        <a href="#" data-i18n="nav_resources">Resources</a>
        <a href="#" data-i18n="nav_about">About</a>
    </div>
    <div class="nav-actions">
        <div class="lang-toggle">
            <button id="lang-en" onclick="setLang('en')">EN</button>
            <button id="lang-fr" onclick="setLang('fr')">FR</button>
        </div>
        <button class="btn-outline" data-i18n="nav_signin">Sign in</button>
        <button class="btn-solid" data-i18n="nav_signup">Sign up</button>
    </div>
</div>

<div class="hero">
    <h1 data-i18n="hero_title_1">Explore opportunities.</h1>
    <h1 data-i18n="hero_title_2">Build your future in <span class="accent">Rwanda.</span></h1>
    <p class="subtitle" data-i18n="hero_subtitle">Search jobs, explore companies and discover the right career for you.</p>

    <form action="/search" method="get">
        <div class="search-panel">
            <input type="text" name="q" data-i18n-placeholder="search_placeholder" placeholder="Job title, keyword or company" value="{{ query or '' }}" required>
            <select name="emp_type">
                <option value="" data-i18n="type_all">Job Type</option>
                <option value="FULLTIME" {% if emp_type == 'FULLTIME' %}selected{% endif %} data-i18n="type_full">Full-time</option>
                <option value="PARTTIME" {% if emp_type == 'PARTTIME' %}selected{% endif %} data-i18n="type_part">Part-time</option>
                <option value="CONTRACTOR" {% if emp_type == 'CONTRACTOR' %}selected{% endif %} data-i18n="type_contract">Contractor</option>
                <option value="INTERN" {% if emp_type == 'INTERN' %}selected{% endif %} data-i18n="type_intern">Intern</option>
            </select>
            <select name="sort_by">
                <option value="relevance" {% if sort_by == 'relevance' %}selected{% endif %} data-i18n="sort_relevance">Relevance</option>
                <option value="title" {% if sort_by == 'title' %}selected{% endif %} data-i18n="sort_title">Title (A-Z)</option>
            </select>
            <button type="submit" class="search-btn" data-i18n="search_btn">🔍 Search Jobs</button>
        </div>
        <div class="options-row">
            <label><input type="checkbox" name="remote_only" value="1" {% if remote_only %}checked{% endif %}> <span data-i18n="remote_only">Remote only</span></label>
        </div>
    </form>

    {% if search_done %}
    <div class="stats-bar">
        <div class="stat"><div class="num">{{ results|length }}</div><div class="label" data-i18n="stat_found">Jobs Found</div></div>
        <div class="stat"><div class="num">{{ remote_count }}</div><div class="label" data-i18n="stat_remote">Remote Jobs</div></div>
        <div class="stat"><div class="num">{{ company_count }}</div><div class="label" data-i18n="stat_companies">Companies</div></div>
    </div>
    {% endif %}
</div>

<div class="content">
    <div class="section-header">
        <h2 data-i18n="cat_title">Popular Categories</h2>
    </div>
    <div class="categories-grid">
        {% for cat in categories %}
        <form action="/search" method="get" style="margin:0;">
            <input type="hidden" name="q" value="{{ cat.query }}">
            <button type="submit" class="category-card" style="width:100%; text-align:left; border:1px solid #e7e9f2; font-family: inherit;">
                <div class="category-icon">{{ cat.icon|safe }}</div>
                <div>
                    <div class="cat-name">{{ cat.name }}</div>
                </div>
            </button>
        </form>
        {% endfor %}
    </div>

    <div class="section-header">
        {% if search_done %}
        <h2><span data-i18n="results_title">Results</span> for "{{ query }}"</h2>
        {% if results %}
        <a href="/export?q={{ query }}&remote_only={{ '1' if remote_only else '' }}&emp_type={{ emp_type }}" data-i18n="export_csv">⬇ Export CSV</a>
        {% endif %}
        {% else %}
        <h2 data-i18n="latest_title">Latest Opportunities</h2>
        {% endif %}
    </div>

    {% if results %}
        {% for job in results %}
        <div class="job-card">
            <div class="job-left">
                <div class="job-logo">{{ job.employer_name[:2]|upper if job.employer_name else "JB" }}</div>
                <div>
                    <div class="job-title">{{ job.job_title }}{% if job.relevance_score is defined %}<span class="score-badge">{{ job.relevance_score }} pts</span>{% endif %}</div>
                    <div class="job-meta">{{ job.employer_name }} &middot; {{ job.job_city or 'Rwanda' }}</div>
                    <div class="job-tags">
                        {% if job.job_is_remote %}<span class="job-tag remote" data-i18n="tag_remote">Remote</span>{% endif %}
                        {% if job.job_employment_type %}<span class="job-tag">{{ job.job_employment_type }}</span>{% endif %}
                    </div>
                </div>
            </div>
            <div class="job-right">
                <a href="{{ job.job_apply_link }}" target="_blank" class="apply-link" data-i18n="apply_now">Apply Now →</a>
            </div>
        </div>
        {% endfor %}
    {% elif search_done %}
        <p class="no-results" data-i18n="no_results">No results found for your search. Please try another keyword or filter.</p>
    {% else %}
        <p class="no-results" data-i18n="start_search">Use the search bar above to discover job opportunities in Rwanda.</p>
    {% endif %}
</div>

<script>
const translations = {
    en: {
        nav_home: "Home", nav_jobs: "Jobs", nav_companies: "Companies", nav_salaries: "Salaries",
        nav_resources: "Resources", nav_about: "About", nav_signin: "Sign in", nav_signup: "Sign up",
        hero_title_1: "Explore opportunities.", hero_title_2: 'Build your future in <span class="accent">Rwanda.</span>',
        hero_subtitle: "Search jobs, explore companies and discover the right career for you.",
        search_placeholder: "Job title, keyword or company",
        type_all: "Job Type", type_full: "Full-time", type_part: "Part-time", type_contract: "Contractor", type_intern: "Intern",
        sort_relevance: "Relevance", sort_title: "Title (A-Z)",
        search_btn: "🔍 Search Jobs", remote_only: "Remote only",
        stat_found: "Jobs Found", stat_remote: "Remote Jobs", stat_companies: "Companies",
        cat_title: "Popular Categories", latest_title: "Latest Opportunities", results_title: "Results",
        tag_remote: "Remote", apply_now: "Apply Now →",
        no_results: "No results found for your search. Please try another keyword or filter.",
        start_search: "Use the search bar above to discover job opportunities in Rwanda.",
        export_csv: "⬇ Export CSV",
    },
    fr: {
        nav_home: "Accueil", nav_jobs: "Emplois", nav_companies: "Entreprises", nav_salaries: "Salaires",
        nav_resources: "Ressources", nav_about: "À propos", nav_signin: "Connexion", nav_signup: "Inscription",
        hero_title_1: "Explorez les opportunités.", hero_title_2: 'Construisez votre avenir au <span class="accent">Rwanda.</span>',
        hero_subtitle: "Recherchez des emplois, explorez des entreprises et trouvez la carrière qui vous correspond.",
        search_placeholder: "Titre du poste, mot-clé ou entreprise",
        type_all: "Type d'emploi", type_full: "Temps plein", type_part: "Temps partiel", type_contract: "Contractuel", type_intern: "Stage",
        sort_relevance: "Pertinence", sort_title: "Titre (A-Z)",
        search_btn: "🔍 Rechercher", remote_only: "Télétravail uniquement",
        stat_found: "Offres trouvées", stat_remote: "Offres à distance", stat_companies: "Entreprises",
        cat_title: "Catégories populaires", latest_title: "Dernières opportunités", results_title: "Résultats",
        tag_remote: "Télétravail", apply_now: "Postuler →",
        no_results: "Aucun résultat pour votre recherche. Essayez un autre mot-clé ou filtre.",
        start_search: "Utilisez la barre de recherche ci-dessus pour découvrir des offres au Rwanda.",
        export_csv: "⬇ Exporter en CSV",
    }
};

function setLang(lang) {
    document.querySelectorAll('[data-i18n]').forEach(el => {
        const key = el.getAttribute('data-i18n');
        if (translations[lang][key]) el.innerHTML = translations[lang][key];
    });
    document.querySelectorAll('[data-i18n-placeholder]').forEach(el => {
        const key = el.getAttribute('data-i18n-placeholder');
        if (translations[lang][key]) el.placeholder = translations[lang][key];
    });
    document.getElementById('lang-en').classList.toggle('active', lang === 'en');
    document.getElementById('lang-fr').classList.toggle('active', lang === 'fr');
    localStorage.setItem('site_lang', lang);
}

const savedLang = localStorage.getItem('site_lang') || 'en';
setLang(savedLang);
</script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE, categories=CATEGORIES)

@app.route('/search')
def search():
    query = request.args.get('q', '')
    location = "Rwanda"
    remote_only = request.args.get('remote_only') == '1'
    emp_type = request.args.get('emp_type', '')
    sort_by = request.args.get('sort_by', 'relevance')

    raw_jobs = fetch_job_listings(query=query, location=location)

    if remote_only:
        raw_jobs = filter_remote_jobs(raw_jobs)
    if emp_type:
        raw_jobs = filter_by_employment_type(raw_jobs, emp_type)

    for job in raw_jobs:
        score = 0
        title = (job.get('job_title') or '').lower()
        desc = (job.get('job_description') or '').lower()
        if query.lower() in title:
            score += 5
        if job.get('job_is_remote'):
            score += 3
        if 'python' in title or 'python' in desc:
            score += 2
        job['relevance_score'] = score

    if sort_by == 'title':
        raw_jobs.sort(key=lambda j: (j.get('job_title') or '').lower())
    else:
        raw_jobs.sort(key=lambda j: j.get('relevance_score', 0), reverse=True)

    remote_count = sum(1 for j in raw_jobs if j.get('job_is_remote'))
    company_count = len(set(j.get('employer_name') for j in raw_jobs if j.get('employer_name')))

    return render_template_string(
        HTML_TEMPLATE,
        results=raw_jobs,
        query=query,
        search_done=True,
        remote_only=remote_only,
        emp_type=emp_type,
        sort_by=sort_by,
        remote_count=remote_count,
        company_count=company_count,
        categories=CATEGORIES
    )

@app.route('/export')
def export():
    query = request.args.get('q', '')
    location = "Rwanda"
    remote_only = request.args.get('remote_only') == '1'
    emp_type = request.args.get('emp_type', '')

    raw_jobs = fetch_job_listings(query=query, location=location)

    if remote_only:
        raw_jobs = filter_remote_jobs(raw_jobs)
    if emp_type:
        raw_jobs = filter_by_employment_type(raw_jobs, emp_type)

    filename = f"jobs_{query.replace(' ', '_')}.csv"
    filepath = f"/tmp/{filename}"
    save_to_csv(raw_jobs, filename=filepath)

    return send_file(filepath, as_attachment=True, download_name=filename)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)