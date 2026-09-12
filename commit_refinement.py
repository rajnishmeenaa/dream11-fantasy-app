import dulwich.porcelain as porcelain
import os

repo_path = os.path.dirname(os.path.abspath(__file__))
porcelain.add(repo_path)
msg = "Refinement: Pure Player App (Zero Admin), Outfit geometric typography, and attractive glowing shield logo"
author = "Fantasy11 Dev <dev@fantasy11.app>"
cid = porcelain.commit(repo_path, message=msg.encode("utf-8"), author=author.encode("utf-8"), committer=author.encode("utf-8"))
print(f"[SUCCESS] Committed logo & font refinement to Git! Commit: {cid.decode('ascii')[:8]}")
