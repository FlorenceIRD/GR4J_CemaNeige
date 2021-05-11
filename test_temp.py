import csv
import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv('temp.csv', header=0)
temp = data['T'].tolist()
temp2 = [temp[i+1]-temp[i] for i in range(len(temp)-1)]
temp2 = [temp[0]] + temp2

with open('/home/florence/Documents/6_Code/GR4JCemaneigeLight/temp2.csv', 'w',
          newline='') as csvfile:
    filewriter = csv.writer(csvfile, delimiter=';')
    filewriter.writerow(['T'])
    for x in temp2:
        filewriter.writerow([x])
data2= pd.read_csv('Debits_BV1.csv', header = 0, sep = '\t')
DatesR = data2['Date'].tolist()
#
#
plt.plot(DatesR, temp2)
plt.show()

