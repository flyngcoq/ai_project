import shutil
import os
from pathlib import Path

project_root = Path("/Users/flyngcoq/AI_Project")
vault_root = project_root / "Obsidian_Vault"

def merge_folders(src, dst):
    for item in os.listdir(src):
        s = src / item
        d = dst / item
        if s.is_dir():
            if not d.exists():
                d.mkdir(parents=True)
            merge_folders(s, d)
        else:
            if not d.exists():
                shutil.move(str(s), str(d))
            else:
                # If file exists, we can overwrite or skip.
                # Given user's request, we'll overwrite to keep the latest from the vault.
                shutil.move(str(s), str(d))

if __name__ == "__main__":
    if vault_root.exists():
        print(f"Merging {vault_root} into {project_root}...")
        merge_folders(vault_root, project_root)
        print("Cleaning up empty Obsidian_Vault directory...")
        shutil.rmtree(vault_root)
        print("Merge complete.")
    else:
        print("Obsidian_Vault not found.")
