import json 
import pandas as pd
import numpy as np
from scrapers import get_fantasypros_projections

def load_league_settings(league_name: str) -> dict:
    filename = league_name + ".json"
    with open(filename) as f:
        league_settings = json.load(f)
        return league_settings

def calculate_fpts(league_settings: dict, df: pd.DataFrame) -> list:
    league_scoring = league_settings['scoring']
    df = df.replace(np.nan, 0)
    result = []
    for i,row in df.iterrows():
        fpts = 0
        for colname, value in zip(row.index, row):
            if colname in league_scoring.keys():
                fpts += round(value * league_scoring[colname], 1)
        result.append(fpts)
    return result

def calculate_vorp(league_settings: dict, df: pd.DataFrame) -> list:
    # TODO: need to change VORP value for TE and QB...
    # QB should maybe be like 15
    

    league_roster_settings = league_settings['roster']
    positions = ['qb', 'rb', 'wr', 'te']
    result = pd.DataFrame()
    for pos in positions:
        df_pos = df[df['position'] == pos].sort_values(by='fpts_new', ascending=False).reset_index(drop=True)
        # Number of teams * number of players at position + half number of teams
        # We want the average (6th best) first man up on the bench
        vorp_idx = league_roster_settings.get('teams') * league_roster_settings.get(pos) + 0.5*league_roster_settings.get('teams')
        replacement_pts = df_pos.loc[vorp_idx, 'fpts_new']
        print(f"VORP for {pos}: {vorp_idx}. Replacement points: {replacement_pts}")
        vorps = [df_pos.loc[i, 'fpts_new'] - replacement_pts for i in df_pos.index]
        df_pos.insert(1, 'vorp', vorps)
        print(df_pos.head(20))

        if result.empty:
            result = df_pos 
        else:
            result = pd.concat([result, df_pos])
    result = result.sort_values(by='vorp', ascending=False).reset_index()
    result.insert(3, 'rank', [x+1 for x in result.index])
    result.insert(4, 'posrank', [x+1 for x in result['index']])
    result = result.drop('index', axis=1)

    return result


def main():
    league_names = ['baltimore_showdown', 'jamie_league', 'league_of_leagues', 'pecker_league']
    raw_data = get_fantasypros_projections()
    for name in league_names:
        print(f"**********{name}**********")
        df = raw_data.copy()
        league_settings = load_league_settings(name)
        # Calculate fantasy points for league
        df.insert(2, 'fpts_new', calculate_fpts(league_settings, df))
        # Calculate value over replacement player (VORP)
        df = calculate_vorp(league_settings, df)
        print(f"Overall VORP draft order for {name}:\n {df.head(30)}")
        df.to_csv(name + "_vorp.csv")

if __name__ == "__main__":
    main()