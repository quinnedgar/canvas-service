import time
import subprocess
import threading


def front():
    subprocess.Popen(["python", "flask/web_import.py"])

def back():
    subprocess.Popen(["python", "canvas-scrape.py"])

def main():
    thread_1 = threading.Thread(target=front)
    thread_2 = threading.Thread(target=back)

    thread_1.start()
    thread_2.start()

    thread_1.join()
    thread_2.join()

if __name__ == "__main__":
    main()




