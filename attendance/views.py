from django.shortcuts import render,redirect,HttpResponse
import io
from xlsxwriter.workbook import Workbook
import csv
import pandas as pd
import xlrd
from datetime import datetime
from datetime import date, timedelta
import random
from django.urls import reverse
import numpy as np
import openpyxl
import os
def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)+1):
        yield start_date + timedelta(n)


def distribute_attendance(present_days, total_days):
    present_days = present_days
    attendance = ['P'] * present_days + ['A'] * (total_days - present_days)
    random.shuffle(attendance)   
    return attendance

WEEKDAYS={
    0:"M",
    1:"T",
    2:"W",
    3:"TH",
    4:"F",
    5:"S",
    6:"SU",   
}
DAYS_31=['01','03','05','07','08','10','12']
DAYS_30=['04','06','09','11']
DAYS_29=['02']
def index(request): 
    return render(request,'index.html')
def convert(request):
    if request.method=='POST':
        df = pd.read_csv(request.FILES['pdfFile'])
        
        start_date = request.POST.get('startdate')
        end_date = request.POST.get('enddate')
        holiday_dates = request.POST.get('holidaydates')
        month = request.POST.get('month')
        batch = request.POST.get('batch')
        batch_no=batch
        batch = "BATCH "+str(batch)
        print(month)
        
        holiday_dates_list = holiday_dates.split(',')
        date_format = '%m/%d/%Y'
        
        no_of_holidays=0
        print(holiday_dates_list)
        holiday_dates=[]
        
        for i in holiday_dates_list:
            if i!='':
                date=WEEKDAYS[datetime.strptime(i,date_format).weekday()]
                if date!='SU':
                    no_of_holidays+=1
                    holiday_dates.append(str(datetime.strptime(i,date_format).day)+" "+str(date))
                
                
        no_of_sundays=0
        date_format = '%Y-%m-%d'
        for single_date in daterange(datetime.strptime(start_date,date_format), datetime.strptime(end_date,date_format)):
            if WEEKDAYS[int(single_date.weekday())]=='SU':
                no_of_sundays+=1
        
        print("Holidays",no_of_holidays)
        print(no_of_sundays)
        
        no_of_days=abs((datetime.strptime(end_date,date_format).date()-datetime.strptime(start_date,date_format).date()).days)+1
        no_of_days=no_of_days-(no_of_sundays+no_of_holidays)
        available_days=[]
        available_days.append('MAHAJYOTI KVY BATCH ID')
        available_days.append('Student Name')
        print(month[5:])
        month_days=""
        if month[5:] in DAYS_31:
            month_days+="-31"
            for single_date in daterange(datetime.strptime(str(month)+"-01",date_format), datetime.strptime(str(month)+"-31",date_format)):
                available_days.append(str(single_date.day)+" "+WEEKDAYS[int(single_date.weekday())])
        if month[5:] in DAYS_30:
            month_days+="-30"
            for single_date in daterange(datetime.strptime(str(month)+"-01",date_format), datetime.strptime(str(month)+"-30",date_format)):
                available_days.append(str(single_date.day)+" "+WEEKDAYS[int(single_date.weekday())])
        if month[5:] in DAYS_29:
            month_days+="-29"
            for single_date in daterange(datetime.strptime(str(month)+"-01",date_format), datetime.strptime(str(month)+"-29",date_format)):
                available_days.append(str(single_date.day)+" "+WEEKDAYS[int(single_date.weekday())])        
        available_days.append('P')
        available_days.append('A')
        available_days.append('L')
        available_days.append('H') 
        available_days.append('HP')
        available_days.append('WO')
        available_days.append('WOP')
        df = df[['BATCHWISE SR.NO.','MAHAJYOTI KVY BATCH ID', 'Student Name']]
        new_df=pd.DataFrame(columns=available_days)
        df=pd.concat([df,new_df])
        df=df.loc[df['BATCHWISE SR.NO.'] == batch]


        num_rows = int(df.shape[0])
        
        print("No. of rows",num_rows)
        
        
        col=list(df.columns)
        num_col=len(col)
        print("No. of col",num_col)
        
        unnecessary_days=[]
        if abs(datetime.strptime(start_date,date_format)-datetime.strptime(str(month)+"-01",date_format))!=0:
           for single_date in daterange(datetime.strptime(str(month)+"-01",date_format), datetime.strptime(start_date,date_format)):
                unnecessary_days.append(str(single_date.day)+" "+WEEKDAYS[int(single_date.weekday())]) 
           unnecessary_days.remove(str(datetime.strptime(start_date,date_format).day)+" "+WEEKDAYS[int(datetime.strptime(start_date,date_format).weekday())])
           
        if abs(datetime.strptime(end_date,date_format)-datetime.strptime(str(month+month_days),date_format))!=0:
           for single_date in daterange(datetime.strptime(end_date,date_format), datetime.strptime(str(month+month_days),date_format)):
                unnecessary_days.append(str(single_date.day)+" "+WEEKDAYS[int(single_date.weekday())]) 
           unnecessary_days.remove(str(datetime.strptime(end_date,date_format).day)+" "+WEEKDAYS[int(datetime.strptime(end_date,date_format).weekday())])
        # print(df)
        for i in range(0,num_rows):
            list_iterator=0
            present_days=random.randrange(int(no_of_days*0.85),int(no_of_days))
            present_days_list=distribute_attendance(present_days,no_of_days)
            present_days_list.append(present_days_list.count('P'))
            present_days_list.append(present_days_list.count('A'))
            present_days_list.append(0)
            present_days_list.append(no_of_holidays+no_of_sundays)
            present_days_list.append(0)
            present_days_list.append(0)
            present_days_list.append(0)
            
            for j in range(3,num_col):
                if col[j][len(col[j])-1]=='U' or col[j] in holiday_dates or col[j] in unnecessary_days:
                    df.iloc[i,j] = '_'
                else:   
                    # print(present_days_list[list_iterator])
                    # print(list_iterator)
                    df.iloc[i,j] = present_days_list[list_iterator]
                    list_iterator+=1
            
            
        print(df)
        df=df.drop(columns=['BATCHWISE SR.NO.'])
        df.index = np.arange(1, len(df)+1) 
        path=r"output/"+"Batch_"+str(batch_no)+".xlsx"
        
        if os.path.isfile(path):
            with pd.ExcelWriter(path=path, engine='openpyxl', mode='a') as writer:  
                df.to_excel(writer,index=True,index_label='Sr.No.',sheet_name=str(start_date)+" to "+str(end_date))
        else:
            with pd.ExcelWriter(path=path, engine='openpyxl', mode='w') as writer:  
                df.to_excel(writer,index=True,index_label='Sr.No.',sheet_name=str(start_date)+" to "+str(end_date))         
    return redirect('index')


