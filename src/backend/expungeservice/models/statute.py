


# I am fairly certain that section and subsection are irrelevant to the analyzers logic


# the way i currently have this configured completely discards section and subsection,  cameron - jan 3 2019

#todo: find out if section and subsection are relevant

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

        self.parse_string()

        # TODO we may need to add components beyond subsection

    def parse_string(self):
        statute_string = self.statute_string
        if len(str(statute_string))>=6: #todo: this is wrong but will kinda work for everything on our list except marijuana crimes.

            statute_string = statute_string.lower() #convert to lowercase
            statute_string = [char for char in statute_string if char not in "abcdefghijklmnopqrstuvwxyz!@#$%^&*() .,;'[]<>?:{}\""] #remove all other chars #todo: fix this it could include weird chars
            statute_string = ''.join(statute_string)
            statute_string = statute_string[0:6] #trim to only first 6

            self.chapter = statute_string[0:3]
            self.subchapter = statute_string[3:7]
            self.statute_string = str(self.chapter) + '.' +str(self.subchapter)

    # todo: commented because im not sure if it still works
    # def __eq__(self, other):
    #     return (self.chapter == other.chapter and
    #             self.subchapter == other.subchapter and
    #             ((not self.section and not other.section) or
    #              self.section == other.section) and
    #             ((not self.subsection and not other.subsection) or
    #              self.subsection == other.subsection))

    def __str__(self):
        return str(self.statute_string)

    # def __dict__(self):
    #     return {'statute_string': self.statute_string,
    #             'chapter': self.chapter,
    #             'subchapter': self.subchapter,
    #             'section': self.section,
    #             'subsection': self.subsection
    #             }

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
