import bs4 as BeautifulSoup
import requests
import datetime as dt 
import re
import random
import argparse
import pandas as pd


def get_flights(airport='tunis'):
    dics=[]
    m = dt.datetime.today().month
    y = dt.datetime.today().year
    x = dt.datetime.today().day

    registered=0

    url = f"http://oaca.nat.tn/newapp/hvdynt/resultatsvolsfrcall2.php?startRow=1&frmmvtCod=D&frmaeropVil=-1&frmnumVol=&frmairport={airport}&frmhour=10&frmday={x}&frmmonth={m}&frmadjust=-1&frmacty={y}"
    req = requests.get(url)
    soup = BeautifulSoup.BeautifulSoup(req.text) 
    trs = soup.findAll("tr" , attrs={"align": u"center"})
    trs=trs[1:]
    for tr in trs:
        tds=tr.findAll("td")
        company = tds[2].text
        dest=tds[0].text
        time=tds[1].text
        hr=int(time[0:time.find(':',0)])
        mi=int(time[time.find(':',0)+1:])
        date=dt.datetime(year=y, month=m, day=x, hour=hr, minute=mi)
        timestampStr = date.strftime("%Y-%m-%d %H:%M:%S.%f")
        comment=tds[4].text
        delay=0
        regex=re.compile("^DECOLLE")
        actualTime = ""
        if (regex.match(comment)):
            
            #time=comment[comment.find(" ",0)+1:]
            hour=int(comment[comment.find(" ",0)+1:comment.find(" ",0)+3])
            minute=int(comment[comment.find(":",0)+1:])
            time=dt.datetime(year=y, month=m, day=x, hour=hour, minute=minute)
            actualTime=time.strftime("%Y-%m-%d %H:%M:%S.%f")
            delay=(time-date).total_seconds()/60
            comment="DECOLLE"

        dics.append({"dest":dest,"plannedTime": str(timestampStr),"actualTime": str(actualTime),"airline":company, "flightId":tds[3].text,"status":comment,"delay":delay})
    return dics

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Get Today's Flights in Tunisia's airports and computes delays")
    parser.add_argument('--out', help='Output file', default='oaca.csv')
    parser.add_argument('--airport', help='Arrival airport', default='tunis')
    args = parser.parse_args()
    df = pd.DataFrame(get_flights(airport=args.airport))
    print(df)
    if args.out:
        df.to_csv(args.out)
