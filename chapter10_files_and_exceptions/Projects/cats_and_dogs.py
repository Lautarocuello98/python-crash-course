from pathlib import Path

filenames = ['cats.txt', 'dogs.txt']

for filename in filenames:
    try:
        path = Path(filename)
        for line in path.read_text().splitlines():
            print(line)
    except FileNotFoundError:
        pass