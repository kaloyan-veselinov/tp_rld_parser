import sys

if __name__ == "__main__":
    path = sys.argv[1]
    with open(path) as file:
        content = file.readlines()
        print(content)
