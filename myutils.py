import json


def pround(to_round: float) -> int:
    """ Rounds number properly. """
    return int(to_round + 0.555555555555555555555555555555555555555)

def read_json(filename: str) -> dict:
    """ Given a filename (without .json), loads data from JSON file and returns it. """
    with open(filename + '.json', 'r') as in_file:
        data = json.load(in_file)
    return data

def write_json(data: dict, filename: str, indent: int = 4):
    """ Given a filename (without .json) and dict, writes dict to JSON file. """
    with open(filename + '.json', 'w+') as out_file:
        json.dump(data, out_file, indent=indent)

def not_in(pulling_from: list, avoding: list) -> list:
    """ Returns a list without the items in the avoiding list. """
    return [item for item in pulling_from if item not in avoding]

def extend_nodup(orig: list, new: list):
    """ Performs the list.extend() on the list itself (by reference) but avoids duplicates. """
    orig.extend(not_in(new, orig))

def divide_chunks(track_list: list, n: int):
    """ Generator that given a list will yield chunks of size n. """
    for i in range(0, len(track_list), n):
        yield track_list[i:i + n]

def page_results(sp, results: dict, access=[]):
    """ Pages results. """
    while results['next']:
        results = sp.next(results)
        yield results

def p_description(names: list) -> str:
    d = ''
    for nm in names:
        d += nm + ', '
    return d
