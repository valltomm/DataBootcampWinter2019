import os
import csv

# Path to collect data from the Resources folder
csvpath = os.path.join('election_data1.csv')


with open(csvpath, newline='') as csvfile:

    # CSV reader specifies delimiter and variable that holds contents
    csvreader = csv.reader(csvfile, delimiter=',')

    print(csvreader)

    csv_header = next(csvreader)
    print(f"CSV Header: {csv_header}")

    votes = []

    khan = []
    correy = []
    li = []
    otooley = []

    #The total number of votes cast
    for row in csvreader:
        votes.append(row[0])


    print(" ")
    print("Election Results")
    print("-----------------------------------")
    print("Total Votes: ", len(votes))

    #A complete list of candidates who received votes

    candidate = []

    #for row in csvreader:
    #    candidates.append(row[2])
    
    for row in csvreader:
        candidate.append(row[2])
    
    print("Candidates:", candidate)


    #The percentage of votes each candidate won



    #The total number of votes each candidate won



    #The winner of the election based on popular vote
