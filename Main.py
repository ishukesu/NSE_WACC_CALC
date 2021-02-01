import yfinance as yf
import numpy
import statistics
import pandas
import bs4 as bs
import requests

Countryname='India'
Stock=input('Ticker:')
#Country=["United States","China","Japan","Germany","United Kingdom","India","France","Italy","Canada","Russia"]
#Indicel=["^DJI","000001.SS","^N225","^GDAXI","^FTSE","^BSESN","^FCHI","FTSEMIB.MI","XIU.TO","IMOEX.ME"]
#Indicelol=pandas.DataFrame(Indicel,Country)
ticker=Stock+'.NS'
stockf=yf.Ticker(ticker)
indicef=yf.Ticker('^BSESN')
Indice=indicef.history(period="3650d",interval="1d")
Stockd =stockf.history(period="3650d",interval="1d")
Main= pandas.merge(Indice['Open'],Stockd['Open'],on=["Date"])
Mainchange=Main.pct_change()
Mainchange=Mainchange.drop(Mainchange.index[[0]])

us="^TNX"
USAf=yf.Ticker(us)
USArate=USAf.history(period="3650d",interval="1d")
USAr=USArate.mean()

URL='http://pages.stern.nyu.edu/~adamodar/New_Home_Page/datafile/ctryprem.html'
url_link = requests.get(URL)
file = bs.BeautifulSoup(url_link.text, "lxml")
find_table = file.find_all('table')[0]
rows = find_table.find_all('tr')
pp=0
c= []
rf= []
for i in rows:
    pp=pp+1
    table_data = i.find_all('td')
    data = [j.text for j in table_data]
    if pp>1 and pp<159:
        coun=data[0].strip()
        coun=coun.replace("\n","")
        c.append(coun.replace("                    "," "))
        rf.append(float(data[3][slice(0,4)]))
rfrate=pandas.DataFrame(rf,c)

RiskFreerate=(USAr[0]+rfrate.loc['India'][0])/100
Beta=numpy.polyfit(Mainchange['Open_x'],Mainchange['Open_y'],1)[0]
Marketreturn=Mainchange["Open_x"].mean()*365
Ke=RiskFreerate+Beta*(Marketreturn-RiskFreerate)

print("Risk Free rate:",RiskFreerate*100,"%")
print("Beta:",Beta)
print("Market Return:",Marketreturn*100,"%")
print("Ke:",Ke*100,"%")

#yahoo_financials = YahooFinancials(ticker)
#BS=yahoo_financials.get_financial_stmts('annual','balance')
#for key, value in BS.items():
    #for key1,value1 in value.items():
        #for key2,value2 in value1[0].items():
            #print(value2)
URL='https://www.screener.in/company/'+Stock+'/consolidated/'
url_link = requests.get(URL)
file = bs.BeautifulSoup(url_link.text, "lxml")
find_table = file.find_all('table')[6]
rows = find_table.find_all('tr')
n=0
for i in rows:
    n=n+1
    table_data = i.find_all('td')
    data = [j.text for j in table_data]
    if n==4:
         borrowing=float(data[12].replace(",",""))*pow(10,7)
    if n==2:
        ShareCapital=float(data[12].replace(",",""))*pow(10,7)
    if n==3:
        Reserves=float(data[12].replace(",",""))*pow(10,7)
find_table = file.find_all('table')[1]
rows = find_table.find_all('tr')
n=0
for i in rows:
    n=n+1
    table_data = i.find_all('td')
    data = [j.text for j in table_data]
    if n==7:
        interest=float(data[12].replace(",",""))*pow(10,7)

URL='https://tradingeconomics.com/country-list/corporate-tax-rate'
url_link = requests.get(URL)
file = bs.BeautifulSoup(url_link.text, "lxml")
find_table = file.find_all('table')[0]
rows = find_table.find_all('tr')
n=0
count=[]
rate=[]
for i in rows:
    n=n+1
    table_data = i.find_all('td')
    data = [j.text for j in table_data]
    if n>1:
        count.append(data[0].replace("\n","").strip())
        rate.append(data[1].strip())
taxratetable=pandas.DataFrame(rate,count)
taxrate=float(taxratetable.loc['India'][0])/100
print('Interest:',interest)
print('Borrowings:',borrowing)
print('Tax Rate:',taxrate*100,'%')
kd=(interest/borrowing)*(1-taxrate)
print('Kd:',kd*100,'%')

Marketcap=stockf.info['marketCap']
WaccBV=Ke*((ShareCapital+Reserves)/(ShareCapital+Reserves+borrowing))+kd*((borrowing)/(ShareCapital+Reserves+borrowing))
WaccMV=Ke*((Marketcap)/(Marketcap+borrowing))+kd*((borrowing)/(Marketcap+borrowing))
print("WACC BV:",WaccBV*100,'%')
print('WACC MV:',WaccMV*100,'%')
cs2=input("CSV final answers(Y/N):")
if cs2=='Y':
    dat={'Risk Free rate':RiskFreerate,'Beta':Beta,'Market Return':Marketreturn,'Ke':Ke,'Interest':interest,'Borrowings':borrowing,'Tax Rate':taxrate,'Kd':kd,'WACC BV':WaccBV,'WACC MV':WaccMV}
    fin=pandas.DataFrame(data=dat,index=[0])
    fin.to_csv("Ans.csv")
