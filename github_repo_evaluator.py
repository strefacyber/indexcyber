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
        return None

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

    # Wagi dla poszczególnych metryk (suma = 100)
    weights = {
        'stars': 25,
        'contributors': 20,
        'issues': 15,
        'pulls': 15,
        'license': 10,
        'commits': 15
    }

    score = 0
    # Gwiazdki: >100 = pełna waga, >50 = połowa wagi, inaczej 0
    stars = repo_data.get('stargazers_count', 0)
    if stars > 100:
        score += weights['stars']
    elif stars > 50:
        score += weights['stars'] * 0.5

    # Kontrybutorzy: >5 = pełna waga, >1 = połowa wagi, inaczej 0
    contributors = len(contributors_data)
    if contributors > 5:
        score += weights['contributors']
    elif contributors > 1:
        score += weights['contributors'] * 0.5

    # Issues: <20 = pełna waga, <50 = połowa wagi, inaczej 0
    issues = len(issues_data)
    if issues < 20:
        score += weights['issues']
    elif issues < 50:
        score += weights['issues'] * 0.5

    # Pull requests: <10 = pełna waga, <20 = połowa wagi, inaczej 0
    pulls = len(pulls_data)
    if pulls < 10:
        score += weights['pulls']
    elif pulls < 20:
        score += weights['pulls'] * 0.5

    # Licencja: obecna = pełna waga, brak = 0
    if repo_data.get('license'):
        score += weights['license']

    # Commity: obecny commit = pełna waga, brak = 0
    if commits_data:
        score += weights['commits']

    print(f"📊 Ocena jakości projektu: {int(score)}/100\n")

    # Zwróć dane do porównania
    return {
        "full_name": repo_data.get('full_name', 'Brak'),
        "score": int(score),
        "stars": stars,
        "contributors": contributors,
        "issues": issues,
        "pulls": pulls,
        "license": repo_data.get('license', {}).get('name', 'Brak'),
        "last_commit": last_commit
    }

def compare_repos(repo1, repo2):
    print("\n🔎 Porównanie projektów:")
    print(f"{repo1['full_name']} vs {repo2['full_name']}")
    print(f"Ocena: {repo1['score']}/100 vs {repo2['score']}/100")
    print(f"Gwiazdki: {repo1['stars']} vs {repo2['stars']}")
    print(f"Kontrybutorzy: {repo1['contributors']} vs {repo2['contributors']}")
    print(f"Otwarte issues: {repo1['issues']} vs {repo2['issues']}")
    print(f"Otwarte PR: {repo1['pulls']} vs {repo2['pulls']}")
    print(f"Licencja: {repo1['license']} vs {repo2['license']}")
    print(f"Ostatni commit: {repo1['last_commit']} vs {repo2['last_commit']}\n")

# Przykład użycia:
if __name__ == "__main__":
    previous_repo = None
    while True:
        owner = input("Podaj nazwę właściciela repozytorium (owner): ")
        repo = input("Podaj nazwę repozytorium (repo): ")
        current_repo = get_repo_info(owner, repo)
        if previous_repo and current_repo:
            compare_repos(previous_repo, current_repo)
        previous_repo = current_repo
        again = input("Czy chcesz sprawdzić inne repozytorium? (t/n): ")
        if again.lower() != "t":
            print("Koniec programu.")
            break
