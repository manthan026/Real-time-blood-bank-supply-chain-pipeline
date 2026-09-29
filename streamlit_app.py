"""
Streamlit Community Cloud Entrypoint
Automatically routes to dashboard/app.py for 1-click cloud deployment.
"""
import os
import sys

# Ensure root and dashboard directories are in sys.path
root_dir = os.path.dirname(os.path.abspath(__file__))
dashboard_dir = os.path.join(root_dir, "dashboard")

for path in [root_dir, dashboard_dir]:
    if path not in sys.path:
        sys.path.insert(0, path)

# Execute the main dashboard app with correct context
app_file = os.path.join(dashboard_dir, "app.py")
globals()["__file__"] = app_file

with open(app_file, "r", encoding="utf-8") as f:
    code = compile(f.read(), app_file, "exec")
    exec(code, globals())
