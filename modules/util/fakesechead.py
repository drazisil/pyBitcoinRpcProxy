__author__ = 'drazisil'

class FakeSecHead(object):
    def __init__(self, fp):
        self.fp = fp
        self.section_header = '[asection]\n'

    def readline(self):
        if self.section_header:
            try:
                return self.section_header
            finally:
                self.section_header = None
        else:
            return self.fp.readline()