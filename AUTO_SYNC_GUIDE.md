# 🔄 Automatic PythonAnywhere Sync Guide

I've created **multiple sync methods** for you. Choose the one that works best:

## 🎯 **Method 1: GitHub Sync (Recommended)**

### **Setup on Your Computer:**
1. **Use the files I created:**
   - `github_sync.py` - Main sync script
   - `quick_sync.bat` - Windows batch file for easy syncing

2. **To sync changes:**
   ```bash
   # Option A: Use the batch file (easiest)
   double-click quick_sync.bat
   
   # Option B: Run Python script manually  
   python github_sync.py
   ```

### **Setup on PythonAnywhere (One-time):**
1. **Open a console** on PythonAnywhere
2. **Clone your repository:**
   ```bash
   cd /home/mathserr  # Replace with your username
   git clone https://github.com/mathserr/symptom-tracker.git mysite
   cd mysite
   ```

3. **Set up your web app** to point to this directory
4. **Update whenever you sync:**
   ```bash
   cd /home/mathserr/mysite
   git pull origin main
   ```

### **Daily Workflow:**
1. **Make changes** to your code locally
2. **Run** `quick_sync.bat` (or `python github_sync.py`)
3. **Go to PythonAnywhere console** and run: `git pull origin main`
4. **Your app updates automatically!**

---

## 🔧 **Method 2: Direct SSH Sync (Advanced)**

### **Installation:**
```bash
pip install paramiko scp
```

### **Usage:**
```bash
python sync_to_pythonanywhere.py
```

This directly uploads files via SSH but requires your PythonAnywhere password each time.

---

## 🎯 **Method 3: Automated PythonAnywhere Pull (Most Convenient)**

### **Create this script on PythonAnywhere:**

1. **In PythonAnywhere Files tab**, create `/home/mathserr/update_app.py`:
   ```python
   #!/usr/bin/env python3
   import subprocess
   import os
   
   os.chdir('/home/mathserr/mysite')
   
   # Pull latest changes
   result = subprocess.run(['git', 'pull', 'origin', 'main'], 
                          capture_output=True, text=True)
   print("Git pull result:", result.stdout)
   
   # Touch WSGI file to reload
   subprocess.run(['touch', 'flask_app.py'])
   print("✅ App reloaded!")
   ```

2. **Run it from PythonAnywhere console:**
   ```bash
   python3.10 /home/mathserr/update_app.py
   ```

---

## 🚀 **Recommended Workflow:**

### **Initial Setup:**
1. ✅ Your code is already on GitHub
2. ✅ Clone it to PythonAnywhere (see Method 1 setup)
3. ✅ Configure your PythonAnywhere web app

### **Daily Development:**
1. **Edit code** locally in VS Code
2. **Run** `quick_sync.bat` to push to GitHub
3. **In PythonAnywhere console:** `cd /home/mathserr/mysite && git pull origin main`
4. **Your app is updated!**

### **Even Easier - Bookmark This:**
Create a bookmark in your browser for the PythonAnywhere console with this command pre-filled, so you just need to click and press Enter.

---

## 📱 **Benefits:**

- ✅ **Version control** - All changes tracked in Git
- ✅ **Backup** - Your code is safe on GitHub
- ✅ **Easy rollback** - Can revert changes if needed
- ✅ **No passwords** needed for GitHub method
- ✅ **Works from anywhere** - Can update from any computer

---

## 🎉 **Quick Start:**

1. **Right now:** Double-click `quick_sync.bat`
2. **On PythonAnywhere:** Run the setup commands from Method 1
3. **Forever after:** Just run the batch file and pull on PythonAnywhere!

Your symptom tracker will stay perfectly synced between your computer and your iPhone! 📱✨