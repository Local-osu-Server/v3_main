import os
import subprocess


def find_python_command():
    commands = ["py", "python", "python3"]
    for command in commands:
        try:
            subprocess.run([command, "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            return command
        except FileNotFoundError:
            continue
    raise RuntimeError("Python interpreter not found.")


project_path = os.path.dirname(os.path.abspath(__file__))

env = os.environ.copy()
env["PYTHONPATH"] = os.environ.get("PYTHONPATH", '') + ":" + project_path

script_path = os.path.join(project_path, "app/server/main.py")

try:
    subprocess.run([find_python_command(), script_path], check=True, env=env)
except Exception as e:
    print(f"Error: {e}")
