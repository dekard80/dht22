# read the configuration file
# the configuration file must be written in the form: key=value
# you can add comments:
# # comment
# or:
# key=value # comment
# the getValue() method always returns strings
# conf equals None if the file does not exist or contains no valid lines

class Config:
    conf = {}

    def __init__(self, file_name):
        try:
            with open(file_name, "r") as f:
                for line in f:
                    line = line.replace(" ", "")
                    line = line.replace("\n", "")
                    if line == "" or line.startswith("#") or line.count("=") != 1:   # noqa: E501
                        continue
                    if "#" in line:
                        line = line[:line.find("#")]
                    line = line.split("=")
                    if line[0] == "" or line[1] == "":
                        continue
                    self.conf[line[0]] = line[1]
                if self.conf.__len__() == 0:
                    self.conf = None
        except FileNotFoundError:
            self.conf = None

    def isValid(self):
        if self.conf is None:
            return False
        else:
            return True

    def getValue(self, key):
        if self.conf is not None:
            if key in self.conf:
                return self.conf[key]
        return None
