from pathlib import Path

path = Path('learning_python.txt')

for line in path.read_text().splitlines():
    print(line)
