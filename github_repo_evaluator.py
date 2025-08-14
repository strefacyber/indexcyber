import requests
import os

def get_github_headers():
    token = os.getenv("GITHUB_TOKEN")
    headers = {'Accept': 'application/vnd.github.v3+json'}
    if token:
        headers['Authorization'] = f'token {token}'
    return headers

def fetch_json(url, headers):
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"❌ Błąd pobierania {url}: {response.status_code}")
        return None

def get_repo_info(owner, repo):
    base_url = f"https://api.github.com/repos/{owner}/{repo}"
    headers = get_github_headers()

    repo_data = fetch_json(base_url, headers)
    if not repo_data:
        print("Nie udało się pobrać danych repozytorium.")
        return

    issues_data = fetch_json(f"{base_url}/issues?state=open&per_page=100", headers) or []
    pulls_data = fetch_json(f"{base_url}/pulls?state=open&per_page=100", headers) or []
    contributors_data = fetch_json(f"{base_url}/contributors?per_page=100", headers) or []
    commits_data = fetch_json(f"{base_url}/commits?per_page=1", headers) or []

    print(f"\n📘 Repozytorium: {repo_data.get('full_name', 'Brak')}")
    print(f"🌟 Gwiazdki: {repo_data.get('stargazers_count', 0)}")
    print(f"🍴 Forki: {repo_data.get('forks_count', 0)}")
    print(f"👥 Kontrybutorzy: {len(contributors_data)}")
    print(f"📄 Licencja: {repo_data.get('license', {}).get('name', 'Brak')}")
    last_commit = commits_data[0]['commit']['committer']['date'] if commits_data else 'Brak danych'
    print(f"🕒 Ostatni commit: {last_commit}")
    print(f"🐞 Otwarte issues: {len(issues_data)}")
    print(f"🔁 Otwarte PR: {len(pulls_data)}")
    print(f"📦 Wersje (releases): sprawdź ręcznie, API ma ograniczenia\n")

    score = 0
    if repo_data.get('stargazers_count', 0) > 100: score += 1
    if len(contributors_data) > 1: score += 1
    if len(issues_data) < 50: score += 1
    if len(pulls_data) < 20: score += 1
    if repo_data.get('license'): score += 1
    if commits_data: score += 1

    print(f"📊 Ocena jakości projektu: {score}/6\n")

# Przykład użycia:
if __name__ == "__main__":
    owner = input("Podaj nazwę właściciela repozytorium (owner): ")
    repo = input("Podaj nazwę repozytorium (repo): ")
    get_repo_info(owner, repo)
