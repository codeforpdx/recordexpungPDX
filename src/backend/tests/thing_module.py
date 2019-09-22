


class Thing:

    def give_stuff(self):
        return "the real stuff"


def get_stuff_from_thing():

    return Thing().give_stuff()


print("this is called before defining the calling code:\n", Thing())

def calling_a_thing():
    res = Thing().give_stuff()
    print("in the caller, the get_stuff result is:", res)
    return res