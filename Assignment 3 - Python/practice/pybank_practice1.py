import os
import csv

# Path to collect data from the Resources folder
csvpath = os.path.join('budget_data.csv')


with open(csvpath, newline='') as csvfile:

    # CSV reader specifies delimiter and variable that holds contents
    csvreader = csv.reader(csvfile, delimiter=',')

    print(csvreader)

    csv_header = next(csvreader)
    print(f"CSV Header: {csv_header}")

    PL = []
    date = []
    PL_change = []

    #sum of PL (row[1) and total months (row[0]) 
    for row in csvreader:
        PL.append(float(row[1]))
        date.append(row[0])
    
    print(" ")
    print("Financial Analysis")
    print("-----------------------------------")
    print("Total Months: ", len(date))
    print("Total Profit/loss: $ ", sum(PL))

    #find difference between each PL row - put into PL_change []
    #average of those differences
    #date of max and min PL change

    for i in range(1,len(PL)):
        PL_change.append(PL[i] - PL[i-1])   
        avg_PL_change = sum(PL_change)/len(PL_change)

        max_PL_change = max(PL_change)

        min_PL_change = min(PL_change)

        max_PL_change_date = str(date[PL_change.index(max(PL_change))])
        min_PL_change_date = str(date[PL_change.index(min(PL_change))])


    print("Average Profit/Loss Change: $", round(avg_PL_change))
    print("Greatest Increase in Profits:", max_PL_change_date,"($", max_PL_change,")")
    print("Greatest Decrease in Profits:", min_PL_change_date,"($", min_PL_change,")")  