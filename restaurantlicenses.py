import urllib.request
import json, csv, datetime
import xml.etree.ElementTree as ET

def getApiOutput(url):
    with urllib.request.urlopen(url) as response:
        output = response.read().decode('utf8')
    return output

def parseXMLfromAPI(apiOutput:str):
    root = ET.fromstring(apiOutput)
    lps = root.find("LPS")
    for lp in lps:
        print(lp)

def timestampExists(ts, countList:list):
    for count in countList:
        if "timestamp" in count and ts == count["timestamp"]:
            return True
    return False

def main():
    startDate = datetime.date(2018,1,1)
    endDate = datetime.date.today() - datetime.timedelta(days=1)
    url = "https://api.data.gov.hk/v1/historical-archive/list-file-versions?url=https%3A%2F%2Fwww.fehd.gov.hk%2Fenglish%2Flicensing%2Flicense%2Ftext%2FLP_Restaurants_EN.XML&start="
    url += startDate.strftime('%Y%m%d')
    url += "&end="
    url += endDate.strftime('%Y%m%d')

    print(f"Getting file timestamps...")
    #print(url)
    output = getApiOutput(url)
    timestamps = json.loads(output)["timestamps"]
    print(f"Got {len(timestamps)} record(s).")
    print("")

    print(f"Reading from CSV file ...")
    countList = []
    try:
        with open('restaurantlicenses.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                countList.append(row)
            print(f"Read {len(countList)} row(s) from CSV file.")
    except:
        print(f"No CSV file.")
    print("")

    print(f"Getting Restaurant License API data ...")
    counter = 0
    for ts in timestamps:
        if counter > 3:
            break
        if timestampExists(ts, countList):
            print(f"Timestamp {ts} exists, skipping.")
            continue
        counter += 1

    url = "https://api.data.gov.hk/v1/historical-archive/get-file?url=https%3A%2F%2Fwww.fehd.gov.hk%2Fenglish%2Flicensing%2Flicense%2Ftext%2FLP_Restaurants_EN.XML&time="
    url += "ts"

if __name__ == "__main__":
    main()
