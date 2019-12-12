import random
import settings
from random import randint
from csv import *
from generator import *
from settings import *
#from PIL import Image, ImageDraw, ImageFont



settings = settings_loader("settings.ncfg")
settings = settings.result
schedule = schedule(3,settings.get_setting("Sessions"),settings.get_setting("Session Size Cap"))
students = loadCSV("requests.csv",settings)
sort_students(students,settings)
make_schedule(students, schedule, settings)
for s in students:
  print(s.d["First Name"]+str(s.sessions))
