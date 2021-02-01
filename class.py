import numpy
import statistics
import pandas

Financial_data=[[11279.96,13072.1,15644.44,9708.5,17527.77,19445.22,17404.2,18835.77,22386.27,27957.49],[517.7,341.55,297.65,76.45,239.6,318.7,424.4,284.5,301.35,444.75]]
USARf=0.04
Indiapre=0.025
Interestamt=4500000000
borrowing=30000000000
taxrate=0.25
ShareCapital=30000000000
Reserves=30000000000
Marketcap=90000000000

data=pandas.DataFrame(Financial_data).transpose()
data.columns=['Sensex','Raymond']
datachange=data.pct_change()
datachange=datachange.drop(datachange.index[[0]])

Riskfreerate=USARf+Indiapre
Beta=numpy.polyfit(datachange['Sensex'],datachange['Raymond'],1)[0]
Marketreturn=datachange['Sensex'].mean()
ke=Riskfreerate+Beta*(Marketreturn-Riskfreerate)

print("Risk Free rate:",Riskfreerate*100,"%")
print("Beta:",Beta)
print("Market Return:",Marketreturn*100,"%")
print("Ke:",ke*100,"%")

kd=(Interestamt/borrowing)*(1-taxrate)
print('Interest:',Interestamt)
print('Borrowings:',borrowing)
print('Tax Rate:',taxrate*100,'%')
print('Kd:',kd*100,'%')

WaccBV=ke*((ShareCapital+Reserves)/(ShareCapital+Reserves+borrowing))+kd*((borrowing)/(ShareCapital+Reserves+borrowing))
WaccMV=ke*((Marketcap)/(Marketcap+borrowing))+kd*((borrowing)/(Marketcap+borrowing))
print("WACC BV:",WaccBV*100,'%')
print('WACC MV:',WaccMV*100,'%')
