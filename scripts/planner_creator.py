from datetime import date
import datetime

#Reading a json file and changing item name
#import json
#
#with open('/home/vetinari/Projects/BookBinding/Scripts/template_example.json') as f:
#	d = json.load(f)
#	print(d)
#	scribus.gotoPage(1)
#	d = scribus.getPageItems()
#	for item in d:
#		print("{}".format(item))
#		#scribus.setItemName(item[0] + "_new", item[0])



# setitemname -> maybe to update item name instead of using copy
#Function to update text, that doesn't keep the text alignment.
def updateText(replacement, item):
	fontName = scribus.getFont(item)
	fontSize = scribus.getFontSize(item)
	scribus.deleteText(item)
	scribus.insertText(replacement, 0, item)
	scribus.setFont(fontName, item)
	scribus.setFontSize(fontSize, item)

# Function that updates text using a workaround found here:  https://forums.scribus.net/index.php?topic=2615.0
def updateTextKeepLayout(replacement, item):
	l = scribus.getTextLength(item)
	scribus.selectText(0, l-1, item)
	scribus.deleteText(item)
	scribus.insertText(replacement, 0, item)
	l = scribus.getTextLength(item)
	scribus.selectText(l-1, 1, item)
	scribus.deleteText(item)
	print("Overflow: {}".format(scribus.textOverflows(item)))
	print("Text Lines: {}".format(scribus.getTextLines(item)))

page=1
pagecount=scribus.pageCount()
monthLbl = None
dayLbl = None
dayOfWeekLbl = None

numberOfDays = int(scribus.valueDialog("Number of days: ", "The number of days to create in this planner", "31"))
# Let's reset the progress bar
scribus.progressReset()
scribus.progressTotal(numberOfDays)
print("NoDays: {}".format(numberOfDays))
inputStartDate = scribus.valueDialog("Start Date: ", "The start Date for this planner", str(date.today()))
tdate = date.fromisoformat('2025-01-01')
tdate = date.fromisoformat(str(inputStartDate))
print("Input date: {}".format(tdate))
if pagecount > 0:
	print("Count: " + str(pagecount))
	scribus.progressSet(page)
	while page < numberOfDays:
		print("Currently at page: {}".format(page))
		scribus.gotoPage(page)
		scribus.statusMessage("Creating page number: {}".format(page))
		d = scribus.getPageItems()
		docname = getDocName()
		template_page = scribus.getMasterPage(1)
		scribus.importPage(docname, tuple([(1)]))
		d = scribus.getPageItems()
		for item in d:
			print(item)
			if "MonthLbl" in item[0]:
				monthLbl = item
				#l = scribus.getTextLength(item[0])
				#scribus.selectText(0, l-1, item[0])
				#scribus.deleteText(item[0])
				monthName = tdate.strftime("%B")
				#updateText(monthName, item[0])
				updateTextKeepLayout(monthName, item[0])
				#scribus.insertText(monthName, 0, item[0])
				print("monthLbl")
			if "WeekLbl" in item[0]:
				WeekDayLbl = item
				weekDay = tdate.strftime("%A")
				updateTextKeepLayout(weekDay, item[0])
				print("WeekDayLbl")
			if "DayLbl" in item[0]:
				dayLbl = item
				updateTextKeepLayout(str(tdate.day), item[0])
				print("DayLbl")
		scribus.redrawAll()
		tdate += datetime.timedelta(days=1)
		print("Date: {}".format(tdate))
		page = page+1
		scribus.progressSet(page)
	scribus.messageBox("Creation Completed", "Finished creating planner. Number of days: {}".format(page), icon=scribus.ICON_INFORMATION)
