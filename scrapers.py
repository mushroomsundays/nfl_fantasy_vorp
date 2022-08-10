import pandas as pd 

def get_fantasypros_projections():
    positions = ['qb', 'rb', 'wr', 'te']
    result_df = pd.DataFrame()
    for pos in positions:
        
        # Read table from website
        url = f"https://www.fantasypros.com/nfl/projections/{pos}.php?week=draft"
        df = pd.read_html(url, header=1)[0]

        # Rename columns
        colname_map = {
            'qb': ['player', 'pass_att', 'pass_cmp', 'pass_yds', 'pass_tds', 'ints',
                'rush_att', 'rush_yds', 'rush_tds', 'fl', 'old_fpts'],
            'rb': ['player', 'rush_att', 'rush_yds', 'rush_tds', 'rec', 'rec_yds', 
                'rec_tds', 'fl', 'old_fpts'],
            'wr': ['player', 'rec', 'rec_yds', 'rec_tds', 'rush_att', 'rush_yds',
                'rush_tds', 'fl', 'old_fpts'],
            'te': ['player', 'rec', 'rec_yds', 'rec_tds', 'fl', 'old_fpts']
        }
        df.columns = colname_map[pos]
        df.insert(1, 'position', pos)

        print(f"***{pos}***")
        print(df.head())
        print(df.columns)

        # Outer merge on player to combine dataframes
        if result_df.empty:
            result_df = df 
        else:
            result_df = pd.merge(left=result_df, right=df, how='outer')
                    
    return result_df

def get_4for4_projections():
    positions = ['QB', 'RB', 'WR', 'TE']
    for pos in positions:
        url = f"https://www.4for4.com/full-impact/cheatsheet/{pos}/60444/ff_nflstats_early/adp_blend"
        df = pd.read_html(url)
        print(type(df))
        print(df)
        break
    # TODO: no tables found; need to use beautifulsoup
