from django.shortcuts import render,redirect,HttpResponse
import io
from xlsxwriter.workbook import Workbook
import csv
import pandas as pd
import xlrd
from datetime import datetime
from datetime import date, timedelta
import random

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

def index(request): 
    return render(request,'index.html')
def convert(request):
    if request.method=='POST':
        df = pd.read_csv(request.FILES['pdfFile'])
        
        start_date=request.POST.get('startdate')
        end_date=request.POST.get('enddate')
        holiday_dates=request.POST.get('holidaydates')
        holiday_dates_list = holiday_dates.split(',')
        date_format = '%m/%d/%Y'
        
        no_of_holidays=0
        print(holiday_dates_list)
        holiday_dates=[]
        for i in holiday_dates_list:
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
        available_days.append('Emp. Code')
        available_days.append(' NAME')
        
        for single_date in daterange(datetime.strptime(start_date,date_format), datetime.strptime(end_date,date_format)):
            available_days.append(str(single_date.day)+" "+WEEKDAYS[int(single_date.weekday())])
            
        df.drop(df.columns[3:], axis=1, inplace=True)
        new_df=pd.DataFrame(columns=available_days)
        df=pd.concat([df,new_df])
        num_rows = int(df.shape[0])
        
        print("No. of rows",num_rows)
        
        
        col=list(df.columns)
        num_col=len(col)
        print("No. of col",num_col)
        
        for i in range(0,num_rows):
            list_iterator=0
            present_days=random.randrange(int(no_of_days*0.8),int(no_of_days*0.9))
            present_days_list=distribute_attendance(present_days,no_of_days)
            for j in range(3,num_col):
                if col[j][len(col[j])-1]=='U' or col[j] in holiday_dates:
                    df.iloc[i,j] = '_'
                else:   
                    # print(present_days_list[list_iterator])
                    # print(list_iterator)
                    df.iloc[i,j] = present_days_list[list_iterator]
                    list_iterator+=1
        
        print(df)    
        df.to_csv('output'+str(request.FILES['pdfFile']))   
    return redirect('index')


