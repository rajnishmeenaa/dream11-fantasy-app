import os
import shutil

src_dir = r"public"
player_assets = r"android-player/app/src/main/assets"
admin_assets = r"android-admin/app/src/main/assets"

# Clean destination dirs
if os.path.exists(player_assets):
    shutil.rmtree(player_assets)
if os.path.exists(admin_assets):
    shutil.rmtree(admin_assets)

os.makedirs(player_assets, exist_ok=True)
os.makedirs(admin_assets, exist_ok=True)

# Player App: Zero Admin
player_files = ['index.html', 'styles.css', 'app.js', 'manifest.json', 'sw.js']
for pf in player_files:
    s = os.path.join(src_dir, pf)
    if os.path.exists(s):
        shutil.copy2(s, os.path.join(player_assets, pf))

# Admin App: Only Admin Console files
admin_files = ['admin.html', 'admin.css', 'admin.js', 'manifest-admin.json', 'styles.css']
for af in admin_files:
    s = os.path.join(src_dir, af)
    if os.path.exists(s):
        shutil.copy2(s, os.path.join(admin_assets, af))

print("Verified strict asset separation:")
print("Player assets:", os.listdir(player_assets))
print("Admin assets:", os.listdir(admin_assets))
