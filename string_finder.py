import sys
from pathlib import Path

results = []


def parse_test_files(string: str = ''):
    for test_file in Path('.').glob("*test_cases/**/test_*.py"):
        with open(test_file, encoding="utf8") as open_file:
            f = open_file.readlines()
            id = ""
            for line in f:
                if "Polarion ID" in line:
                    id = line.split("Polarion ID: ")[-1].split("\n")[0]
                if string in line:
                    results.append(id)


def parse_test_files_2(string: str = ''):
    for test_file in Path('.').glob("*test_cases/**/test_*.py"):
        with open(test_file, encoding="utf8") as open_file:
            f = open_file.read()
            try:
                f.index(string)
                index = f.find("Polarion ID: ") + 13
                results.append(f[index:index+10])
            except ValueError:
                pass
            

def get_results():
    print(f"Used in test cases ({len(set(results))}): \n{set(results)}")


if __name__ == '__main__':
    parse_test_files(sys.argv[1])
    get_results()
