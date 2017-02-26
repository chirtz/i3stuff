import sys


class Tools:
    """
    Static function inclusion
    """

    # If we are running cstatus.py standalone, assume I3 mode
    if sys.modules["__main__"].__file__.endswith("cstatus.py"):
        I3 = True

        @classmethod
        def sym(cls, text):
            return "<span face='FontAwesome'>%s</span>" % text
    else:  # otherwise, assume CBar mode
        I3 = False

        @classmethod
        def sym(cls, text):
            return text
