from generator import student
def loadCSV(path,settings):
  students = []
  z = open(path)
  keys = z.readline().rstrip().split(',')
  line = z.readline()
  while line:
    data = line.rstrip().split(',')
    d = dict()
    for i in range(0,len(data)):
      if keys[i] == "Grade":
        d[keys[i]] = int(data[i])
      else:
        d[keys[i]] = data[i]
    students.append(student(d,settings.get_setting("Choice Field")))

    line = z.readline()
  return students