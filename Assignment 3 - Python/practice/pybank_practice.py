import os
import csv

# Path to collect data from the Resources folder
csvpath = os.path.join('budget_data.csv')

#with open(csvpath, newline='') as csvfile:

with open(csvpath, newline='') as csvfile:

    # CSV reader specifies delimiter and variable that holds contents
    csvreader = csv.reader(csvfile, delimiter=',')

    csv_header = next(csvreader)

    # read each row after the header and count number of rows (months)
    for row in csvreader:
        months = sum(1 for row in csvreader)
        #print (months)
        
   
    #total the Profit/Losses column 
    total = 0
    for row in csvreader:
        total += float(row[1])
        #print(total)

    
    #The average of the changes in "Profit/Losses" over the entire period
    #average = total / len(months)
    for row in csvreader:
        average_change






        #The greatest increase in profits (date and amount) over the entire period



        #The greatest decrease in (PROFITS?) losses (date and amount) over the entire period



# Export file as txt

