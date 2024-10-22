import urllib3
import re

# https://stackoverflow.com/questions/1007481/how-to-replace-whitespaces-with-underscore
def urlify(s):

    # Remove all non-word characters (everything except numbers and letters)
    s = re.sub(r'[^\w\s-]', '', s).strip() 

    # Replace all runs of whitespace with a single dash
    s = re.sub(r"\s+", '-', s)

    s = urllib3.util.parse_url(s).url

    return s