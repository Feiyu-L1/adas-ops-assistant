import sys
import os

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from core.graph import app

result = app.invoke({"message": "sensor data read failure"})
print(result)
