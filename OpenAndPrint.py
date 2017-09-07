import sys
class OpenAndPrint:

    def open_file(self):
        while True:
            file_name = input('Enter the file name: ')
            try:
                opened_file = open(file_name)  # use with?
                break
            except:  # FileNotFoundError or OSError
                print('File', file_name, 'cannot be opened. Please enter again.')
                continue
        return opened_file

    def print_lines(self):
        match = ["INDI", "NAME", "SEX", "BIRT", "DEAT", "FAMC",
                 "FAMS", "FAM", "MARR", "HUSB", "WIFE", "CHIL",
                 "DIV", "DATE", "HEAD", "TRLR", "NOTE"]
        opened = self.open_file()

        for line in opened:
            print("-->", line, end="")

            words = line.split()
            if words[1] in match:
                print("<-- ", end="")
                for word in words:
                    if words.index(word) == 1:
                        print("|" + word + "|Y|", end="")
                    else:
                        print(word, end="")
                print()
            elif words[-1] in match:  # two special cases
                print("<-- " + words[0] + "|" + words[-1] + "|Y|" + words[1], end="")
                print("")
            else:
                print("<-- ", end="")
                for word in words:
                    if words.index(word) == 1:
                        print("|" + word + "|N|", end="")
                    else:
                        print(word, end="")
                print()



def main():
    test = OpenAndPrint()
    test.print_lines()


if __name__ == '__main__':
    main()