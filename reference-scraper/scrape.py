from io import StringIO
from time import sleep
import pymongo
import pandas as pd
import undetected_chromedriver as uc
import re
from flask import jsonify
from datetime import datetime


def testscrape():
    return("test true")

def connecttoDB(df,category):
    client = pymongo.MongoClient('mongodb://localhost:27017/')
    db = client['TechScoutRelational']
    if(category=='cpu'):
        collection = db['CPU']
    if(category=='video-card'):
        collection = db['VideoCard']
    if(category=='memory'):
        collection = db['Memory']
    if(category=='motherboard'):
        collection = db['Motherboard']
    if(category=='monitor'):
        collection = db['Monitor']
    if(category=='keyboard'):
        collection = db['Keyboard']
    data_dict = df.to_dict('records')
    collection.insert_many(data_dict)
    
def scrape_setup():
    print("scrape_setup")
    chrome_options = uc.ChromeOptions()
    prefs = {"profile.managed_default_content_settings.images": 2}
    chrome_options.add_experimental_option("prefs", prefs)
    chrome_driver = uc.Chrome(headless=True, options=chrome_options)
    return chrome_driver

def clean_column(column, patterns):
    for pattern in patterns:
        column = column.str.replace(pattern, '', regex=True)
    return column

def process(df):
    df.columns = df.columns.str.strip()
    df['Name'] = df['Name'].str.replace(r'\s*\(.*?\)', '', regex=True)
    if 'Core Count' in df.columns:
        df['Core Count'] = clean_column(df['Core Count'], ['Core Count'])
        df['Core Count'] = df['Core Count'].apply(lambda x: int(re.sub(r'[^\d]', '', str(x))) if re.sub(r'[^\d]', '', str(x)) else None)
    if 'Performance Core Clock' in df.columns:
        df['Performance Core Clock'] = df['Performance Core Clock'].apply(lambda x: int(re.sub(r'[^\d]', '', str(x))) if re.sub(r'[^\d]', '', str(x)) else None)
    if 'Performance Core Boost Clock' in df.columns:
        df['Performance Core Boost Clock'] = df['Performance Core Boost Clock'].apply(lambda x: int(re.sub(r'[^\d]', '', str(x))) if re.sub(r'[^\d]', '', str(x)) else None)
    if 'Integrated Graphics' in df.columns:
        df['Integrated Graphics'] = clean_column(df['Integrated Graphics'], ['Integrated Graphics'])
    if 'SMT' in df.columns:
        df['SMT'] = clean_column(df['SMT'], ['SMT'])
        df['SMT'] = df['SMT'].apply(lambda x: True if str(x).strip().lower() == 'yes' else False)
    if 'TDP' in df.columns:
        df['TDP'] = clean_column(df['TDP'], ['TDP'])
        df['TDP'] = df['TDP'].apply(lambda x: int(re.sub(r'[^\d]', '', str(x))) if re.sub(r'[^\d]', '', str(x)) else None)
    if 'Price' in df.columns:
        df['Price'] = df['Price'].apply(lambda x: float(re.sub(r'[^\d]', '', str(x))) if re.sub(r'[^\d]', '', str(x)) else None)
        df = df.rename(columns={'Price': 'Price/USD'})
    if 'Rating' in df.columns:
        df['Rating'] = df['Rating'].apply(lambda x: int(re.sub(r'[^\d]', '', str(x))) if re.sub(r'[^\d]', '', str(x)) else None)
    if 'Chipset' in df.columns:
        df['Chipset'] = clean_column(df['Chipset'], ['Chipset'])
    if 'Memory' in df.columns:
        df['Memory'] = clean_column(df['Memory'], ['Memory'])
        df['Memory'] = df['Memory'].apply(lambda x: int(re.sub(r'[^\d]', '', str(x))) if re.sub(r'[^\d]', '', str(x)) else None)
    if 'Core Clock' in df.columns:
        df['Core Clock'] = clean_column(df['Core Clock'], ['Core Clock'])
        df['Core Clock'] = df['Core Clock'].apply(lambda x: int(re.sub(r'[^\d]', '', str(x))) if re.sub(r'[^\d]', '', str(x)) else None)
    if 'Boost Clock' in df.columns:
        df['Boost Clock'] = clean_column(df['Boost Clock'], ['Boost Clock'])
        df['Boost Clock'] = df['Boost Clock'].apply(lambda x: int(re.sub(r'[^\d]', '', str(x))) if re.sub(r'[^\d]', '', str(x)) else None)
    if 'Color' in df.columns:
        df['Color'] = clean_column(df['Color'], ['Color'])
    if 'Length' in df.columns:
        df['Length'] = clean_column(df['Length'], ['Length'])
        df['Length'] = df['Length'].apply(lambda x: int(re.sub(r'[^\d]', '', str(x))) if re.sub(r'[^\d]', '', str(x)) else None)
    if 'Speed' in df.columns:
        df['Speed'] = clean_column(df['Speed'], ['Speed'])
    if 'Modules' in df.columns:
        df['Modules'] = clean_column(df['Modules'], ['Modules'])
    if 'Price/GB' in df.columns:
        df['Price/GB'] = clean_column(df['Price/GB'], ['Price/GB'])
        df['Price/GB'] = df['Price/GB'].apply(lambda x: float(re.sub(r'[^\d]', '', str(x))) if re.sub(r'[^\d]', '', str(x)) else None)
    if 'First Word Latency' in df.columns:
        df['First Word Latency'] = clean_column(df['First Word Latency'], ['First Word Latency'])
        df['First Word Latency'] = df['First Word Latency'].apply(lambda x: float(re.sub(r'[^\d]', '', str(x))) if re.sub(r'[^\d]', '', str(x)) else None)
    if 'CAS Latency' in df.columns:
        df['CAS Latency'] = clean_column(df['CAS Latency'], ['CAS Latency'])
        df['CAS Latency'] = df['CAS Latency'].apply(lambda x: int(re.sub(r'[^\d]', '', str(x))) if re.sub(r'[^\d]', '', str(x)) else None)
    if 'Socket / CPU' in df.columns:
        df['Socket / CPU'] = clean_column(df['Socket / CPU'], ['Socket / CPU'])
    if 'Form Factor' in df.columns:
        df['Form Factor'] = clean_column(df['Form Factor'], ['Form Factor'])
    if 'Memory Max' in df.columns:
        df['Memory Max'] = clean_column(df['Memory Max'], ['Memory Max'])
        df['Memory Max'] = df['Memory Max'].apply(lambda x: int(re.sub(r'[^\d]', '', str(x))) if re.sub(r'[^\d]', '', str(x)) else None)
    if 'Memory Slots' in df.columns:
        df['Memory Slots'] = clean_column(df['Memory Slots'], ['Memory Slots'])
        df['Memory Slots'] = df['Memory Slots'].apply(lambda x: int(re.sub(r'[^\d]', '', str(x))) if re.sub(r'[^\d]', '', str(x)) else None)
    if 'Screen Size' in df.columns:
        df['Screen Size'] = clean_column(df['Screen Size'], ['Screen Size'])
        df['Screen Size'] = df['Screen Size'].apply(lambda x: float(re.sub(r'[^\d]', '', str(x))) if re.sub(r'[^\d]', '', str(x)) else None)
    if 'Resolution' in df.columns:
        df['Resolution'] = clean_column(df['Resolution'], ['Resolution'])
    if 'Refresh Rate' in df.columns:
        df['Refresh Rate'] = clean_column(df['Refresh Rate'], ['Refresh Rate'])  
        df['Refresh Rate'] = df['Refresh Rate'].apply(lambda x: float(re.sub(r'[^\d]', '', str(x))) if re.sub(r'[^\d]', '', str(x)) else None)
    if 'Response Time (G2G)' in df.columns:
        df['Response Time (G2G)'] = clean_column(df['Response Time (G2G)'], ['Response Time (G2G)'])
        df['Response Time (G2G)'] = df['Response Time (G2G)'].apply(lambda x: float(re.sub(r'[^\d]', '', str(x))) if re.sub(r'[^\d]', '', str(x)) else None)
    if 'Panel Type' in df.columns:
        df['Panel Type'] = clean_column(df['Panel Type'], ['Panel Type'])
    if 'Aspect Ratio' in df.columns:
        df['Aspect Ratio'] = clean_column(df['Aspect Ratio'], ['Aspect Ratio'])
    if 'Style' in df.columns:
        df['Style'] = clean_column(df['Style'], ['Style'])
    if 'Switch Type' in df.columns:
        df['Switch Type'] = clean_column(df['Switch Type'], ['Switch Type'])
    if 'Backlit' in df.columns:
        df['Backlit'] = clean_column(df['Backlit'], ['Backlit'])
    if 'Tenkeyless' in df.columns:
        df['Tenkeyless'] = clean_column(df['Tenkeyless'], ['Tenkeyless'])
        df['Tenkeyless'] = df['Tenkeyless'].apply(lambda x: True if str(x).strip().lower() == 'Yes' else False)
    if 'Connection Type' in df.columns:
        df['Connection Type'] = clean_column(df['Connection Type'], ['Connection Type'])
    
    df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
    return df


def scrape(category, driver):
    dfs = []
    for i in range(1,3):
        driver.get(f"https://pcpartpicker.com/products/{category}/#page={i}")
        sleep(2)
        df = pd.read_html(StringIO(driver.page_source))
        dfs.append(df[0])
    df = pd.concat(dfs)
    df['Scrape Timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"column names:{df.columns}")
    if 'Unnamed: 0' in df.columns:
        df = df.drop(columns=['Unnamed: 0'])
    cleaned_df=process(df)
    connecttoDB(cleaned_df,category)
    return cleaned_df

def scrape_all():
    categories = ["cpu", "video-card", "memory", "motherboard", "monitor", "keyboard"]
    chrome_driver=scrape_setup()
    for category in categories:
        scrape(category, chrome_driver)
