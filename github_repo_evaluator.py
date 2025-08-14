import requests

def get_repo_info(owner, repo):
    base_url = f"https://api.github.com/repos/{owner}/{repo}"
    headers = {'Accept': 'application/vnd.github.v3+json'}

    repo_data = requests.get(base_url, headers=headers).json()
    issues_data = requests.get(base_url + "/issues?state=open", headers=headers).json()
    pulls_data = requests.get(base_url + "/pulls?state=open", headers=headers).json()
    contributors_data = requests.get(base_url + "/contributors", headers=headers).json()
    commits_data = requests.get(base_url + "/commits", headers=headers).json()

    print(f"\n📘 Repozytorium: {repo_data.get('full_name')}")
    print(f"🌟 Gwiazdki: {repo_data.get('stargazers_count')}")
    print(f"🍴 Forki: {repo_data.get('forks_count')}")
    print(f"👥 Kontrybutorzy: {len(contributors_data)}")
    print(f"📄 Licencja: {repo_data.get('license')['name'] if repo_data.get('license') else 'Brak'}")
    print(f"🕒 Ostatni commit: {commits_data[0]['commit']['committer']['date'] if commits_data else 'Brak danych'}")
    print(f"🐞 Otwarte issues: {len(issues_data)}")
    print(f"🔁 Otwarte PR: {len(pulls_data)}")
    print(f"📦 Wersje (releases): {repo_data.get('releases_url').count('/')} (sprawdź ręcznie, API ma ograniczenia)\n")

    # Prosta ocena jakości
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
    get_repo_info("psf", "requests")  # Zmień na dowolne repozytorium: "owner", "repo"
