#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division, print_function

import re
import json
import requests


def get_number_of_citations(url):
    r = requests.get(url)
    try:
        r.raise_for_status()
    except Exception as e:
        print(e)
        return None
    results = re.findall("([0-9]+) results", r.text)
    if not len(results):
        print("no results found")
        return None
    try:
        return int(results[0])
    except Exception as e:
        print(e)
        return None


def update_others():
    with open("other_pubs.json", "r") as f:
        pubs = json.load(f)
        for i, pub in enumerate(pubs):
            if not pub["url"].startswith("https://scholar.google.com"):
                continue
            n = get_number_of_citations(pub["url"])
            if n is None or n < pub["citations"]:
                continue
            pubs[i]["citations"] = n

    with open("other_pubs.json", "w") as f:
        json.dump(pubs, f, sort_keys=True, indent=2, separators=(",", ": "))


if __name__ == "__main__":
    update_others()
