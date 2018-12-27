


# I am fairly certain that section and subsection are irrelevant to the analyzers logic
#todo: find out if section and subsection are relevant

#todo: find out the various formats that these strings are in, and write some parser logic for that.


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


    def __str__(self):
        return str(self.statute_string)


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

