import re

# TODO Compile regexp
# TODO Migrate to an object

def normalize_link(text):
    urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', text)
    for url in urls:
        text = text.replace(url, ' URL ')
    return text


def normalize_users(text):
    users = re.findall('@[^ @]*', text)
    for user in users:
        text = text.replace(user, ' @USER ')
    return text


def normalize_hashtags(text):
    htags = re.findall('#[^ #]*', text)
    for htag in htags:
        text = text.replace(htag, htag[1:]+" ")
    return text


def normalize(text):
    text = text.lower()
    text = normalize_link(text)
    text = normalize_users(text)
    text = normalize_hashtags(text)

    return text