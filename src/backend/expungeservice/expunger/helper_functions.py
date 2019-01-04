import datetime

def date2obj(input_date):

    """
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
