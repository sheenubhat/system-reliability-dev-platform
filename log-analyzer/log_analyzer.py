
import sys

def analyze(file):
    with open(file) as f:
        for line in f:
            if "ERROR" in line or "WARN" in line:
                print(line.strip())

if __name__ =="__main__":
    analyze(sys.argv[1])