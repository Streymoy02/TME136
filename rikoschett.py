#Rune Streymoy 0205171739

import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import numpy as np
from pickle import TRUE
import pandas as pd

def readStockData(filename):
# Läs in aktiefilen, välj ut rätt data och placera i en dataframe
# Returna dataframe

    file = pd.read_csv(filename,  decimal=',', sep=';')
    stock = pd.DataFrame(file, columns=['Date', 'High price', 'Low price', 'Closing price'] )
    list = []

    for i in range(len(stock)):
        rikoRange = ((stock.loc[i]['Closing price']-stock.loc[i]['Low price'])/(stock.loc[i]['High price']-stock.loc[i]['Low price']))
        list.append(rikoRange)    
        
    stock['Range'] = list
    stock = stock[::-1].reset_index(drop=TRUE)

    return(stock)

def simulateStrategy(stock):
# Silmulera Rikoschett-strategin med datan från readStockData
# Simulerings resultaten sparas i en dataframe
# Den simulerade procentuella förändringen av kapital sparas i en array
# Returna dataframe och array

    buy = []
    sell = []
    days = []
    transaction = pd.DataFrame()

    for i in range(len(stock)-5):   
        if stock.loc[i]['Range'] <= 0.1:    
            stockBuy = stock.loc[i]['Closing price']
            buy.append(stockBuy)
            for h in range(1, 6):
                if stockBuy < stock.loc[i+h]['Closing price']:
                    sell.append(stock.loc[i+h]['Closing price'])
                    days.append(h)
                    break
                elif h == 5:
                    sell.append(stock.loc[i+h]['Closing price'])
                    days.append(h)
                    break
        # Rikoschett-simulering
                
    transaction['buy'] = buy
    transaction['sell'] = sell
    transaction['days'] = days
    transaction['gain'] = (transaction['sell'] - transaction['buy'])/transaction['buy']
        #Simuleringsresultat 

    money_list = [100]
    for i in range(len(transaction)):
        money_list.append(money_list[i]*(1.0 + transaction['gain'][i]))
    money = np.array(money_list)
        #Procentuella förändringen av kapital
    print(money)
    return(transaction, money)

def printAndPlotResult(stock, transaction, money):
# Tar in data från simulateStrategy och readStockData
# Skapar hist och linjegraf med datan från simulateStrategy
# Visar grafer, skriver ut resultat i terminalfönstret samt sparar resultat som fil
 
    transaction_days = transaction['days'] 
    transaction_gain = transaction['gain'] 

    #Histogram
    fig, ax1 = plt.subplots()
    ax1.hist(100*transaction['gain'], bins = 10) 
    ax1.set_xlabel('resultat [%]')        
    ax1.set_ylabel('frekvens')

    #Linjegraf
    fig, ax2 = plt.subplots()
    ax2.plot(range(len(money)), money)
    plt.grid() 
    ax2.set_xlabel('trades')        
    ax2.set_ylabel('kapital')
    ax2.yaxis.set_major_formatter(mtick.PercentFormatter()) 
        #https://stackoverflow.com/questions/31357611/format-y-axis-as-percent
    plt.show()


    rikoträff = 0
    for i in range(len(transaction_gain)):
        if  transaction_gain[i] > 0:
            rikoträff = rikoträff + 1
        # Kollar hur många gånger vi hamnar i rikochett-zonen

    #Lista för enklare utskrift av resultat
    utskrift = [
        f'Totalt antal dagar i data: {len(stock)}',
        f'Antal rikoschett-lägen: {len(transaction_gain)} ({len(transaction_gain)/len(stock):.2%})',
        f'Genomsnittligt utfall: { transaction_gain.mean():.2%}',
        f'Genomsnittlig träffsäkerhet: {rikoträff/len(transaction_gain):.1%}',
        f'Genomsnittligt antal dagar i affär: {transaction_days.mean():.3}']

    #Utskrift av resultat till terminal och fil
    f = open("myResult.txt","w")   
    for i in range(len(utskrift)):
        print(utskrift[i])
        f.write(utskrift[i])
        f.write("\n")
    f.close()

    return()

filename = 'ERIC_B-2015-10-01-2022-09-26.csv'
    # Input av fil

stock = readStockData(filename)
transaction, money = simulateStrategy(stock)
printAndPlotResult(stock, transaction, money)