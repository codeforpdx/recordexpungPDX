import datetime
import json, jsonpickle

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

def file2string(location):
    """this is only used when loading locally stored html files"""
    with open(location, 'r') as myfile:
        filedata = myfile.read()

    myfile.close()
    return filedata

def OBJtoJSON(self):
    serialized = jsonpickle.encode(self.__dict__())
    serialized = json.dumps(json.loads(serialized), indent=2)
    return serialized
    # print(yaml.dump(yaml.load(serialized), indent=2))


