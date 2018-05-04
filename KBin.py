#!/bin/env python

def inttobar(i):
    ex = 0
    while i > 2 ** (ex + 1):
        ex += 1

    bar = []
    while ex >= 0:
        if (i >= 2 ** ex):
            bar.insert(0, True)
            i -= 2 ** ex
        else:
            bar.insert(0, False)
        ex -= 1

    return bar

def bartoint(bar):
    ex = 0
    i = 0
    for x in bar:
        if x:
            i += 2 ** ex
        ex += 1
    return i
