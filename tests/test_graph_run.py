import sys
import os

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from core.graph import app

if __name__ == "__main__":
    result = app.invoke({"message": "sensor data read failure", "history": []})
    print("=== Intent ===")
    print(result["intent"])
    print("\n=== Analysis ===")
    print(result["analysis"])
    print("\n=== Report ===")
    print(result.get("report", ""))
    print("\n=== Escalation ===")
    print(result.get("escalation", ""))
