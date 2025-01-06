import os, urllib.request as urllib2, json, sqlite3
import pandas as pd, datetime, numpy as np, glob
from random import randint
from time import sleep

DATA = "/opt/Downloads/alldata/sp500"

DAY_URL = "https://api.polygon.io/v2/aggs/grouped/locale/us/market/stocks/%s?adjusted=true&apiKey=%s"

# place your Polygon.io key inside a JSON, key is polygon, value is your polygon pass
params = json.loads(open(os.environ['HOME'] + "/.nomterr.conf").read())

def get_spy_tickers():
    link = ("https://en.wikipedia.org/wiki/List_of_S%26P_500_companies#S&P_500_component_stocks")
    df = pd.read_html(link, header=0)[0]
    df.to_csv(DATA + "/spy-tickers.csv", index=False)
    
def get_since_2010():
    tickers_df = pd.read_csv(DATA + "/spy-tickers.csv")
    for val, row in tickers_df.iterrows():
        ticker = row['Symbol']
        fout = DATA + "/2010-2024/%s.csv" % ticker
        if os.path.isfile(fout) == True:
            print ('skipping...', ticker)
            continue
        print ('getting ticker', ticker)
        df = util.get_yahoo_ticker(2010, ticker)
        df.to_csv(fout)
        sleep(randint(2,7))

def get_day(day):
    year = day[0:4]; mon = day[5:7]
    fout = open(DATA + "/%s/%s/%s.csv" % (year, mon, day), "w")
    sp_stocks = pd.read_csv(DATA + "/spy-tickers.csv").Symbol
    sp_stocks = list(sp_stocks)    
    url = DAY_URL % (day,params['polygon'])
    print (url)
    r = urllib2.urlopen(url).read()
    data = json.loads(r)
    for res in data['results']:
        sym = res['T'].replace(".","-")
        if sym not in sp_stocks: continue
        fout.write("%s,%s" % (sym,res['c']))
        fout.write("\n")
        fout.flush()
    fout.close()

def db_conn():
    db_file = DATA + "/sp500.db"
    conn = sqlite3.connect(db_file)    
    return conn
    
def db_create():
    conn = db_conn()
    c = conn.cursor()
    res = c.execute('''DROP TABLE IF EXISTS TICKER; ''')
    res = c.execute('''CREATE TABLE TICKER (dt INTEGER, sym TEXT, c NUMERIC, PRIMARY KEY (dt, sym)); ''')

def db_load_2010():
    conn = db_conn()    
    cursor = conn.cursor()
    dir = "2010-2024"
    for file in glob.glob(DATA + "/" + dir + "/*"):
        print (file)
        df = pd.read_csv(file)
        sym = os.path.basename(file).replace(".csv","")
        for idx,row in df.iterrows():
            dt = int(row['Date'].replace("-",""))
            c = float(row['Adj Close'])
            #print (sym, dt, c)
            cursor.execute('''INSERT INTO TICKER (dt,sym,c) VALUES (?,?,?)''', (dt,sym,c))
        conn.commit()        

def db_load_inc(dir):
    conn = db_conn()    
    cursor = conn.cursor()
    gdir = DATA + "/" + dir + "/**/*.csv"
    for file in glob.glob(gdir,recursive=True):        
        dt = os.path.basename(file).replace(".csv","")
        dt = dt.replace("-","")
        cursor.execute('''DELETE FROM TICKER where dt = ?''', (dt,))
        conn.commit()        
        df = pd.read_csv(file,header=None)
        for idx,row in df.iterrows():
            sym, c = row[0], row[1]
            print (dt,sym,c)
            cursor.execute('''INSERT INTO TICKER (dt,sym,c) VALUES (?,?,?)''', (dt,sym,c))
        conn.commit()        

def get_db_tickers(year, tickers):
    c = db_conn().cursor()
    year = int(str(year) + "0101")
    dfs = []
    for ticker in tickers:
        rows = c.execute("SELECT dt,c from TICKER where sym = ? and dt >= ?", (ticker,year))
        df = pd.DataFrame(rows.fetchall(),columns=['dt',ticker])
        df['dt'] = pd.to_datetime(df['dt'], format='%Y%m%d')
        df = df.set_index('dt')
        dfs.append(df)
    df = pd.concat(dfs,axis=1)
    return df
    
if __name__ == "__main__": 
    #db_create()
    #db_load_2010()
    #db_load_inc("2024/12")
    #get_since_2010()
    get_day("2025-01-03")
    pass
