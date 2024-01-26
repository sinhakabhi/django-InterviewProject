import csv
from DummyApp.models import Author

with open('InterviewProject\Library_Authors.csv', mode ='r') as file:
    csvFile = csv.reader(file)
    for lines in csvFile:
            Author.objects.update_or_create(name=lines)
