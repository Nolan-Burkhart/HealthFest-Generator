#My NolanCFG Reader
import re
import copy

class settings:
  settings = dict()
  def __init__(self):
    self.settings = dict()
  def get_setting(self, name):
    if name in self.settings.keys():
      if self.settings[name][1] == "str":
        return self.settings[name][0]
      elif self.settings[name][1] == "int":
        return int(self.settings[name][0])
      elif self.settings[name][1] == "arr":
        return copy.deepcopy((self.settings[name][0]))
      else:
        print("Config Error: Type "+self.settings[name][1]+" not recongnized")
        return "Error"
    else:
      return "Not Found"
  def add_setting(self, name, value):
    self.settings[name] = value
  def get_settings(self):
    return self.settings.keys()

SEARCHES = ["(?P<key>.*) = \[(?P<array_raw>.*)\] as Array","(?P<key>.*) = (?P<value>.*) as (?P<type>.*)","(?P<key>.*) = (?P<value>.*)"]

class settings_loader:
  f = ""
  result = settings()
  def __init__(self, f):
    self.f = f
    self.result = settings()
    self.load_settings()
  def load_settings(self):
    file_reader = open(self.f) #open our file
    line = file_reader.readline() #read first line
    while line:
      unignored_key = line.find(" -+")
      if unignored_key != -1:
        line = line[:unignored_key]
      print(line)
      if len(line) > 1:
        for search in SEARCHES:
          match = re.search(search,line)
          if match is not None:
            self.line_handler(search,line,match)
            break
      line = file_reader.readline()
    return self.result
  def line_handler(self, search, text, regex):
    #dont you love not having switch statements
    if search == "(?P<key>.*) = \[(?P<array_raw>.*)\] as Array":
      array_clean = regex.group("array_raw").split(",")
      for i in range(len(array_clean)):
        if array_clean[i][0] == " ":
          array_clean[i] = array_clean[i][1:]
      self.result.add_setting(regex.group("key"),[array_clean,"arr"])
    elif search == "(?P<key>.*) = (?P<value>.*) as (?P<type>.*)":
      if regex.group("type") == "String":
        self.result.add_setting(regex.group("key"),[regex.group("value"),"str"])
      elif regex.group("type") == "Int":
        self.result.add_setting(regex.group("key"),[regex.group("value"),"int"])
    elif search == "(?P<key>.*) = (?P<value>.*)":
      self.result.add_setting(regex.group("key"),[regex.group("value"),"str"])

      


