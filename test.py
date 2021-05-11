import csv
import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv('Precip.csv', header=0)
pluie = data['P'].tolist()
pluie2 = [pluie[i+1]-pluie[i] for i in range(len(pluie)-1)]
pluie2 = [pluie[0]] + pluie2
with open('C:/Users/Florence/Documents/IRD/VIA/6_Code/GR4JCemaneige_light/GR4JCemaneigeLight/Precip2.csv', 'w',
          newline='') as csvfile:
    filewriter = csv.writer(csvfile, delimiter=';')
    filewriter.writerow(['P'])
    for x in pluie2:
        filewriter.writerow([x])
# data2= pd.read_csv('Debits_BV1.csv', header = 0, sep = '\t')
# DatesR = data2['Date'].tolist()
#
#
# plt.plot(DatesR, pluie2)
# plt.show()



# with open('C:/Users/Florence/Documents/IRD/VIA/6_Code/GR4JCemaneige_light/GR4JCemaneigeLight/Precip2.csv', 'w',
#           newline='') as csvfile:
#     filewriter = csv.writer(csvfile, delimiter=';')
#     filewriter.writerow(['P'])
#     filewriter.writerow(['P'])
#     for x in b:
#         filewriter.writerow(x)
# print(0)