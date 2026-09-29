"""
Streamlit Community Cloud Entrypoint
Automatically routes to dashboard/app.py for 1-click cloud deployment.
"""
import os
import sys

# Ensure dashboard directory is in path
dashboard_dir = os.path.join(os.path.dirname(__file__), "dashboard")
if dashboard_dir not in sys.path:
    sys.path.insert(0, dashboard_dir)

# Execute the main dashboard app
app_file = os.path.join(dashboard_dir, "app.py")
with open(app_file, "r", encoding="utf-8") as f:
    code = compile(f.read(), app_file, "exec")
    exec(code, globals())
