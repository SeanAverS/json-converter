import pandas as pd
import json
import os
import sys

def run_conversion():
    # Use custom file path if provided in terminal, otherwise use sample file
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
    else:
        file_path = "data/Scoreboard Test.xlsx"
    
    if not os.path.exists(file_path):
        print(f"Cannot find {file_path}.")
        return

    # start data load from row 2
    df = pd.read_excel(file_path, header=1)

    clean_columns = []
    
    # clean the data 
    for i, col in enumerate(df.columns):
        # change first column header title 
        if i == 0:
            clean_columns.append("date")
            continue
            
        # remove extra spaces from headers
        name = str(col).replace("\n", " ").strip()
        
        # keep blank columns, give generic id 
        if "Unnamed" in name or name == "nan":
            name = f"metric_column_{i}"
            
        clean_columns.append(name)

    # cleaned data  
    df.columns = clean_columns

    # prepare output.json using cleaned data 
    # start from row 8 
    df = df.iloc[5:].reset_index(drop=True)

    # make sure rows start with 'date'
    df = df.dropna(subset=['date'])
    
    # convert 'date' to string  
    df['date'] = df['date'].astype(str)

    output_file = "output.json"
    
    # format export
    # to_json: dealts with NAN 
    # orient: seperate date objects 
    # indent: proper spacing between data 
    df.to_json(output_file, orient='records', indent=4)

    print(f"✅ Success! Processed {len(df.columns)} columns.")
    print(f"📊 {len(df)} rows of data saved to {output_file}")

if __name__ == "__main__":
    run_conversion()