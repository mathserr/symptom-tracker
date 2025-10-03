#!/usr/bin/env python3
"""
Automatic sync script for PythonAnywhere deployment
This script will automatically upload your files to PythonAnywhere when you make changes

Requirements:
1. Install: pip install paramiko scp
2. Set up your PythonAnywhere credentials
3. Run this script after making changes

Usage:
    python sync_to_pythonanywhere.py
"""

import os
import json
import paramiko
from scp import SCPClient
from datetime import datetime
import getpass

class PythonAnywhereSync:
    def __init__(self):
        self.config_file = 'pythonanywhere_config.json'
        self.config = self.load_config()
        
    def load_config(self):
        """Load or create configuration"""
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r') as f:
                return json.load(f)
        else:
            return self.create_config()
    
    def create_config(self):
        """Create initial configuration"""
        print("🔧 Setting up PythonAnywhere sync configuration...")
        print("You can find these details in your PythonAnywhere account settings.")
        
        config = {
            'username': input('PythonAnywhere username: '),
            'hostname': '',  # Will be set automatically
            'remote_path': '',  # Will be set automatically
            'files_to_sync': [
                'flask_app.py',
                'templates/index.html',
                'data/symptom_log.json'
            ]
        }
        
        # Set derived values
        config['hostname'] = f"{config['username']}.pythonanywhere.com"
        config['remote_path'] = f"/home/{config['username']}/mysite"
        
        # Save config (without password for security)
        with open(self.config_file, 'w') as f:
            json.dump(config, f, indent=2)
            
        print(f"✅ Configuration saved to {self.config_file}")
        print(f"📡 Will sync to: {config['hostname']}:{config['remote_path']}")
        
        return config
    
    def get_password(self):
        """Securely get password"""
        return getpass.getpass(f"Password for {self.config['username']}: ")
    
    def sync_files(self):
        """Sync files to PythonAnywhere"""
        try:
            print(f"🚀 Syncing to {self.config['hostname']}...")
            
            # Get password
            password = self.get_password()
            
            # Create SSH connection
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            
            # Connect
            ssh.connect(
                hostname='ssh.pythonanywhere.com',
                username=self.config['username'], 
                password=password,
                port=22
            )
            
            print("✅ Connected to PythonAnywhere")
            
            # Create SCP client
            with SCPClient(ssh.get_transport()) as scp:
                
                # Ensure remote directories exist
                self.create_remote_directories(ssh)
                
                # Sync each file
                for file_path in self.config['files_to_sync']:
                    if os.path.exists(file_path):
                        remote_file = f"{self.config['remote_path']}/{file_path}"
                        print(f"📤 Uploading {file_path} → {remote_file}")
                        
                        # Ensure remote directory exists
                        remote_dir = os.path.dirname(remote_file)
                        ssh.exec_command(f'mkdir -p {remote_dir}')
                        
                        # Upload file
                        scp.put(file_path, remote_file)
                        print(f"✅ {file_path} uploaded successfully")
                    else:
                        print(f"⚠️  {file_path} not found, skipping")
                
                # Reload web app
                self.reload_webapp(ssh)
                
            ssh.close()
            print(f"🎉 Sync completed! Check your app at: https://{self.config['username']}.pythonanywhere.com")
            
        except Exception as e:
            print(f"❌ Error during sync: {str(e)}")
            print("💡 Check your username/password and try again")
    
    def create_remote_directories(self, ssh):
        """Create necessary directories on remote server"""
        directories = [
            self.config['remote_path'],
            f"{self.config['remote_path']}/templates",
            f"{self.config['remote_path']}/data"
        ]
        
        for directory in directories:
            ssh.exec_command(f'mkdir -p {directory}')
            print(f"📁 Ensured directory exists: {directory}")
    
    def reload_webapp(self, ssh):
        """Reload the web app on PythonAnywhere"""
        try:
            # Touch the WSGI file to reload
            wsgi_path = f"{self.config['remote_path']}/flask_app.py"
            ssh.exec_command(f'touch {wsgi_path}')
            print("🔄 Web app reloaded")
        except Exception as e:
            print(f"⚠️  Could not reload web app automatically: {e}")
            print("💡 You may need to reload manually in PythonAnywhere Web tab")

def main():
    """Main function"""
    print("🐍 PythonAnywhere Auto-Sync Tool")
    print("=" * 40)
    
    syncer = PythonAnywhereSync()
    syncer.sync_files()

if __name__ == "__main__":
    main()