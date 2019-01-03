


# I am fairly certain that section and subsection are irrelevant to the analyzers logic
#todo: find out if section and subsection are relevant
from expungeservice.analyzer.ineligible_crimes_list import IneligibleCrimesList





class Statute(object):
    """ Statute corresponding to a law

    Statutes are represented by numbers in hierarchical manner:
    chapter.subchapter(section)(subsection) e.g. 653.412(5)(c)

    Attributes:
        chapter: An integer that specifies statute chapter.
        subchapter: An integer that specifies statute sub-chapter.
        section: An integer that specifies the section within sub-chapter.
        subsection: A string of length 1 that specifies the sub-section within
                    section.
    """
    def __init__(self, statute_string, chapter=None, subchapter=None, section=None, subsection=None):

        self.statute_string = str(statute_string)
        self.chapter = chapter
        self.subchapter = subchapter
        self.section = section
        self.subsection = subsection
        # TODO we may need to add components beyond subsection

        if len(statute_string)>=6: #todo: this is wrong but will kinda work for everything on our list except marijuana crimes.

            statute_string = statute_string.lower() #convert to lowercase

            statute_string = [char for char in statute_string if char not in "abcdefghijklmnopqrstuvwxyz!@#$%^&*() .,;'[]<>?:{}\""] #remove all other chars #todo: fix this it could include weird chars
            statute_string = ''.join(statute_string)

            statute_string = statute_string[0:6] #trim to only first 6

            self.chapter = statute_string[0:3]
            self.subchapter = statute_string[3:7]

            self.statute_string = self.chapter + '.' + self.subchapter

    def __eq__(self, other):
        return (self.chapter == other.chapter and
                self.subchapter == other.subchapter and
                ((not self.section and not other.section) or
                 self.section == other.section) and
                ((not self.subsection and not other.subsection) or
                 self.subsection == other.subsection))

    def __str__(self):
        return str(self.statute_string)

    # def __str__(self):
    #     # TODO do these need to have leading zeros?
    #     statute = '{}'.format(self.chapter)
    #     if self.subchapter:
    #         statute = '{}.{:03d}'.format(statute, self.subchapter)
    #     if self.section:
    #         statute = '{}({})'.format(statute, self.section)
    #     if self.subsection:
    #         statute = '{}({})'.format(statute, self.subsection)
    #     return statute



    def type_elegible_for_expungement(self): #this method iterates through the ineligeble list and searches for the statute specified #todo: this probably needs to be done in the charge class

        #todo: add check for felony A or B

        print("analyzing: " + self.statute_string)

        for item in IneligibleCrimesList:

            if len(item) == 2: # if this is a range of values

                lower_chapter = item[0][0:3]
                lower_subchapter = item[0][4:7]

                upper_chapter = item[1][0:3]
                upper_subchapter = item[1][4:7]

                if self.chapter <= upper_chapter and self.chapter >= lower_chapter:
                    if self.subchapter <= upper_subchapter and self.subchapter >= lower_subchapter:

                        print("FALSE" + str(item))
                        return [False, item] #return false and the reason why its false

            else: # this is a discrete value
                if item == self.statute_string:
                    print('FALSE ' + item)
                    return [False, item]

        print(self.statute_string + " TRUE !!!!")
        return True


    # Commented this out until we comlplete the parser logic for these

    # def __str__(self):
    #     # TODO do these need to have leading zeros?
    #     statute = '{}'.format(self.chapter)
    #     if self.subchapter:
    #         statute = '{}.{:03d}'.format(statute, self.subchapter)
    #     if self.section:
    #         statute = '{} {}'.format(statute, self.section)
    #     if self.subsection:
    #         statute = '{}({})'.format(statute, self.subsection)
    #     return statute


if __name__ == '__main__':

    #some testing stuff

    list = ['803455',
            '483050',
            '163.175',
            '811175',
            '8111751',
            '806010',
            '8111751',
            '806010',
            '8112101B',
            '163.375',
            '163.427',
            '163.160(2)',
            '163.095',
            '163.095',
            '163.095',
            '166.085',
            '163.427',
            '163.427',
            '161.405(2)(c)',
            '163.095',
            '163.095',
            '163.095',
            '166.085',
            '161.405(2)(a)',
            '163.375',
            '163.427',
            '163.425',
            '163.415',
            '163.415',
            '110151',
            '811110',
            '811100',
            '811100C',
            '43',
            '811.100',
            '43',
            '43',
            '811.100',
            '43',
            '314.075',
            '314.075',
            '314.075']

    for item in list:
        newStatute = Statute(item)
        newStatute.type_elegible_for_expungement()


    exit()

