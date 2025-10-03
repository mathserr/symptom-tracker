#!/usr/bin/env python3
"""
GitHub-based sync for PythonAnywhere
This uses Git to sync changes via GitHub, which PythonAnywhere supports natively

Setup:
1. Your code is already on GitHub (github.com/mathserr/symptom-tracker)
2. Clone the repo on PythonAnywhere
3. Use this script to push changes and pull them on PythonAnywhere

This is more reliable than direct SSH/SCP upload.
"""

import os
import subprocess
import json
from datetime import datetime
import requests

class GitHubSync:
    def __init__(self):
        self.repo_path = "."
        self.github_user = "mathserr"
        self.repo_name = "symptom-tracker"
        
    def commit_and_push(self, message=None):
        """Commit changes and push to GitHub"""
        if not message:
            message = f"Auto-sync: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        
        try:
            print("📝 Committing changes...")
            
            # Add all changes
            subprocess.run(['git', 'add', '.'], check=True, cwd=self.repo_path)
            
            # Check if there are changes to commit
            result = subprocess.run(['git', 'status', '--porcelain'], 
                                 capture_output=True, text=True, cwd=self.repo_path)
            
            if not result.stdout.strip():
                print("ℹ️  No changes to commit")
                return False
            
            # Commit changes
            subprocess.run(['git', 'commit', '-m', message], check=True, cwd=self.repo_path)
            print(f"✅ Committed: {message}")
            
            # Push to GitHub
            print("📤 Pushing to GitHub...")
            subprocess.run(['git', 'push'], check=True, cwd=self.repo_path)
            print("✅ Pushed to GitHub successfully")
            
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Git error: {e}")
            return False
    
    def create_pythonanywhere_script(self):
        """Create a script for PythonAnywhere to pull changes"""
        pa_script = f"""#!/bin/bash
# PythonAnywhere pull script
# Run this in a PythonAnywhere console to update your app

cd /home/{self.github_user}/mysite

# Pull latest changes from GitHub
echo "📥 Pulling latest changes from GitHub..."
git pull origin main

# Copy files to correct locations (if needed)
echo "📁 Organizing files..."
cp flask_app.py .
cp -r templates .
mkdir -p data
cp -f data/symptom_log.json data/ 2>/dev/null || echo "No existing data file"

# Touch WSGI file to reload app
echo "🔄 Reloading web app..."
touch /var/www/{self.github_user}_pythonanywhere_com_wsgi.py

echo "✅ Update complete! Visit https://{self.github_user}.pythonanywhere.com"
"""
        
        with open('pythonanywhere_update.sh', 'w') as f:
            f.write(pa_script)
        
        print("📜 Created pythonanywhere_update.sh")
        print(f"💡 Upload this script to PythonAnywhere and run it after each sync")

def main():
    """Main sync function"""
    print("🔄 GitHub-based PythonAnywhere Sync")
    print("=" * 40)
    
    syncer = GitHubSync()
    
    # Get commit message
    message = input("Commit message (Enter for auto-message): ").strip()
    
    # Commit and push changes
    if syncer.commit_and_push(message if message else None):
        print("\n🎯 Next steps:")
        print("1. Go to PythonAnywhere console")
        print("2. Navigate to your project directory")
        print("3. Run: git pull origin main")
        print("4. Reload your web app")
        print(f"\n🌐 Your app: https://{syncer.github_user}.pythonanywhere.com")
        
        # Create helper script
        syncer.create_pythonanywhere_script()
    else:
        print("❌ Sync failed or no changes to sync")

if __name__ == "__main__":
    main()