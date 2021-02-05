
import re

def get_domain_from_url(url):
    return re.search("^(?:https?:\/\/)?(?:[^@\n]+@)?(?:www\.)?([^:\/\n?]+)\.",url)

