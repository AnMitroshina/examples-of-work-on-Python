#! /usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
from decimal import Decimal

parser = argparse.ArgumentParser(description='Choose room')
parser.add_argument('a', type=Decimal, help='длина комнаты М')
parser.add_argument('b', type=Decimal, help='ширина комнаты М')
parser.add_argument('c', type=Decimal, help='длина комнаты Р')
parser.add_argument('d', type=Decimal, help='длина комнаты Р')


args = parser.parse_args()

if args.a * args.b > args.c * args.d:
    print('M')
elif args.a * args.b < args.c * args.d:
    print('P')
elif args.a * args.b == args.c * args.d:
    print('E')




