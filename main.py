from icalendar import Calendar, Event
import psycopg2
import json

config = json.load(open("appsettings.json"))

g = open('calendar.ics','rb')
gcal = Calendar.from_ical(g.read())

conn = psycopg2.connect(database=config["database"],
                        host=config["db_host"],
                        user=config["db_user"],
                        password=config["db_pass"],
                        port=config["db_port"])

with conn.cursor() as cursor:
    for component in gcal.walk():
        if component.name == "VEVENT":
            description = component['summary']
            if not description in config["excluded_holidays"]:
                startDateBase = str(component['DTSTART'].to_ical()).strip("b'").strip("'")
                endDateBase = str(component['DTEND'].to_ical()).strip("b'").strip("'")
                
                startDate = "{0}-{1}-{2}".format(startDateBase[0:4], startDateBase[4:6], startDateBase[6:8])
                endDate = "{0}-{1}-{2}".format(endDateBase[0:4], endDateBase[4:6], endDateBase[6:8])
                
                cursor.execute("SELECT * FROM dates WHERE calendar = '{0}' AND date = '{1}'".format("NO", startDate))
                
                if len(cursor.fetchall()) == 0:
                    cursor.execute("INSERT INTO dates(calendar, date, description) VALUES('{0}', '{1}', '{2}')".format("NO", startDate, str(description).replace("'", "")))
                    
                    print(description)
                    print(startDate)
                    print(endDate)
                
conn.commit()
conn.close()

g.close()
