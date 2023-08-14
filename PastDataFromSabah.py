import requests
import bs4
import time
from datetime import date
import pandas as pd
import datetime
from dateutil.relativedelta import relativedelta 
import os


class PastDataFromSabahFinance:

    def DateValues(self,index):
        self.index=index
        DateValues=[]
        today = datetime.datetime.today()
        DateValues.append((today-relativedelta(days=index)).day)
        DateValues.append((today-relativedelta(days=index)).month)
        DateValues.append((today-relativedelta(days=index)).year)
        return DateValues

    def all_values(self,index):
        Data=PastDataFromSabahFinance()
        self.index=index
        DateValues=Data.DateValues(index)
        result=[];
        try:
            r=requests.get(f"https://www.sabah.com.tr/finans/borsa/gecmis-kapanislar?gun={DateValues[0]}&ay={DateValues[1]}&yil={DateValues[2]}&tip=Hisse")
            soup=bs4.BeautifulSoup(r.text,"lxml")
            AllCode=soup.select("td")
            
            for td in AllCode:
                result.append(td.getText().strip())
        except:
            print(str(DateValues[0])+"."+str(DateValues[1])+"."+str(DateValues[2])+" gununde veri alinamadi")
        
        
        return result

    def CompanyAndPrices(self,index):
        Data = PastDataFromSabahFinance()
        dict_list=[]
        self.index=index
        AllData=Data.all_values(index)
        DateValues=Data.DateValues(index)
        day=str(DateValues[0])+"."+str(DateValues[1])+"."+str(DateValues[2])
        index2=8
        while index2<len(AllData)-86:

            stock={ 'Stock Name': AllData[index2], str(day): AllData[index2+1]}
            index2+=9
            dict_list.append(stock)
        
        return dict_list



def GetOpeningDataAndCompanyNames(days):
    
    Data = PastDataFromSabahFinance()
    df_main=pd.DataFrame(Data.CompanyAndPrices(0))
    today = datetime.datetime.today()
    for index in range(0,days):
        if ((today-relativedelta(days=index)).weekday()==5 or (today-relativedelta(days=index)).weekday()==6):
            pass
        else:
            df=pd.DataFrame(Data.CompanyAndPrices(index))
            print(today-relativedelta(days=index))
            try:
                df_main=pd.merge(df,df_main,how='right')
            except:
               print(str(today-relativedelta(days=500))+" datasi alinamadi.") 
           
    return df_main


def main():
    days=int(input("Please specify how many days you want to download the stock market values: "))

    df=GetOpeningDataAndCompanyNames(days)
    
    path= os.getcwd()
    df.to_excel(path+ "\\GecmisData"+str(days)+'.xlsx',index=False)
    print("Warning: Because the program does not dowload weekend values, number of columns in excel sheet can be less than the value entered by you. ")
    print("Data stored at: "+path+ "\\GecmisData"+str(days)+'.xlsx')
main()
