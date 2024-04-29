import subprocess
import sys

def main():
    # intentionally do call wait() on the subprocess
    proc = subprocess.Popen(('sleep', '60'), stdout=None)
    return

if __name__ == '__main__':
    sys.exit(main())
