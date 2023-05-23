# -*- coding:utf-8 -*-
#!/usr/bin/python
import json
import time


def Run():
    try:
        [CODE]
    except Exception as e:
        return format(e)


if __name__ == '__main__':
    dicts = {
        'RunTime': 0,
        'Memory': 0,
        'Result': '',
    }

    start = time.perf_counter()
    dicts['Result'] = str(Run())
    dicts['RunTime'] = round((time.perf_counter() - start) * 1000, 2)

    json_dicts = json.dumps(dicts)
    print(json_dicts)