import datetime

def date2obj(input_date):

    """
        Converts a date string into a date object

    Args:
        string: a string in date format mm/dd/yyyy
    Returns:
        a datetime object
    """

    if type(input_date) == datetime.date: #if this is already a datetime object then do nothing.
        return input_date
    else:

        #parse the date
        month, day, year = map(int, input_date.split("/"))
        date_obj = datetime.date(year, month, day)

        return date_obj

"""this is only used when loading locally stored html files"""

def file2string(location):
    with open(location, 'r') as myfile:
        filedata = myfile.read()

    myfile.close()
    return filedata


