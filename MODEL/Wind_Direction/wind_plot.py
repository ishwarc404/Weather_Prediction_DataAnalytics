import pandas as pd
import matplotlib as plt
import matplotlib.pyplot as plt
from datetime import datetime

df = pd.read_csv("44065_clean.csv")

print(df.columns)
print(df['WindDir'])

import numpy as np

X = [] 
for i in df['datetime'][5600:5900]:
    X.append(datetime.strptime(i,"%Y-%m-%d %H:%M:%S"))

Y = df['WindDir'][5600:5900]



fig, ax = plt.subplots()

x_direct = 1
y_direct = 1

windspeed = df.windspeed[5600:5900]
ax.quiver(X,Y,x_direct,y_direct,angles=(360-Y+90))
plt.xticks(rotation=90)
plt.show()
