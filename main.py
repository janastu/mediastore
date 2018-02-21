#!/usr/bin/env python
#-*- coding: utf-8 -*-

from mediastore import app
import sys

def main():
    app.run(host="0.0.0.0", port=8000, ssl_context='adhoc')

if __name__ == '__main__':
    main()
