import os
import csv

# Path to collect data from the Resources folder
csvpath = os.path.join('election_data.csv')


with open(csvpath, newline='') as csvfile:

    # CSV reader specifies delimiter and variable that holds contents
    csvreader = csv.reader(csvfile, delimiter=',')

    print(csvreader)

    csv_header = next(csvreader)
    print(f"CSV Header: {csv_header}")


#calculate each of the following: 
#The total number of votes cast



#A complete list of candidates who received votes


#The percentage of votes each candidate won


#The total number of votes each candidate won


#The winner of the election based on popular vote.

