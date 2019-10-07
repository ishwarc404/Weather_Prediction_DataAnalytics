# imported the requests library
import requests
import pandas as pd
import datetime

#comment some of the numbers here out for faster processing
irenebuoy = ["42060","41043", "41046", "41004", "41013", "41025", "44014", "44009", "44025", "44020"]  # bouynumber array
year = "2011"  # year


#stations contains the details about every station
testdf = pd.read_csv("stations.csv")
stationdic = {}


for index, row in testdf.iterrows():
    ID = testdf.loc[index, 'ID']
    if ID in irenebuoy:
        if ID not in stationdic.keys():
            stationdic[ID] = [testdf.loc[index, 'Lat'],
                              testdf.loc[index, 'Lon']]
            stationdic[ID][1] = stationdic[ID][1].replace('\u00ad', '-')
            stationdic[ID][0] = stationdic[ID][0].replace('\u00ad', '-')

print(stationdic)

#here we are scraping using requests
for i in irenebuoy:
    text_url = "https://www.ndbc.noaa.gov/view_text_file.php?filename=" + \
        i + "h" + year + ".txt.gz&dir=data/historical/stdmet/"

    r = requests.get(text_url)  # create HTTP response object

    # send a HTTP request to the server and save
    # the HTTP response in a response object called r

    with open(i + ".txt", 'wb') as f:

        # Saving received content as a text file in
        # binary format
        # write the contents of the response (r.content)
        # to a new file in binary mode.
        f.write(r.content)


#declaring a new dataframe to store all the accumulated data
maindf = pd.DataFrame()

windspeedfinal = []
pressurefinal = []
yearfinal = []
monthfinal = []
dayfinal = []
hourfinal = []
minsfinal = []
waveheightfinal = []
waveperiodfinal = []
wavedirectionfinal = []
latfinal = []
winddirfinal = []
lonfinal = []
idlistfinal = []
for i in irenebuoy:

    f = open(i + '.txt', 'r')

    windspeed = []
    winddir = []
    pressure = []
    year = []
    month = []
    day = []
    hour = []
    mins = []
    waveheight = []
    waveperiod = []
    wavedirection = []
    lat = []
    lon = []
    idlist = []
    for line in f: #reading each field 
        winddir.append(line[17:21])
        windspeed.append(line[21:25])
        pressure.append(line[53:59])
        year.append(line[0:5])
        month.append(line[5:8])
        day.append(line[8:11])
        hour.append(line[11:14])
        mins.append(line[14:17])
        waveheight.append(line[32:36])
        waveperiod.append(line[44:48])
        wavedirection.append(line[49:52])
        lat.append(stationdic[i][0])
        lon.append(stationdic[i][1])
        idlist.append(i)
    
    #accumulating data from every
    winddirfinal = winddirfinal + winddir[2:]
    windspeedfinal = windspeedfinal + windspeed[2:]
    pressurefinal = pressurefinal + pressure[2:]
    yearfinal = yearfinal + year[2:]
    monthfinal = monthfinal + month[2:]
    dayfinal = dayfinal + day[2:]
    hourfinal = hourfinal + hour[2:]
    minsfinal = minsfinal + mins[2:]
    waveheightfinal = waveheightfinal + waveheight[2:]
    waveperiodfinal = waveperiodfinal + waveperiod[2:]
    wavedirectionfinal = wavedirectionfinal + wavedirection[2:]
    latfinal = latfinal + lat[2:]
    lonfinal = lonfinal + lon[2:]
    idlistfinal = idlistfinal + idlist[2:]
    #pressurefinal = pressurefinal  + pressure[2:]



maindf['ID'] = idlistfinal
maindf['year'] = yearfinal
maindf['month'] = monthfinal
maindf['day'] = dayfinal
maindf['hour'] = hourfinal
maindf['mins'] = minsfinal
maindf['waveperiod'] = waveperiodfinal
maindf['wavedirection'] = wavedirectionfinal
maindf['waveheight'] = waveheightfinal
maindf['Lat'] = latfinal
maindf['Lon'] = lonfinal
maindf['WindDir'] = winddirfinal


# from 2 to the end so as to ignore the title lables
maindf['windspeed'] = windspeedfinal
maindf['pressure'] = pressurefinal

# CONVERTING TO NUMERIC

for i in maindf.columns:
    maindf[i] = pd.to_numeric(maindf[i], downcast='float', errors='coerse')
"""maindf['ID'] =  pd.to_numeric(maindf['ID'],downcast = 'float',errors = 'coerse');
maindf['pressure'] =  pd.to_numeric(maindf['pressure'],downcast = 'float',errors = 'coerse');
maindf['windspeed'] =  pd.to_numeric(maindf['windspeed'],downcast = 'float',errors = 'coerse');
maindf['waveperiod'] =  pd.to_numeric(maindf['waveperiod'],errors = 'coerse',downcast = 'float');
maindf['wavedirection'] =  pd.to_numeric(maindf['wavedirection'],errors = 'coerse',downcast = 'float');
maindf['Lat'] =  pd.to_numeric(maindf['Lat'],downcast = 'float',errors = 'coerse');
maindf['Lon'] =  pd.to_numeric(maindf['Lon'],errors = 'coerse',downcast = 'float');"""
l = []

#encoding wind direction
for i in maindf['WindDir']:

    if i in range(35, 70):
        l.append('NE')

    elif i in range(70, 115):
        l.append('E')

    elif i in range(115, 155):
        l.append('SE')
    elif i in range(155, 200):
        l.append('S')
    elif i in range(200, 245):
        l.append('SW')
    elif i in range(245, 300):
        l.append('W')
    elif i in range(300, 345):
        l.append('NW')
    else:
        l.append('N')
maindf['WindDir_L'] = l

"""for index,rows in maindf.iterrows():
    if maindf.loc[index,'pressure'] < 1005 :
        maindf.loc[index,"possibility"] = 1 
    else:
        maindf.loc[index,"possibility"] = 0 
"""


# MAKING A NEW COLUMN CALLED DATE AND TIME. THIS WILL BE USED FOR LABELLING

for index, rows in maindf.iterrows():
    maindf.loc[index, 'datetime'] = datetime.datetime(
        maindf.loc[index, 'year'], maindf.loc[index,'month'], maindf.loc[index, 'day'],
        maindf.loc[index, 'hour'], maindf.loc[index, 'mins'], 0)

maindf = maindf.sort_values(['datetime'])
maindf['hurrthreat'] = 0
for index, rows in maindf.iterrows():
    i = maindf.loc[index, 'datetime']
    if ((i.day > 1) and (i.day < 29) and (i.month == 8)):
        maindf.loc[index, 'hurrthreat'] = 1
maindf['DaysTH'] = 0
j = datetime.datetime(2011,8,29)
for index , row in maindf.iterrows():
    i = maindf.loc[index,'datetime']
    diff  =j-i
    maindf.loc[index,'DaysTH'] = diff.days




maindf.to_csv("IRENECSV.csv")
#final CSV with the data
