import subprocess

if __name__ == "__main__":
    front_proc = subprocess.Popen(["python", "web_import.py"])
    back_proc = subprocess.Popen(["python", "canvas-scrape.py"])
    #fswatch = subprocess.Popen(["python", "fswatch.py"])

    try:
        front_proc.wait()
        back_proc.wait()
        #fswatch.wait()
    except KeyboardInterrupt:
        print("Interrupted, terminating...")
        front_proc.terminate()
        back_proc.terminate()
        #fswatch.terminate()




