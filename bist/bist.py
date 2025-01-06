import os, urllib.request as urllib2, json, sqlite3
import pandas as pd, datetime, numpy as np, glob, json
from random import randint
from time import sleep

DATA = "/opt/Downloads/alldata/bist/"

def get_since_2010():
    tickers_df = pd.read_csv(DATA + "/bist-tickers.csv")
    for val, row in tickers_df.iterrows():
        ticker = row['Symbol2']
        fout = DATA + "/2010-2024/%s.csv" % ticker
        if os.path.isfile(fout) == True:
            print ('skipping...', ticker)
            continue
        print ('getting ticker', ticker)
        df = util.get_yahoo_ticker2(2010, ticker + ".IS")
        df.index.names = ['Date']
        df.columns = ['Adj Close']
        df.to_csv(fout)
        exit()        

def db_conn():
    db_file = DATA + "/bist100.db"
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
            c = float(row["Adj Close"])
            #print (sym, dt, c)
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

def convert_excel(dt):
    # can load daily updates from this excel https://www.isyatirim.com.tr/en-us/analysis/stocks/Pages/bist-data-table.aspx?endeks=01#page-1
    df = pd.read_excel(os.environ['HOME'] + "/Downloads/temelozet.xlsx")
    df[['Stock','Close (TL)']].to_csv(DATA + "/" + dt + ".csv",header=None,index=None)

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

    
if __name__ == "__main__": 
 
    #db_create()
    #db_load_2010()
    #get_since_2010()
    #convert_excel("2024/12/2024-12-23")
    db_load_inc("2024/12")
    pass
