#Detta program läser in data från en json-fil, varav datan sedan används för att plotta ut en graf samt skriva ut en tabell i terminalfönstret
#Skapad av Rune Streymoy (020517)
#Senast ändrad: 26-09-2022

import json
import matplotlib.pyplot as plt
import pandas as pd
import math
from matplotlib.ticker import MultipleLocator as ML

rita = True #Sätts till True eller False, avgör om grafen skall ritas eller sparas som en fil

with open('kaffeTeData.json', 'r') as f: 
    inläst_data = json.load(f)  #läser in datan från json-filen till variabeln inläst data

indata_år = inläst_data[0]      #Fördelar indatan årtal, kaffekonsumtion och tekonsumtion till respektive lista 
indata_kaffe = inläst_data[1]
indata_te = inläst_data[2]

fontsize = 16         #skapar en variabel för font storleken så att det enkelt går att ändra
color = 'b'           #Skapar en variabel för färgen på den första grafen

fig, ax1 = plt.subplots() #Plottar den första axeln
l1, = ax1.plot(indata_år, indata_kaffe, color = color, linewidth=2,  label = 'kaffe') #Bestämmer plottens data samt utseende

ax1.set_xlabel('år', fontsize=fontsize)         #Bestämmer x-axelns rubrik och utseende
ax1.set_ylabel('kaffe [kg per person och år]', color = color, fontsize=fontsize)    #Bestämmer första y-axelns rubrik och utseende
ax1.xaxis.set_minor_locator(ML(1))      #skapar tick på x-axeln samt bestämmer deras avstånd
ax1.tick_params(axis= 'x', labelsize = 11, rotation = 20) #Bestämmer tick utseende på x-axeln
ax1.tick_params(axis='y', labelsize = 11)   #Bestämmer tick utseende på första y-axeln
ax1.set_facecolor('bisque') #Bestämmer bakgrundsfärg
plt.grid()    #Skapar rutnät till bakgrunden
plt.ylim([
  math.floor(min(indata_kaffe)), #Avrundar det minsta värdet i listan indata_kaffe och sätter det sedan som första y-axelns undre gränsvärde
  math.ceil(max(indata_kaffe))]) #Avrundar det största värdet i listan indata_kaffe och sätter det sedan som första y-axelns övre gränsvärde

ax2 = ax1.twinx()  # skapar en andra y-axeln som delar samma x-axel

color = 'r'   #Skapar en variabel för färgen på den andra grafen

l2, = ax2.plot(indata_år, indata_te, color = color, ls=":", linewidth=2, label = 'te')    #Skapa andra y-axeln till höger
ax2.set_ylabel('te [kg per person och år]', color = color, fontsize=fontsize)   #Bestämmer första y-axelns rubrik och utseende
ax2.tick_params(axis='y', labelsize = 11)   #Bestämmer tick utseende på andra y-axeln
plt.ylim([
((math.floor((min(indata_te)*100)/10) *10)/100),    
((math.ceil((max(indata_te)*100)/10) *10)/100)])  
  #det minsta/största värdet i indata_te multipliceras med 100 så att floor/ceil kan användas 
  #det nya värdet avrundas till närmsta 10-tal och divideras sedan med hundra igen
  #de slutliga värdena används som andra y-axelns undre och övre gränsvärde

år1 = indata_år[0]                  
år2 = indata_år[len(indata_år)-1]
  #Skapar en variabel för första respektive sista värdet i år-listan   

plt.title(f'konsumtion av kaffe och te i sverige {år1}-{år2} ') #årtalen i titeln är beroende på första och sista värdet i listan år

plt.xlim([
  math.floor(år1/ 10) * 10, 
  math.ceil(år2/ 10) * 10])
    #avrundar det minsta/största värdet i indata_år till närmaste tiotal

plt.tight_layout()  #Fixar så att andra y-axeln inte clipper plottens kanter
plt.legend(handles = [l1, l2], loc = 'lower right', fontsize = 14)  
    #skapar och bestämmer vart legenden ska vara samt hur den ska se ut 

if rita:    #om rita är sant visas grafen
  plt.show()
else:       #om rita är falskt visas ej grafen utan sparas istället som en fil
  plt.savefig('fig_inl2.png')

print(f'Ackumulerad kaffekonsumtion \n\
[kg/person sedan {år1}]\n\
===========================')

årList = []
kgList = []
kg = 0
räknare=0
while räknare < len(indata_år):   #Loop som kommer att repeteras lika många gånger som det finns värden i indata_år

  if str(indata_år[räknare]).endswith('9') == True:   #om årtalet slutar på en 9a initieras if-satsen

    kg = kg + indata_kaffe[räknare]   #variabel som adderar föregående värde av indata_kaffe det nästa
    årList.append(indata_år[räknare]) #Adderar de årtal som slutar på 9 i en lista
    kgList.append(kg)   #Lägger till nuvarande summan av kg i en lista

  else:
    kg = kg + indata_kaffe[räknare] #variabel som adderar föregående värde av indata_kaffe det nästa

  räknare = räknare + 1
  
s = pd.Series(kgList, index=årList) #Skapar en serie av kgList och årList

print(s.to_string()) #Skriver ut serien som en string så det blir fint :)
print('===========================')