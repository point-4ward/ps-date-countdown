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

nextOccurYear = int(today.year)
nextOccur = datetime.date(nextOccurYear , dateMonth , dateDay)

if nextOccur < date:
  # date must be the first occurrence
  nextOccur = date

if nextOccur < today:
  # if event has passed this year, nextOccur is next year
  nextOccurYear = nextOccurYear + 1
  nextOccur = datetime.date(nextOccurYear, dateMonth, dateDay)

numberOfDays = 0
years = nextOccurYear - dateYear

if years < 0:
  # if years is negative, then date is more than 365 days away
  # nextOccur will be the first occurrence
  years = 0

numberOfDays = (nextOccur - today).days

friendly_name = ''

if type.lower() == 'birthday':
  friendly_name = "{}'s {}".format(name , type)
else:
  friendly_name = "{} {}".format(name , type)

hass.states.set(sensorName , numberOfDays ,
  {
    "icon" : "mdi:calendar-star" ,
    "unit_of_measurement" : "days" ,
    "friendly_name" : friendly_name,
    "nextoccur" : "{}/{}/{}".format(nextOccur.day , nextOccur.month , nextOccur.year) ,
    "years" : years
  }
)
