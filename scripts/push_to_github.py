import sys
import os
from dulwich.repo import Repo
from dulwich.porcelain import add, commit, push, remote_add
from dulwich.client import get_transport_and_path

repo_path = "."
repo = Repo(repo_path)

if len(sys.argv) < 2:
    print("Usage: python scripts/push_to_github.py <GITHUB_REPO_URL_OR_TOKEN_URL>")
    print("Example: python scripts/push_to_github.py https://github.com/myuser/dream11-fantasy-app.git")
    print("Or with token: python scripts/push_to_github.py https://<TOKEN>@github.com/myuser/dream11-fantasy-app.git")
    sys.exit(1)

remote_url = sys.argv[1]

# Configure origin remote
config = repo.get_config()
config.set((b"remote", b"origin"), b"url", remote_url.encode("utf-8"))
config.set((b"remote", b"origin"), b"fetch", b"+refs/heads/*:refs/remotes/origin/*")
config.write_to_path()
print(f"Remote 'origin' set to: {remote_url}")

# Push main branch
print("Pushing to GitHub remote...")
try:
    push(repo, remote_location="origin", refspecs=[b"refs/heads/main:refs/heads/main"])
    print("✓ Successfully pushed repository to GitHub!")
    print("Check the 'Actions' tab on your GitHub repository to watch the Cloud Build compile both APKs!")
except Exception as e:
    print(f"Push error: {e}")
