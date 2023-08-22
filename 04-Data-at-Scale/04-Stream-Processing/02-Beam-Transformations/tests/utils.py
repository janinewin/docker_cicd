import os
import ast


def load_intermediate_output(folder, pattern):
    list_files = os.listdir(folder)
    file_path = ""
    for file in list_files:
        if os.path.isfile(os.path.join(folder, file)):
            if pattern in file:
                file_path = os.path.join(folder, file)
                break

    if len(file_path) > 0:
        l = []
        with open(file_path) as f:
            l = f.readlines()
        return l
    return None


def convert_string_eval(str_txt):
    try:
        return ast.literal_eval(str_txt.strip("\n"))
    except:
        return None


def sort_lower(l):
    if l is not None:
        key_output = [x.lower() for x in l]
        key_output.sort()
        return key_output
    return None
