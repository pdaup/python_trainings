import sys
from pathlib import Path


class StringFinder:
    level_counter = 0
    results = set()
    search_strings = set()
    new_strings = set()
    used_strings = set()

    def parse_framework_files(self, string: str = ''):
        while self.level_counter < 3:
            if self.level_counter == 0:
                self.search_strings.add(string)
            else:
                self.search_strings = self.new_strings - self.used_strings
            for string in self.search_strings:
                self.used_strings.add(string)
                for file in Path('.').glob("**/*.py"):
                    with open(file, encoding="utf8") as open_file:
                        f = open_file.readlines()
                        id_found = False
                        for i in range(len(f)):
                            line = f[i]
                            if "Polarion ID: " in line:
                                id = line.split("Polarion ID: ")[-1].split("\n")[0]
                                id_found = True
                            if id_found and string in line:
                                self.results.add(id)
                                break
                            elif string in line:
                                for _ in range(i):
                                    i -= 1
                                    if f[i].startswith("def "):
                                        prefix = f[i].split("def ")[1].split("(")[0]
                                        new_string = f"{prefix}("
                                        self.new_strings.add(new_string)
            self.level_counter += 1

    def get_results(self):
        print(f"Used in test cases ({len(self.results)}): \n{self.results}")
        print(self.used_strings)


if __name__ == '__main__':
    string_finder = StringFinder()
    string_finder.parse_framework_files(sys.argv[1])
    string_finder.get_results()
