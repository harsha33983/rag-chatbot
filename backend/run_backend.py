import os
import sys

# Move up one level to project root
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

os.environ["PYTHONPATH"] = ROOT_DIR + (os.pathsep + os.environ.get("PYTHONPATH", "") if os.environ.get("PYTHONPATH") else "")
os.chdir(ROOT_DIR)

import uvicorn

if __name__ == "__main__":
    print(f"Starting MindCare AI Backend from: {ROOT_DIR}")
    print("Database: SQLite (mindcare.db)")
    print("Server running at: http://127.0.0.1:8000")
    print("API Documentation: http://127.0.0.1:8000/docs")
    uvicorn.run(
        "backend.app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        app_dir=ROOT_DIR
    )
