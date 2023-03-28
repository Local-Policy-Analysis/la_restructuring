import pandas as pd

def restructure(df, from_year, to_year):
    '''
    Function to change the local authority structure from a given start point to a new year's structure. Appends new columns containing the
    post restructuring ons codes, ecodes, authority and class variables. File being restructured must contain a column of ons codes with 
    the variable name "ons_code"
    
    df: dataframe to be restructured
    from_year: integer representing the financial year of the starting LA structure. Note financial year 2022-23 would be 2022. 
    Must be smaller than to_year.
    to_year: integer representing the financial year of the desired LA structure. Must be larger than from_year.
    
    returns: dataframe post restructuring
    
    requisites: import pandas as pd
    # to do: LA names were taken from ONS code history database but there are duplicate names since for e.g. Essex refers to the SC and the FRA
    '''
    assert to_year > from_year, 'to_year is less than from_year'
    df_lookup = pd.read_table("./bin/la_structure.tsv")
    df = (df[['ons_code']]
          .merge(df_lookup[[f'ons_code_{from_year}', f'ecode_{from_year}',f'authority_{from_year}',f'class_{from_year}',f'ons_code_{to_year}',f'ecode_{to_year}',f'authority_{to_year}',f'class_{to_year}']]
                 .drop_duplicates(),
                 left_on='ons_code',
                 right_on=f'ons_code_{from_year}',
                 how='left')
          ).drop(columns = f'ons_code_{from_year}')
    return df

df = pd.read_excel('./to_restructure.xlsx', index=False)
df = restructure(df, 2013, 2023)

df.to_csv("testp.csv")