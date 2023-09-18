import csv

# Create a new CSV file

header = ["id", "name", "age"]

with open("new.csv", "w") as file:
    writer = csv.writer(file)
    writer.writerow(header)
