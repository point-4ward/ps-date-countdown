today = datetime.datetime.now().date()

name = data.get('name')
type = data.get('type')
sensorName = "sensor.{}_{}".format(type , name.replace(" " , "_"))

dateStr = data.get('date')
dateSplit = dateStr.split("/")

dateDay = int(dateSplit[0])
dateMonth = int(dateSplit[1])
dateYear =  int(dateSplit[2])
date = datetime.date(dateYear , dateMonth , dateDay)

thisYear = int(today.year)
nextOccur = datetime.date(thisYear , dateMonth , dateDay)

numberOfDays = 0
years = dateYear - thisYear

# if the year is "next year" or further
if years > 0:
  nextOccur = datetime.date(dateYear , dateMonth , dateDay)
  numberOfDays = (nextOccur - today).days
else:
  
  numberOfDays = (nextOccur - today).days
  # if event has passed this year
  if numberOfDays < 0:
    nextYear = thisYear + 1
    nextOccur = datetime.date(nextYear , dateMonth , dateDay)
    numberOfDays = (nextOccur - today).days
    years = years + 1

defaultFriendlyName = ''

if type.lower() == 'birthday':
  defaultFriendlyName = "{}'s {}".format(name , type)
else:
  defaultFriendlyName = "{} {}".format(name , type)

hass.states.set(sensorName , numberOfDays ,
  {
    "icon" : data.get("icon", "mdi:calendar-star"),
    "unit_of_measurement" : "days" ,
    "friendly_name" : data.get('friendly_name', defaultFriendlyName),
    "nextoccur" : "{}/{}/{}".format(nextOccur.day , nextOccur.month , nextOccur.year) ,
    "years" : years
  }
)
