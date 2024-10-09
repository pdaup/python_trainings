import sys
from pathlib import Path
from typing import Sequence, Tuple, List


def parse_test_case(file: Sequence[str], string: str) -> Tuple[str, bool]:
    id_: str = ""
    string_in_file: bool = False

    for _, line in enumerate(file):
        if "Polarion ID: " in line:
            id_ = line.split("Polarion ID: ")[-1].split("\n")[0]
        elif id_ and string in line:
            string_in_file = True
    return id_, string_in_file


def parse_framework_file(file: Sequence[str], string: str) -> List:
    new_strings: list = []
    for i, line in enumerate(file):
        if string in line:
            if line.startswith("def "):
                break
            for index in range(i, 0, -1):
                if file[index].startswith("def "):
                    prefix = file[index].split("def ")[1].split("(")[0]
                    new_string = f"{prefix}("
                    new_strings.append(new_string)

    return new_strings


def extract_tc_ids(string: str = '') -> Tuple[set, set]:
    counter: int = 0
    results: set = set()
    search_strings: set = set()
    new_strings: set = set()
    used_strings: set = set()

    while counter < 6:
        if counter == 0:
            search_strings.add(string)
        else:
            search_strings = new_strings - used_strings
        for string in search_strings:
            used_strings.add(string)
            for file in Path('.').glob("**/*.py"):
                with open(file, encoding="utf8") as open_file:
                    f = open_file.readlines()
                    if not file.name.startswith('test_'):
                        new_search_strings = parse_framework_file(file=f, string=string)
                        new_strings.symmetric_difference_update(new_search_strings)
                    else:
                        id_, string_in_file = parse_test_case(file=f, string=string)
                        if string_in_file:
                            results.add(id_)
        counter += 1
    return results, used_strings


if __name__ == '__main__':
    results, used_strings = extract_tc_ids(sys.argv[1])
    print(f"Used in test cases ({len(results)}): \n{results}")
    print(used_strings)
