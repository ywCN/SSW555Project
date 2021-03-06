import sqlite3
import os
from datetime import datetime
from prettytable import PrettyTable


'''
Our team is using database solution.
Please put the .db file in the same path of this .py file.
'''


class HW4:
    def __init__(self):
        self.db = r'project.db'
        if os.path.isfile(self.db):
            self.conn = sqlite3.connect(self.db)
            self.c = self.conn.cursor()
        else:
            print("\n"
                  "--------------------------------------------------------------------\n"
                  "| Please put the 'project.db' in the same path of this python file!|\n"
                  "--------------------------------------------------------------------")
            exit()

    def dates_before_current_date(self):
        """
        US01 - Dates before current date
        :rtype: None
        """
        query = "select INDI, NAME, BIRT, DEAT, fam.MARR, fam.DIV from indi LEFT JOIN fam ON INDI.INDI = FAM.HUSB OR " \
                "INDI.INDI = FAM.WIFE "
        today = datetime.today().date()

        for row in self.query_info(query):
            birth = datetime.strptime(row[2], '%Y-%m-%d').date()
            try:
                death = datetime.strptime(row[3], '%Y-%m-%d').date()
            except (TypeError, ValueError):
                death = "NA"
            try:
                marriage = datetime.strptime(row[4], '%Y-%m-%d').date()
            except (TypeError, ValueError):
                marriage = "NA"
            try:
                divorce = datetime.strptime(row[5], '%Y-%m-%d').date()
            except (TypeError, ValueError):
                divorce = "NA"
            dates = [birth, death, marriage, divorce]
            for date in dates:
                if date != "NA" and date > today:
                    print("ERROR: US01: {} occurs after today {} for {}".format(date, today, row[0] + row[1]))

    def birth_before_marriage(self):
        """
        US02 - Birth before marriage
        :rtype: None
        """
        query = "select INDI, NAME, BIRT, fam.MARR from indi INNER JOIN fam ON INDI.INDI = FAM.HUSB OR INDI.INDI = " \
                "FAM.WIFE "
        for row in self.query_info(query):
            if row[3] != "NA":
                birth = datetime.strptime(row[2], '%Y-%m-%d').date()
                marriage = datetime.strptime(row[3], '%Y-%m-%d').date()
                if birth > marriage:
                    print("ERROR: US02: Birth {} occurs after marriage {} for {}"
                          .format(birth, marriage, row[0] + row[1]))

    def birth_before_death(self):
        """
        US03 - Birth before death
        :rtype: None
        """
        query = "select INDI, NAME, BIRT, DEAT from indi"
        for row in self.query_info(query):
            if row[3] != "NA":
                birth = datetime.strptime(row[2], '%Y-%m-%d').date()
                death = datetime.strptime(row[3], '%Y-%m-%d').date()
                if birth > death:
                    print("ERROR: US03: Birth {} occurs after death {} for {}".format(birth, death, row[0] + row[1]))

    def marriage_before_divorce(self):
        """
        US04 - Marriage before divorce
        :rtype: None
        """
        query = "select INDI, NAME, fam.MARR, fam.DIV from indi INNER JOIN fam " \
                "ON INDI.INDI = FAM.HUSB OR INDI.INDI = FAM.WIFE"
        for row in self.query_info(query):
            if row[3] != "NA":
                marry = datetime.strptime(row[2], '%Y-%m-%d').date()
                divorce = datetime.strptime(row[3], '%Y-%m-%d').date()
                if marry > divorce:
                    print("ERROR: US04: Marriage {} occurs after divorce {} for {}"
                          .format(marry, divorce, row[0] + row[1]))

    def marriage_before_death(self):
        """
        US05 - Marriage before death
        :rtype: None
        """
        query = "select INDI, NAME, DEAT, fam.MARR from indi INNER JOIN fam " \
                "ON INDI.INDI = FAM.HUSB OR INDI.INDI = FAM.WIFE"

        for row in self.query_info(query):
            if row[2] != "NA":
                death = datetime.strptime(row[2], '%Y-%m-%d').date()
                marry = datetime.strptime(row[3], '%Y-%m-%d').date()
                if marry > death:  # cannot marry after death
                    print("ERROR: US05: Marriage {} occurs after death {} for {}".format(marry, death, row[0] + row[1]))

    def divorce_before_death(self):
        """
        US06 - Divorce before death
        :rtype: None
        """
        query = "select INDI, NAME, DEAT, fam.DIV from indi INNER JOIN fam " \
                "ON INDI.INDI = FAM.HUSB OR INDI.INDI = FAM.WIFE"

        for row in self.query_info(query):
            if row[2] != "NA" and row[3] != "NA":
                death = datetime.strptime(row[2], '%Y-%m-%d').date()
                divorce = datetime.strptime(row[3], '%Y-%m-%d').date()
                if divorce > death:  # cannot divorce after death
                    print("ERROR: US06: Divorce {} occurs after death {} for {}"
                          .format(divorce, death, row[0] + row[1]))

    def less_than_150_years_old(self):
        """
        US07 - Less then 150 years old
        :rtype: None
        """
        query = "select INDI, NAME, BIRT, DEAT from indi"
        today = datetime.today().date()
        for row in self.query_info(query):
            birth = datetime.strptime(row[2], '%Y-%m-%d').date()
            if row[3] != "NA":
                death = datetime.strptime(row[3], '%Y-%m-%d').date()
                age = death.year - birth.year
            else:
                age = today.year - birth.year
            if age >= 150:
                print("ERROR: US07: Age is greater than or equal to 150 years for {}".format(row[0] + row[1]))

    def birth_before_marriage_of_parents(self):
        """
        US08 - Birth before marriage of parents
        :rtype: None
        """
        query = "select indi.INDI, indi.NAME, indi.BIRT, fam.MARR, fam.DIV from indi left join fam on indi.FAMC = " \
                "fam.FAM "
        for row in self.query_info(query):
            birth = datetime.strptime(row[2], '%Y-%m-%d').date()
            try:
                marry = datetime.strptime(row[3], '%Y-%m-%d').date()
            except (TypeError, ValueError):
                marry = "NA"
            try:
                divorce = datetime.strptime(row[4], '%Y-%m-%d').date()
            except (TypeError, ValueError):
                divorce = "NA"
            if marry != "NA" and birth < marry:
                print("ERROR: US08: Parent marriage {} after birth {} of {}".format(marry, birth, row[0] + row[1]))
            if divorce != "NA":
                if divorce.year == birth.year:
                    if birth.month - divorce.month > 9:
                        print("ERROR: {} was born {} after 9 months of parent divorce {}"
                              .format(row[0] + row[1], birth, divorce))
                elif divorce.year == birth.year - 1:
                    months = birth.month + 12 - divorce.month
                    if months > 9:
                        print("ERROR: US08: {} was born {} after 9 months of parent divorce {}"
                              .format(row[0] + row[1], birth, divorce))
                elif divorce.year < birth.year - 1:
                    print("ERROR: US08: {} was born {} after 9 months of parent divorce {}"
                          .format(row[0] + row[1], birth, divorce))

    def query_info(self, query):
        """
        :type query: str
        :rtype: List[List[str]]
        """
        self.c.execute("%s" % query)
        return self.c.fetchall()

    def disconnect(self):
        """
        :return: null
        """
        self.c.close()
        self.conn.close()

    def get_age(self, birthday, deathday):
        today = datetime.today().date()
        birth = datetime.strptime(birthday, '%Y-%m-%d').date()
        if deathday != "NA":
            return (datetime.strptime(deathday, '%Y-%m-%d').date() - birth).days / 365.25
        return (today - birth).days / 365.25

    def print_info(self):
        indi_info = 'SELECT INDI, NAME, SEX, BIRT, DEAT, FAMC, FAMS FROM indi'
        fam_info = 'SELECT FAM, MARR, DIV, HUSB, WIFE, CHIL FROM fam'
        t_indi = PrettyTable(["ID", "Name", "Gender", "Birthday", "Age", "Alive", "Death", "Child", "Spouse"])
        t_fam = PrettyTable(
            ["ID", "Married", "Divorced", "Husband ID", "Husband Name", "Wife ID", "Wife Name", "Children"])
        name_map = {}

        for row in self.query_info(indi_info):
            age = round(self.get_age(row[3], row[4]))

            if row[4] == "NA":
                alive = True
            else:
                alive = False

            name_map[row[0]] = row[1]
            lst = list(row)
            lst.insert(4, age)
            lst.insert(5, alive)
            t_indi.add_row(lst)

        for row in self.query_info(fam_info):
            lst = list(row)
            lst.insert(4, name_map[row[3]])
            lst.insert(6, name_map[row[4]])
            t_fam.add_row(lst)

        print("People")
        print(t_indi)
        print("Families")
        print(t_fam)
        print()

    def run_sprint1(self):
        self.print_info()
        self.dates_before_current_date()
        self.birth_before_marriage()
        self.birth_before_death()
        self.marriage_before_divorce()
        self.marriage_before_death()
        self.divorce_before_death()
        self.less_than_150_years_old()
        self.birth_before_marriage_of_parents()


def main():
    demo = HW4()
    demo.run_sprint1()
    demo.disconnect()


if __name__ == '__main__':
    main()
