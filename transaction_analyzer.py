import csv
import gspread
import re
import time
import os

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo

import pandas as pd
import matplotlib.pyplot as plt

root = tk.Tk()
root.title('Tkinter open File Dialog')
root.resizable(False, False)
root.geometry('300x150')

plt.style.use('bmh')

month = 'august'
transactions =[]
file = f"cimb_{month}.csv"



def convToNum(stringToConvert):
    listOfNumbers = re.findall('\d+\.\d+', stringToConvert)
    numbers = "".join(str(x) for x in listOfNumbers)
    if len(listOfNumbers) ==0:
        numbers = '0'
    
    return numbers

categories = {"I-FUNDS":"Instant transfer in", "IBG CREDIT":"Interbank transfer in", "ATM WITHDRAWAL":"ATM Withdrawal", "CREDIT INTEREST":"Interest", "DUITNOW TO ACCOUNT":"Transfer money to other account", "MYDEBIT PURCHASE":"Debit card payment", "BULK SETTLEMENT CR":"PTPTN payment in", "BULK SETTLEMENT DR":"PTPTN payment out", "I-PAYMENT":"Online purchase",  "POS DEBIT":"Debit card payment"  }

def sortCategories(ctgry):
    for x in categories.keys():
        if x in ctgry:
            return categories[x]
        
def cimbFin(filename):
    x = []
    y = []
    a = []
    b = []
    cost = []
    cat = []
    ttl =[]
    with open(filename, mode='r') as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            #print(row)
            if row[0] == 'Date':
                continue
            date = row[0]
            details = row[1]
            total = float(convToNum(row[2])) - float(convToNum(row[3]))
            #total = float(row[2]) - float(row[3])
            #category ='other'
            category = sortCategories(details)
            if category == None:
                category ="Others"
            transaction = ((date, details, category, total))
            
            cost.append([category, total])
            
            
            if total <0:
                y.append((-1)* total)
                x.append(category)
            elif total > 0:
                a.append(total)
                b.append(category)
            #print(transaction)
            transactions.append(transaction)
        
        cost = sorted(cost)
        for i in range(len(cost)):
            if cost[i][0] not in cat:
                cat.append(cost[i][0])
                ttl.append(abs(cost[i][1]))
            else:
                val = abs(cost[i][1]) + abs(cost[i-1][1])
                ttl.pop()
                ttl.append(val)
            
                
        
        plt.pie(ttl, labels=cat, autopct='%1.2f%%')
        plt.show()
        #print(y)
        


def select_file():
    filetypes = (
        ('text files', '*.txt'),
        ('All files', '*.*')
    )


    filename = fd.askopenfilename(
        title='Open a file',
        initialdir='/',
        filetypes=filetypes
    )
    cimbFin(os.path.basename(filename))
    #showinfo(
     #       title ='Selected File',
      #      message= os.path.basename(filename)
      #  )

open_button = ttk.Button(
    root,
    text='Open a File',
    command=select_file
)

open_button.pack(expand=True)

root.mainloop()




    