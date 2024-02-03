import re


def extract_numericals(inValue):
    match = re.search(r'\((\d+)\)', inValue)

    if match:
        numerical_value = int(match.group(1))
        print("Numerical Value:", numerical_value)
    else:
        print("No numerical value found in the given text.")
    return numerical_value