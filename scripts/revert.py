import subprocess
try:
    subprocess.run(["git", "checkout", "index.html"], check=True)
    print("Success")
except Exception as e:
    print("Error:", e)
