class LogErrors:
    def __init__(self, func):
        self.func = func
        self.logfile = "debug.txt"

    def __call__(self, *args, **kwargs):
        try:
            out = self.func(*args, **kwargs)
            return out
        except Exception as e:
            with open(self.logfile, 'a') as f:
                f.write("Error in {}:\n{}\n".format(self.func.__name__,
                                                    str(e)))


def debug_log(s):
    with open("debug.txt", 'a') as f:
        f.write(s + "\n")
