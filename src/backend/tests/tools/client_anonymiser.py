


def search_and_replace_preserve_case(file_path, search_text, replacement_text):

    with open(file_path) as f:
        lowerd =  f.read()
        newText = lowerd.replace(search_text, replacement_text)

    with open(file_path, "w") as f:
        f.write(newText)

def search_and_replace(file_path, search_text, replacement_text):

    with open(file_path) as f:
        lowerd =  f.read()
        newText = lowerd.replace(search_text, replacement_text)

    with open(file_path, "w") as f:
        f.write(newText)


def do_folder(dir_path, search_text, replacement_text):
    import os

    # traverse root directory, and list directories as dirs and files as files
    for root, dirs, files in os.walk(dir_path):
        path = root.split(os.sep)

        for file in files:

            file_path = dir_path + os.sep + file

            #search_and_replace(file_path, search_text, replacement_text)
            search_and_replace_preserve_case(file_path, search_text, replacement_text)


if __name__ == '__main__':
    do_folder("/home/cameron/PycharmProjects/recordexpungPDX/src/backend/tests/fixtures/html/litter", "doot", "doe")


