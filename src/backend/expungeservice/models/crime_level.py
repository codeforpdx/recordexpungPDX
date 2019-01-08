
# TODO we may need to change this to Enum since only a few valid values are allowed.

import collections
import enum

import logging

class CrimeLevel(object):
    """ Crime Level.

    Describes crime level. e.g. Felony Class A.

    Attributes:
        type_: A string describing the type of crime.
        class_: A string of length 1 specifying the class.
    """
    def __init__(self, level_string, type_=None, class_=None,):
        self.type_ = type_
        self.class_ = class_
        self.level_string = level_string


        self.parse_string_from_crawler(level_string)

    def __str__(self):
        if self.class_:
            return '{} Class {}'.format(self.type_, self.class_)
        else:
            return self.type_

    # def __dict__(self):
    #     return {'type': self.type_,
    #             'class': self.class_,
    #             'level_string':self.level_string #todo: find if this is necessary
    #             }

    #todo: on the ward weaver case detailpage8.html the crime level is "death", this is probably a non issue but we should devise a better way to handle that

    def parse_string_from_crawler(self, level_string): #todo: move this to the parser

        try:

            level_string = level_string.upper().split()

            if len(level_string) == 3:

                if 'VIOLATION' in level_string[0]:
                    self.type_ = 'VIOLATION'
                if 'INFRACTION' in level_string[0]:
                    self.type_ = 'INFRACTION'
                elif 'MISDEMEANOR' in level_string[0]:
                    self.type_ = 'MISDEMEANOR'
                elif 'FELONY' in level_string[0]:
                    self.type_ = 'FELONY'
                elif 'DEATH' in level_string[0]: #this is a wild guess but im pretty sure any crime recieveing the death penelty would be a felony
                    self.type_ = 'FELONY'

                self.class_ = level_string[2].upper() #set crime class (a, b, c, d)
        except:
            logging.info('parse_string_from_crawler got a None string ')


