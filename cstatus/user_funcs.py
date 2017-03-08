"""
User-defined functions, e.g. callback functions for status bar clicks go here
"""


def logout(button, *_):
    import os
    if button == 1:
        os.system("i3-msg exit")
