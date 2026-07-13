import sys
from ima_system import ask

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "ask":
        question = " ".join(sys.argv[2:])
        print(ask(question))
    else:
        print("usage: python3 ima.py ask <question>")
