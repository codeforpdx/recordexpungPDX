from objbrowser import browse


from tests.fixtures.john_doe import JohnDoe # this is the pre downloaded john doe record in HTML format
from expungeservice.analyzer.client_builder import BuildClientObject



"""
this is the placeholder for actual unit tests, it allows you to create a client object and inspect it with the object inspector gui
note: case[0] should have correct charge info, but cases 1 and 2 will just have charge data from case 0 since we dont have any more examples to test with
"""

#todo: write actual unit tests with pytest
#todo: fix DOB

if __name__ == '__main__':

    print("analyzer prototype")

    client = BuildClientObject(JohnDoe.RECORD)

    browse(client)





