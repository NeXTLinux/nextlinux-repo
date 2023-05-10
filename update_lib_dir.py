import os
import requests
import json

org_name = 'nextlinux'
lib_dir = 'libraries'

# Get the organization's repositories
headers = {
    'Authorization': f'token {os.environ["GITHUB_TOKEN"]}'
}
url = f'https://api.github.com/orgs/{org_name}/repos'
response = requests.get(url, headers=headers)
repos = json.loads(response.text)

# Iterate through the repositories
for repo in repos:
    # Check if the repository is a library
    if 'library' in repo.get('topics', []):
        # Check if the repository is already in the library directory
        repo_name = repo['name']
        lib_path = os.path.join(lib_dir, repo_name)
        if not os.path.exists(lib_path):
            # Clone the repository into the library directory
            os.system(f'git clone {repo["clone_url"]} {lib_path}')
            # Checkout the latest tag
            os.system(f'cd {lib_path} && git checkout $(git describe --tags $(git rev-list --tags --max-count=1))')
