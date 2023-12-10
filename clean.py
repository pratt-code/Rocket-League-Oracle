from config import use_columns
import get_data
import numpy as np

## Function used to generate list of column names for each replay ##
def parse_json(json, parent_name='', columns=[], row=[]):
    for key in json:
        if type(json[key]) is dict and parent_name != '':
            columns, row = parse_json(json[key], parent_name + '_' + key, columns, row)
        elif type(json[key]) is dict:
            columns, row = parse_json(json[key], key, columns, row)
        elif type(json[key]) is list and parent_name != '':
            for item in json[key]:
                columns, row = parse_json(item, parent_name + '_' + key, columns, row)
        elif type(json[key]) is list:
            for item in json[key]:
                columns, row = parse_json(item, key, columns, row)
        elif(parent_name != ''):
            columns.append(parent_name+ '_' + key)
            row.append(json[key])
        else:
            columns.append(key)
            row.append(json[key])
    return columns, row

def parse_by_player(playerid, json):
    columns, row = parse_json(json, row=[], columns=[])
    parsed_row = np.full(len(use_columns), None)
    winningTeam = None
    playerTeam = None
    i=0
    while(i < len(columns)):
        # Find winning team
        if columns[i].endswith('mvp') and row[i] == True:
            winningTeam = columns[i]

        if columns[i] == ("orange_players_id_id") and row[i]==playerid:
            playerTeam = columns[i]
            while not(columns[i].startswith('orange_players_stats')):
                i += 1
            while(columns[i].startswith('orange_players_stats')):
                column_name = columns[i][7:]
                if column_name.endswith('mvp') and row[i] == True:
                    winningTeam = columns[i]
                elif column_name in use_columns:
                    index = use_columns.index(column_name)
                    parsed_row[index] = row[i]
                i += 1
        elif columns[i] == ("blue_players_id_id") and row[i]==playerid:
            playerTeam = columns[i]
            while not(columns[i].startswith('blue_players_stats')):
                i += 1
            while(columns[i].startswith('blue_players_stats')):
                column_name = columns[i][5:]
                if column_name.endswith('mvp') and row[i] == True:
                    winningTeam = columns[i]
                elif column_name in use_columns:
                    index = use_columns.index(column_name)
                    parsed_row[index] = row[i]
                i += 1
        elif columns[i] in use_columns:
            index = use_columns.index(columns[i])
            parsed_row[index] = row[i]
            i += 1
        else:
            i += 1

    #Add win to end of row
    if(playerTeam[0]==winningTeam[0]):
        parsed_row[-1] = 1
    else:
        parsed_row[-1] = 0

    return columns, parsed_row

def parse_by_team(playerid, json):
    columns, row = parse_json(json, row=[], columns=[])
    parsed_row = np.full(len(use_columns), None)
    winningTeam = None
    playerTeam = None
    i=0
    while(i < len(columns)):
        # Find winning team
        if columns[i].endswith('mvp') and row[i] == True:
            winningTeam = columns[i]

        if columns[i] == ("orange_players_id_id") and row[i]==playerid:
            playerTeam = columns[i]
            while not(columns[i].startswith('orange_players_stats')):
                i += 1
            while(columns[i].startswith('orange_players_stats')):
                column_name = columns[i][7:]
                if column_name.endswith('mvp') and row[i] == True:
                    winningTeam = columns[i]
                elif column_name in use_columns:
                    index = use_columns.index(column_name)
                    parsed_row[index] = row[i]
                i += 1
        elif columns[i] == ("blue_players_id_id") and row[i]==playerid:
            playerTeam = columns[i]
            while not(columns[i].startswith('blue_players_stats')):
                i += 1
            while(columns[i].startswith('blue_players_stats')):
                column_name = columns[i][5:]
                if column_name.endswith('mvp') and row[i] == True:
                    winningTeam = columns[i]
                elif column_name in use_columns:
                    index = use_columns.index(column_name)
                    parsed_row[index] = row[i]
                i += 1
        elif columns[i] in use_columns:
            index = use_columns.index(columns[i])
            parsed_row[index] = row[i]
            i += 1
        else:
            i += 1

    #Add win to end of row
    if(playerTeam[0]==winningTeam[0]):
        parsed_row[-1] = 1
    else:
        parsed_row[-1] = 0

    return columns, parsed_row
    

def clean_list_by_player(json_list, playerid):
    rows = np.full([len(json_list), len(use_columns)], None)
    for i in range(len(json_list)):
        columns, row = parse_by_player(playerid, json_list[i])
        rows[i] = row
    return rows


def read_variables():
    return