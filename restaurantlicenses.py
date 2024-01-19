import urllib.request
import json, csv, datetime, time, sys
import xml.etree.ElementTree as ET

MAX_ITER = 1

def getApiOutput(url):
    with urllib.request.urlopen(url) as response:
        output = response.read().decode('utf8')
    return output

def parseXMLfromAPI(apiOutput:str):
    count = {
        "Timestamp": "",
        "RL": 0,
        "RR": 0,
        "MR": 0,
    }
    root = ET.fromstring(apiOutput)
    lps = root.find("LPS")
    for lp in lps:
        count[lp.find("TYPE").text] += 1
    return count

def timestampExists(ts, countList:list):
    for count in countList:
        if "Timestamp" in count and ts == count["Timestamp"]:
            return True
    return False

def main():
    timestamps = []
    countList = []

    startDate = datetime.date(2021,1,1)
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
    try:
        with open('restaurantlicenses.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if timestampExists(row["Timestamp"], countList):
                    continue
                countList.append(row)
            print(f"Read {len(countList)} row(s) from CSV file.")
    except:
        print(f"No CSV file.")
    print("")

    print(f"Getting Restaurant License API data ...")
    counter = 0
    skipped = 0
    for ts in timestamps:
        if timestampExists(ts, countList):
            skipped += 1
            # print(f"Timestamp {ts} exists, skipping.")
            continue
        if counter > MAX_ITER:
            break
        else:
            time.sleep(1)
        # print(f"Retrieving data for {datetime.datetime.strptime(ts, '%Y%m%d-%H%M')}.")
        sys.stdout.write(f".")
        sys.stdout.flush()
        url = "https://api.data.gov.hk/v1/historical-archive/get-file?url=https%3A%2F%2Fwww.fehd.gov.hk%2Fenglish%2Flicensing%2Flicense%2Ftext%2FLP_Restaurants_EN.XML&time="
        url += ts
        output = getApiOutput(url)
        count = parseXMLfromAPI(output)
        count["Timestamp"] = ts
        countList.append(count)
        counter += 1
    print(f"\nRetrieved {counter} record(s) from API.")
    print("")

    print(f"Writing to CSV File...")
    if "Timestamp" in countList[0]:
        countList = sorted(countList, key=lambda x: x['Timestamp'])
    with open('restaurantlicenses.csv', 'w', newline='') as csvfile:
        fieldnames = count.keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for count in countList:
            writer.writerow(count)
    print(f"Wrote {len(countList)} row(s) to CSV file.")

if __name__ == "__main__":
    start_ts = time.time()
    MAX_ITER = input("How many records do you want to read? ")
    if MAX_ITER == "":
        MAX_ITER = 10
    else:
        MAX_ITER = int(MAX_ITER)
    main()
    print(f"Time elapsed: {round(time.time() - start_ts, 1)} seconds.")
