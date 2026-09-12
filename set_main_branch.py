import os
from dulwich.repo import Repo

repo_path = os.path.dirname(os.path.abspath(__file__))
repo = Repo(repo_path)

head_commit = repo.head()
# Set refs/heads/main
repo.refs[b"refs/heads/main"] = head_commit
# Point HEAD to refs/heads/main
repo.refs.set_symbolic_ref(b"HEAD", b"refs/heads/main")

print(f"HEAD is now pointing to: {repo.refs.read_ref(b'HEAD')}")
print(f"Branch 'main' created at commit: {head_commit.decode('ascii')}")
