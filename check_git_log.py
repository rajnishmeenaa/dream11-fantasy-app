import dulwich.porcelain as porcelain
import os

repo_path = os.path.dirname(os.path.abspath(__file__))
entries = porcelain.log(repo_path, max_entries=5)
for entry in entries:
    c = entry.commit
    print("=" * 60)
    print(f"Commit: {c.id.decode('ascii')}")
    print(f"Author: {c.author.decode('utf-8')}")
    print(f"Message: {c.message.decode('utf-8').strip()}")
print("=" * 60)
