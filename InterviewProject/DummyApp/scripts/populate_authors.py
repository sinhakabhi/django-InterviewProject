# import csv
# from DummyApp.models import Author, Book, Member

# def run():
#     # with open('Library_Authors.csv', mode ='r') as file:
#     #     csvFile = csv.reader(file)
#     #     for lines in csvFile:
#     #         Author.objects.update_or_create(name=lines[0])
    

#     with open('Library_Books.csv', mode ='r') as file:
#         csvFile = csv.reader(file)
#         for lines in csvFile:
#             author = Author.objects.get(name=lines[1])
#             Book.objects.update_or_create(name=lines[0], author=author, total_copies =1, available_copies=1)
            

    
#     # with open('Library_Members.csv', mode ='r') as file:
#     #     csvFile = csv.reader(file)
#     #     for lines in csvFile:
#     #         Member.objects.update_or_create(name=lines[0])
