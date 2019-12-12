class student:
  d = dict()
  assigned = 1
  sessions = []
  choice_names = []
  choices_recieved = []
  def __init__(self, dictionary, choice_names):
    self.choices_recieved = []
    self.d = dictionary
    self.sessions = [-1,-1,-1]
    self.assigned = 1
    self.choice_names = choice_names
  def fill_vaping(self):
    self.sessions[abs(self.d["Grade"]-11)] = 0 #set vaping class

#our class or session. limited to 1 person for testing purposes
class session:
  students = []
  size_cap = 0
  size = 0
  block = 0
  name = ""
  session_id = 0
  def __init__(self,block,session_id,name,size):
    self.students = []
    self.size_cap = size
    self.block = block
    self.name = name
    self.session_id = session_id
    if name == "Vaping":
      self.size = self.size_cap
  def increment(self):
    self.size += 1
  def has_room(self):
    return self.size < self.size_cap
  def add_student(self,student):
    self.students.append(student)
    self.increment()

#our schedule, a glorified matrix generator/holder
class schedule:
  matrix = []
  def __init__(self,periods,sessions,size_cap):
    for i in range(periods):
      arr = []
      for x in range(len(sessions)): #class size
        arr.append(session(i,x,sessions[x],size_cap))
      self.matrix.append(arr)
  def get_session(self,period,name):
    for z in self.matrix[period]:
      if z.name == name:
        return z

# Sorts array with mergesort greatest to least using a value in dictionary
# Precondition: SORT_CRTIERIA is a valid key in all student dictionaries
def sort_students(array, settings):
  if len(array) > 1:
    sort_criteria = settings.get_setting("Sort Delimeter")
    midpoint = len(array)//2
    left = array[:midpoint]
    right = array[midpoint:]

    sort_students(left,settings)
    sort_students(right,settings)

    left_index = 0
    right_index = 0
    array_index = 0

    while left_index < len(left) and right_index < len(right):
      if (left[left_index].d[sort_criteria] > right[right_index].d[sort_criteria]):
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
def make_schedule(students, schedule, settings):
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
          choice_num = int(schedule.get_session(i,x.d[choice]).session_id)
          if (got_assigned):
            break
          for b in range(0,len(x.sessions)):
            if (got_assigned):
              break
            if x.sessions[b] == -1 and schedule.matrix[b][choice_num].has_room():
              schedule.matrix[b][choice_num].add_student(x)
              x.sessions[b] = choice_num
              x.choices_recieved.append(choice)
              x.choice_names.remove(choice)
              x.assigned = x.assigned + 1
              got_assigned = True
              break

def fill_unassigned(students, schedule):
  for student in students:
    for i in range(len(student.sessions)):
      if student.sessions[i] == -1:
        lowest = 20
        lowest_session = schedule.matrix[i][0]
        for session in schedule.matrix[i]:
          if session.size < lowest and session.class_id not in student.sessions:
            lowest_session = session
            lowest = session.size
        student.sessions[i] = lowest_session.class_id
        lowest_session.has_room()
        lowest_session.add_student(student)

""" Override
for i in range(len(students)):
  if students[i].d["First Name"] == "Nolan" and students[i].d["Last Name"] == "Burkhart":
    students[i].assigned = 3
    students[i].sessions = [8,7,1]
    students[i].choices_recieved = ["First Choice","Second Choice"]
    for s in range(len(students[i].sessions)):
      schedule.matrix[s][students[i].sessions[s]-1].has_room()
      schedule.matrix[s][students[i].sessions[s]-1].add_student(students[i])
"""