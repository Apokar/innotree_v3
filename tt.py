#!/usr/bin/python
# -*- coding: utf-8 -*-

import time


def test():
    for i in range(20):
        if i <18:
            print i
            time.sleep(0.5)
        else:
            print 'daole '
            quit()


if __name__ == '__main__':
    test()
