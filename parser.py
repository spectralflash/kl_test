#!/usr/bin/env python3
"""Test exercise, details: https://github.com/silversum/test"""
import gzip
from typing import TextIO
from pprint import pprint


def chunks(file_obj: TextIO):
    """
    :param file_obj: text file or file-like object opened for reading
    :return: parsed data dictionaries as an iterator object
    """
    chunk = {}
    key = None
    for line in file_obj.readlines():
        if line.startswith('#'):
            continue
        if not line.strip():
            if chunk:
                yield strip_linebreaks(chunk)
            chunk = {}
            continue
        if line.startswith(' '):
            if key is None:
                raise SyntaxError(f'Bad start of a data block, '
                                  f'expected "id: value": {line}')
            chunk[key] += line.lstrip()
        else:
            if ':' not in line:
                raise SyntaxError(f'Expected "id: value", got: {line}')
            key, val = line.split(':', maxsplit=1)
            val = val.lstrip()
            # If a key is already there, append. If the key is new, assign.
            if key in chunk:
                chunk[key] += val
            else:
                chunk[key] = val
    # Yield the last chunk, for the cases
    # when there is no line break in the end of the file.
    if chunk:
        yield strip_linebreaks(chunk)


def parse_file(path: str):
    """
    :param path: path to the file to parse
    :return: parsed data dictionaries as an iterator object
    """
    if path.lower().endswith('.gz'):
        def opener():
            return gzip.open(path, 'rt')
    else:
        def opener():
            return open(path, 'r', buffering=1, encoding='utf-8-sig')
    with opener() as file_obj:
        yield from chunks(file_obj)


def strip_linebreaks(chunk: dict):
    """
    :param chunk: key/value dictionary
    :return: key/value dictionary, trailing line breaks removed from values
    """
    return {k: v.rstrip('\n') for k, v in chunk.items()}


if __name__ == '__main__':
    for elem in parse_file('example.txt'):
        pprint(elem)
