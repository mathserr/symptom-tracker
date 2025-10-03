# PythonAnywhere Deployment Guide

## 🐍 **Step-by-Step PythonAnywhere Deployment**

### **1. Create PythonAnywhere Account**
1. Go to [pythonanywhere.com](https://pythonanywhere.com)
2. Sign up for a **free "Beginner" account**
3. Confirm your email and log in

### **2. Upload Your Files**
1. **Go to Files tab** in PythonAnywhere dashboard
2. **Navigate to** `/home/mathserr/` (replace `mathserr` with your username)
3. **Create folder** called `mysite`
4. **Upload these files to** `/home/mathserr/mysite/`:
   ```
   flask_app.py          (the WSGI file)
   templates/index.html  (create templates folder first)
   symptom_log.json      (optional - your existing data)
   ```

### **3. Set Up Web App**
1. **Go to Web tab** in PythonAnywhere dashboard
2. **Click "Add a new web app"**
3. **Choose "Manual configuration"**
4. **Select Python 3.10**
5. **Click Next through the setup**

### **4. Configure WSGI File**
1. **In Web tab**, find **"WSGI configuration file"** link
2. **Click it** to open the editor
3. **Replace ALL content** with:
   ```python
   import sys
   import os

   # Add your project directory to the Python path
   path = '/home/mathserr/mysite'  # Replace 'mathserr' with YOUR username
   if path not in sys.path:
       sys.path.append(path)

   from flask_app import application
   ```

### **5. Set Up Static Files (Optional)**
1. **In Web tab**, scroll to **"Static files"** section
2. **Add new static file mapping**:
   - **URL**: `/static/`
   - **Directory**: `/home/mathserr/mysite/static/`

### **6. Update File Paths**
**IMPORTANT**: Edit `flask_app.py` and replace `mathserr` with your actual username:
```python
BASE_DIR = '/home/YOURUSERNAME/mysite'  # Change YOURUSERNAME
```

### **7. Test Your App**
1. **Click "Reload" button** in Web tab
2. **Visit your app** at: `http://mathserr.pythonanywhere.com`
3. **Check error logs** if it doesn't work (in Web tab)

## 📱 **Accessing on iPhone**
- **URL**: `http://yourusername.pythonanywhere.com`
- **Add to Home Screen**: Safari → Share → "Add to Home Screen"

## 🔧 **File Structure on PythonAnywhere**
```
/home/mathserr/mysite/
├── flask_app.py           # Main WSGI app
├── templates/
│   └── index.html         # Web interface
├── data/
│   └── symptom_log.json   # Your symptom data (created automatically)
└── error.log              # Error logging (if issues occur)
```

## 🆓 **Free Tier Limitations**
- **Always-on until**: 3 months, then need to refresh
- **1 web app** allowed on free tier
- **512MB disk space**
- **CPU seconds limited** per day

## 🚨 **Troubleshooting**
If your app doesn't work:
1. **Check error logs** in Web tab
2. **Verify file paths** in flask_app.py
3. **Ensure templates folder** exists with index.html
4. **Check WSGI configuration** is correct
5. **Visit** `/health` endpoint to test: `http://yourusername.pythonanywhere.com/health`

## 📤 **Importing Existing Data**
Copy your local `symptom_log.json` to `/home/yourusername/mysite/data/` or use the web interface to re-enter data.

---

**Need help?** PythonAnywhere has excellent documentation and forums for troubleshooting!