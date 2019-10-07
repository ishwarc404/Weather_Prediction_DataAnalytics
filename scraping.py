# imported the requests library
import requests
import pandas as pd
import datetime

irenebuoy = ["42060"] #,"41043", "41046", "41004", "41013", "41025", "44014", "44009", "44025", "44020"]  # bouynumber array
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


