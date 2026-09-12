import os
import sys
import dulwich.porcelain as porcelain
from dulwich.repo import Repo
from dulwich.config import ConfigFile

repo_path = os.path.dirname(os.path.abspath(__file__))
repo = Repo(repo_path)

print("=" * 60)
print("  FANTASY11 GITHUB REPOSITORY & CLOUD BUILD CONFIG")
print("=" * 60)

if len(sys.argv) > 1:
    remote_url = sys.argv[1].strip()
else:
    print("Usage:")
    print("  python push_to_github.py <YOUR_GITHUB_REPO_URL>")
    print("Example:")
    print("  python push_to_github.py https://github.com/myaccount/fantasy11.git")
    print("-" * 60)
    remote_url = input("Enter your GitHub repository URL (or press Enter to skip): ").strip()

if remote_url:
    # Set remote in git config
    config = repo.get_config()
    config.set((b"remote", b"origin"), b"url", remote_url.encode("utf-8"))
    config.set((b"remote", b"origin"), b"fetch", b"+refs/heads/*:refs/remotes/origin/*")
    config.write_to_path()
    print(f"\n[SUCCESS] Configured remote origin -> {remote_url}")

# Stage any new or modified files
porcelain.add(repo_path)

status = porcelain.status(repo_path)
changes = len(status.staged["add"]) + len(status.staged["modify"]) + len(status.staged["delete"])

if changes > 0:
    msg = "Update: CI/CD workflow and Git repository setup for Fantasy11"
    author = "Fantasy11 Dev <dev@fantasy11.app>"
    cid = porcelain.commit(repo_path, message=msg.encode("utf-8"), author=author.encode("utf-8"), committer=author.encode("utf-8"))
    print(f"[SUCCESS] Committed latest updates (Commit: {cid.decode('ascii')[:8]})")
else:
    print("[INFO] Working tree clean, nothing new to commit.")

print("\n" + "=" * 60)
print("  NEXT STEPS TO TRIGGER CLOUD APK BUILD:")
print("=" * 60)
print("1. If you have not created your GitHub repository yet:")
print("   Go to https://github.com/new and create a repository (e.g. 'fantasy11').")
print("")
print("2. Run the push command:")
if remote_url:
    print(f"   git push -u origin main")
else:
    print("   git remote add origin https://github.com/<YOUR_USER>/<REPO>.git")
    print("   git push -u origin main")
print("")
print("3. Once pushed, open GitHub ➔ click 'Actions' tab ➔ Watch both APKs compile!")
print("=" * 60)
