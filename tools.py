import re
from typing import Iterator


def build_query(it: Iterator, cmd: str, value: str) -> Iterator:
    """
    :param it: запрос пользователя
    :param cmd: команда - filter, map, unique, sort, limit, regex
    :param value: аргумент с работой с 'cmd'
    """
    res = iter(map(lambda v: v.strip(), it))
    if cmd == 'filter':
        return filter(lambda v: value in v, res)
    if cmd == 'map':
        arg = int(value)
        return map(lambda v: v.split(' ')[arg], res)
    if cmd == 'unique':
        return iter(set(res))
    if cmd == 'sort':
        reverse = value == 'desc'
        return iter(sorted(res, reverse=reverse))
    if cmd == 'limit':
        return get_limit(res, int(value))
    if cmd == 'regex':
        regex = re.compile(value)
        return filter(lambda v: regex.findall(v), res)
    return res


def get_limit(it: Iterator, value: int) -> Iterator:
    n = 0
    for item in it:
        if n < value:
            yield item
        else:
            break
        n += 1

