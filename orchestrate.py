import subprocess

if __name__ == "__main__":
    front_proc = subprocess.Popen(["python", "web-import-API.py"])
    back_proc = subprocess.Popen(["python", "canvas-scrape.py"])

    try:
        front_proc.wait()
        back_proc.wait()
    except KeyboardInterrupt:
        print("Interrupted, terminating...")
        front_proc.terminate()
        back_proc.terminate()




