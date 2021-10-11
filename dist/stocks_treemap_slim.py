import pandas as _pd
import numpy as _np

def run(input_df):
    input_df = input_df[['Company','Symbol','Symbol_Yahoo','Description','MarketCap','MarketCap_USD','Currency','Country','Industries']]
    input_df.columns = ['Company','Symbol','Yahoo Symbol','Description','Market Cap','Market Cap (USD)','Currency','Country','Industries']
    industries = _np.unique(', '.join(input_df['Industries']).split(', '))
    
    industries_to_plot = []

    for industry in industries:
        industry_df = input_df[input_df['Industries'].str.contains(industry)].copy()
        industries_to_plot.append((industry,industry_df,len(industry_df)))

    industries_to_plot = sorted(industries_to_plot, key=lambda x: x[2], reverse=True)

    map_df = _pd.DataFrame(columns=['Yahoo Symbol','Industry'])

    for industry_to_plot in industries_to_plot:
        valid = True    

        for industry_to_compare in industries_to_plot:
            if (industry_to_plot[1] is industry_to_compare[1]):
                continue

            valid = not all(elem in list(industry_to_compare[1]['Yahoo Symbol']) for elem in list(industry_to_plot[1]['Yahoo Symbol']))
            
            if(not valid):
                break

        if(valid):
            industry_to_plot[1]['Industry'] = industry_to_plot[0]
            map_df = map_df.append(industry_to_plot[1][['Yahoo Symbol','Industry']], ignore_index=True)

    map_df = map_df[~map_df['Yahoo Symbol'].duplicated(keep='last')]
    map_df = map_df.join(input_df[['Company','Symbol','Yahoo Symbol','Description','Country','Currency','Market Cap','Market Cap (USD)']].set_index('Yahoo Symbol'), on='Yahoo Symbol')
    map_df = map_df.sort_values(['Country', 'Market Cap (USD)'], ascending=[False, False])
    map_df = map_df[['Industry','Company','Symbol','Yahoo Symbol','Description','Country','Currency','Market Cap','Market Cap (USD)']]

    return map_df.reset_index(drop=True)