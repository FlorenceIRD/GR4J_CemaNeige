import csv
import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv('ET.csv', header=0)
evap = data['E'].tolist()
evap2 = [evap[i+1]-evap[i] for i in range(len(evap)-1)]
evap2 = [evap[0]] + evap2
with open('C:/Users/Florence/Documents/IRD/VIA/6_Code/GR4JCemaneige_light/GR4JCemaneigeLight/ET2.csv', 'w',
          newline='') as csvfile:
    filewriter = csv.writer(csvfile, delimiter=';')
    filewriter.writerow(['E'])
    for x in evap2:
        filewriter.writerow([x])
data2= pd.read_csv('Debits_BV1.csv', header = 0, sep = '\t')
DatesR = data2['Date'].tolist()


plt.plot(DatesR, evap2)
plt.show()



# with open('C:/Users/Florence/Documents/IRD/VIA/6_Code/GR4JCemaneige_light/GR4JCemaneigeLight/ET2.csv', 'w',
#           newline='') as csvfile:
#     filewriter = csv.writer(csvfile, delimiter=';')
#     filewriter.writerow(['E'])
#     filewriter.writerow(['E'])
#     for x in b:
#         filewriter.writerow(x)
# print(0)