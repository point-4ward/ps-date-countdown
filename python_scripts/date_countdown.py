##########
#
# Date Countdown
#
# A python_script for homeassistant by mf_social
#
##########


# Get the basic information to do the calculations
today = datetime.datetime.now().date()
name = data.get('name')
eventType = data.get('type')
defaultFriendlyName = ''
numberOfDays = 0


# Convert the date we got
dateStr = data.get('date')
dateSplit = dateStr.split("/")

dateDay = int(dateSplit[0])
dateMonth = int(dateSplit[1])
dateYear =  int(dateSplit[2])
date = datetime.date(dateYear , dateMonth , dateDay)


# Calculate the next occurrence
nextOccurYear = int(today.year)
nextOccur = datetime.date(nextOccurYear , dateMonth , dateDay)

if nextOccur < date:
  # date must be the first occurrence
  nextOccur = date

if nextOccur < today:
  # if event has passed this year, nextOccur is next year
  nextOccurYear = nextOccurYear + 1
  nextOccur = datetime.date(nextOccurYear, dateMonth, dateDay)

years = nextOccurYear - dateYear

if years < 0:
  # if years is negative, then date is more than 365 days away
  # nextOccur will be the first occurrence
  years = 0

numberOfDays = (nextOccur - today).days


# Set the default friendly name
if eventType.lower() == 'birthday':
  # add an apostophe for birthdays
  defaultFriendlyName = "{}'s {}".format(name , eventType)
else:
  defaultFriendlyName = "{} {}".format(name , eventType)


# Sanitise the entity_id to meet the criteria by
# replacing Scandanavian characters and spaces
name1 = name.replace("Æ" , "AE")
name2 = name1.replace("Ø" , "O")
name3 = name2.replace("Å" , "AA")
name4 = name3.replace("æ" , "ae")
name5 = name4.replace("ø" , "o")
name6 = name5.replace("å" , "aa")
safeName = name6.replace(" " , "_")
sensorName = "sensor.{}_{}".format(eventType , safeName)


# Send the sensor to homeassistant
hass.states.set(sensorName , numberOfDays ,
  {
    "icon" : data.get("icon", "mdi:calendar-star"),
    "unit_of_measurement" : "days" ,
    "friendly_name" : data.get('friendly_name', defaultFriendlyName),
    "nextoccur" : "{}/{}/{}".format(nextOccur.day , nextOccur.month , nextOccur.year) ,
    "years" : years
  }
)
