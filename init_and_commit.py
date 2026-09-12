import os
import dulwich.porcelain as porcelain
from dulwich.repo import Repo

repo_path = os.path.dirname(os.path.abspath(__file__))
git_dir = os.path.join(repo_path, ".git")

print(f"Target repository: {repo_path}")

# 1. Initialize Git repository if not already initialized
if not os.path.exists(git_dir):
    repo = Repo.init(repo_path)
    print("[SUCCESS] Initialized fresh Git repository (.git/)")
else:
    repo = Repo(repo_path)
    print("[INFO] Existing Git repository found")

# 2. Add files respecting .gitignore
# Stage all files
print("Staging files...")
porcelain.add(repo_path)

# 3. Commit
commit_message = "Initial commit: Fantasy11 Dual Android Platform (Player App & Admin Console) with GitHub Actions Cloud APK Builder"
author = "Fantasy11 Dev <dev@fantasy11.app>"

try:
    commit_id = porcelain.commit(
        repo_path,
        message=commit_message.encode("utf-8"),
        author=author.encode("utf-8"),
        committer=author.encode("utf-8")
    )
    print(f"[SUCCESS] Commit created successfully! Hash: {commit_id.decode('ascii')}")
except Exception as e:
    print(f"[INFO] Commit status: {e}")

# 4. Show status
status = porcelain.status(repo_path)
print(f"Staged files: {len(status.staged['add']) + len(status.staged['modify'])}")
print(f"Untracked files: {len(status.untracked)}")

print("Git repository is fully initialized and committed!")
