# timesheet accepts data in format of: [name, date, start time, end time, break time, total time]

import os
from pandas import read_csv
from pathlib import Path
import csv

def main():

    timeSheetPath = Path(__file__).parents[2] / "data" / "timeSheet.csv"
    tempFilePath = Path(__file__).parents[2] / "data" / "tempFile.csv"

    df = read_csv(timeSheetPath)
    df.columns = ["Name", "Date", "Start Time", "End Time", "Break Time", "Total Time"]
    df.to_csv(timeSheetPath, index=False)

    while True:

        # learn what user wants to do (add, edit, delete, view, exit)

        pathway = input("What would you like to do? (add, edit, delete, view, sum, exit): ").lower()

        # if exit, exit

        if pathway == "exit":
            exit()


        name = input("What is your name? ")

        # if add, ask for name, date, start time, end time, break time, total time

        if pathway == "add":
            date = input("What is the date? (mm/dd/yyyy): ")
            start_time = input("What time did you start? (hh:mm): ")
            end_time = input("What time did you end? (hh:mm): ")
            break_time = input("How long was your break? (hh:mm): ")
            # calculate total time
            t_time = (int(end_time.split(":")[0]) - int(start_time.split(":")[0]) - int(break_time.split(":")[0])) * 60 + (int(end_time.split(":")[1]) - int(start_time.split(":")[1]) - int(break_time.split(":")[1]))
            hrs, mins = divmod(t_time, 60)
            if t_time <= 60:
                t_time = 60
            elif hrs >= 1:
                if mins >= 30:
                    mins = 0
                    hrs += 1
            total_time = str(hrs) + ":" + str(mins)

            # write data to file

            with open(timeSheetPath, "a", newline="") as file:
                addWriter = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

                addWriter.writerow([name, date, start_time, end_time, break_time, total_time])

        # if edit, ask for name, show options of dates, ask for date, allow user to edit 

        elif pathway == "edit":

            # TODO: FUNDAMENTAL FLAW IS THAT IT ASKS FOR DATE, BUT THERE CAN BE MULTIPLE ENTRIES FOR A DATE

            with open(timeSheetPath, "r") as file:
                editReader = csv.reader(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                data = list(editReader)

            for line in data:
                if line[0] == name:
                    print(line)

            date = input("What is the date of the entry you want to edit? (mm/dd/yyyy): ")

            entries = []

            for line in data:
                if line[1] == date:
                    entries.append(line)

            if len(entries) > 1:
                print("There are multiple entries for this date. Please choose one of the following: ")
                for entry in entries:
                    print(entry)

            which_entry = input("What is the start time of the entry you want to edit? (hh:mm): ")
            entry = []

            for e in entries:
                if e[2] == which_entry:
                    entry = e
            

            start_time = input("What time did you start? (hh:mm): ")
            end_time = input("What time did you end? (hh:mm): ")
            break_time = input("How long was your break? (hh:mm): ")
            # calculate total time
            t_time = (int(end_time.split(":")[0]) - int(start_time.split(":")[0]) - int(break_time.split(":")[0])) * 60 + (int(end_time.split(":")[1]) - int(start_time.split(":")[1]) - int(break_time.split(":")[1]))
            hrs, mins = divmod(t_time, 60)
            if t_time <= 60:
                t_time = 60
            elif hrs >= 1:
                if mins >= 30:
                    mins = 0
                    hrs += 1
            total_time = str(hrs) + ":" + str(mins)



            new_entry = [name, date, start_time, end_time, break_time, total_time]

            # write data to file

            with open(timeSheetPath, "r") as file_input:
                editReader = csv.reader(file_input, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                with open(tempFilePath, "w", newline="") as output: 
                    editWriter = csv.writer(output, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                    for line in list(editReader):
                        if line != entry:
                            editWriter.writerow(line)
                    editWriter.writerow(new_entry)

            os.replace(tempFilePath, timeSheetPath)            

        # if delete, ask for name, show options of dates, ask for date, delete

        elif pathway == "delete":
            with open(timeSheetPath, "r") as file:
                deleteReader = csv.reader(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                data = list(deleteReader)

            for line in data:
                if line[0] == name:
                    print(line)

            date = input("What is the date of the entry you want to delete? (mm/dd/yyyy): ")

            for line in data:
                if line[1] == date:
                    entry = line

            with open(timeSheetPath, "r") as file_input:
                deleteReader = csv.reader(file_input, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                with open(tempFilePath, "w", newline="") as output: 
                    deleteWriter = csv.writer(output, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                    for line in list(deleteReader):
                        if line != entry:
                            deleteWriter.writerow(line)

            os.replace(tempFilePath, timeSheetPath)

        # if view, ask for name, show data

        elif pathway == "view":
            with open(timeSheetPath, "r") as file:
                viewReader = csv.reader(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                data = list(viewReader)

            for line in data:
                if line[0] == name:
                    print(line)

        elif pathway == "sum":
            with open(timeSheetPath, "r") as file:
                sumReader = csv.reader(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                data = list(sumReader)

            total_time = 0

            for line in data:
                if line[0] == name:
                    total_time += int(line[5].split(":")[0]) * 60 + int(line[5].split(":")[1])

            hrs, mins = divmod(total_time, 60)
            print("Total time worked: " + str(hrs) + ":" + str(mins))

        else:
            print("Invalid input. Please try again.")

if __name__ == "__main__":
    main() 