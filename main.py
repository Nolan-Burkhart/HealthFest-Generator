import random
import csv
from random import randint

SORT_CRITERIA = "Grade"
SIZE_CAP = 0

class student:
  d = dict()
  assigned = 1
  sessions = []
  choice_names = []
  def __init__(self, dictionary):
    self.d = dictionary
    self.sessions = [-1,-1,-1]
    self.assigned = 1
    self.choice_names = ["Preferences [First Choice]","Preferences [Second Choice]","Preferences [Third Choice]","Preferences [Fourth Choice]"]
    self.update_choice_names()
  def fill_vaping(self):
    self.sessions[abs(self.d["Grade"]-11)] = 1 #set vaping class
  def update_choice_names(self):
    for i in self.choice_names:
      self.d[i] = self.d[i].split(" ")[0][1:].replace(":","")

#our class or session. limited to 1 person for testing purposes
class session:
  size_cap = 0
  size = 0
  block = 0
  class_id = 0
  def __init__(self,block,class_id):
    self.size_cap = SIZE_CAP
    self.block = block
    self.class_id = class_id
    if class_id == 1:
      self.size = self.SIZE_CAP
  def increment(self):
    self.size += 1
  def has_room_check(self):
    return self.size < self.size_cap
  def has_room(self):
    if self.has_room_check():
      self.increment()
      return True
    else:
      return False

#our schedule, a glorified matrix generator/holder
class schedule:
  matrix = []
  def __init__(self):
    for i in range(1,4):
      arr = []
      for x in range(1,13): #class size
        arr.append(session(i,x))
      self.matrix.append(arr)


def loadCSV(path):
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
    students.append(student(d))

    line = z.readline()
  return students

# Sorts array with mergesort greatest to least using a value in dictionary
# Precondition: SORT_CRTIERIA is a valid key in all student dictionaries
def sort_students(array):
  if len(array) > 1:
    midpoint = len(array)//2
    left = array[:midpoint]
    right = array[midpoint:]

    sort_students(left)
    sort_students(right)

    left_index = 0
    right_index = 0
    array_index = 0

    while left_index < len(left) and right_index < len(right):
      if (left[left_index].d[SORT_CRITERIA] > right[right_index].d[SORT_CRITERIA]):
        array[array_index] = left[left_index]
        left_index += 1
      else:
        array[array_index] = right[right_index]
        right_index += 1
      array_index += 1
    
    while left_index < len(left):
      array[array_index] = left[left_index]
      left_index += 1
      array_index += 1
    
    while right_index < len(right):
      array[array_index] = right[right_index]
      right_index += 1
      array_index += 1

#the for loops made me kinda loopy
def make_schedule(students, schedule):
  for i in range(len(students)):
    students[i].fill_vaping()
  for i in range(len(students[0].sessions)): #start the loop
    for x in students:
      got_assigned = False
      if x.assigned < len(x.sessions):
        if (got_assigned):
          break
        for choice in x.choice_names:
          print(x.d[choice])
          choice_num = int(x.d[choice])
          if (got_assigned):
            break
          for b in range(0,len(x.sessions)):
            if (got_assigned):
              break
            if x.sessions[b] == -1 and schedule.matrix[b][choice_num-1].has_room():
              x.sessions[b] = choice_num
              x.choice_names.remove(choice)
              x.assigned = x.assigned + 1
              got_assigned = True
              break

def fill_unassigned(students, schedule):
  for student in students:
    for i in range(len(student.sessions)):
      if student.sessions[i] == -1:
        pot = []
        for session in schedule.matrix[i]:
          if session.has_room_check():
            pot.append(session)
        new_assignment = random.choice(pot)
        pot.has_room()
        student.sessions[i] = new_assignment.class_id

literal_names = ["#1 Vaping: What We Know Right Now","#2 A 'Shot' of Information", "#3 Latest Trends in Sexually Transmitted Infections","#4: Plugging In: Power and Connection","#5 Anxiety and Depression in Teens,#10 Exercise and Medicine","#6 Understanding Eating Disorders","#7 Yoga","#8 Mindfulness","#9 A 2190 Mile Mindset","#10 Exercise and Medicine","#11 How to Fuel Your Body for Optimal Performance & The Effects of Stress on the Body","#12 Poisoning Prevention: Not Just for *Little* Kids"]

schedule = schedule()
students = loadCSV("results.csv")
sort_students(students)
make_schedule(students, schedule)
fill_unassigned(students,schedule)
print("Schedules:")


with open('output.csv', mode='w') as output_file:
  output_writer = csv.writer(output_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
  output_writer.writerow(['Email Address','Block 1', 'Block 2', 'Block 3'])
  for x in students:
    row = []
    row.append(x.d["Email Address"])
    for z in range(len(x.sessions)):
      row.append(literal_names[x.sessions[z]-1])
    output_writer.writerow(row)
  