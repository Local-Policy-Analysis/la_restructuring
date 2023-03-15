import pandas as pd

def restructure(df, from_year, to_year):
    '''
    Function to change the local authority structure from a given start point to a new year's structure. Will replace old
    authority names, la class, ons code and ecode to new structure
    
    df: dataframe to be restructured
    from_year: integer representing the financial year of the starting LA structure. Note financial year 2022-23 would be 2022. 
    Must be smaller than to_year.
    to_year: integer representing the financial year of the desired LA structure. Must be larger than from_year.
    
    returns: dataframe post restructuring with ecode, ons_code overwritten and class and authority columns merged
    
    requisites: import pandas as pd
    '''
    assert to_year > from_year, 'to_year is less than from_year'
    url = 'https://github.com/JamesCaddick/la_strucuture_lookup/blob/main/la_structure.xlsx?raw=true'
    df_lookup = pd.read_excel(url)
    dict_ons = pd.Series(df_lookup[f'ons_code_{to_year}'].values, index=df_lookup[f'ons_code_{from_year}']).to_dict()
    dict_ecode = pd.Series(df_lookup[f'ecode_{to_year}'].values, index=df_lookup[f'ecode_{from_year}']).to_dict()
    df = (df
          .replace(dict_ons).replace(dict_ecode)
          .merge(df_lookup[[f'class_{to_year}', f'ons_code_{to_year}', f'authority_{to_year}']], left_on='ons_code', right_on=f'ons_code_{to_year}', how='left')
          .drop(columns=f'ons_code_{to_year}'))
    return df

df = pd.read_excel('to_restructure.xlsx')
df = restructure(df, 2013, 2023)