"""
User-defined functions, e.g. callback functions for status bar clicks go here
"""


def logout(*args):
    import os
    os.system("i3-msg exit")
