import dulwich.porcelain as porcelain
import os

repo_path = os.path.dirname(os.path.abspath(__file__))
porcelain.add(repo_path)
msg = "Design Overhaul: Luxury Dark Mode (OLED #070b12, Electric Crimson & Cyber Gold neon styling)"
author = "Fantasy11 Dev <dev@fantasy11.app>"
cid = porcelain.commit(repo_path, message=msg.encode("utf-8"), author=author.encode("utf-8"), committer=author.encode("utf-8"))
print(f"[SUCCESS] Committed Luxury Dark Mode overhaul! Commit hash: {cid.decode('ascii')[:8]}")
