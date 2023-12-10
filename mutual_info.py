from clean import clean_list_by_player
import get_data
import config
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_selection import SelectKBest, mutual_info_classif
from matplotlib import pyplot
from sklearn.preprocessing import OrdinalEncoder
from datetime import date

def mutual_info_by_player(json_list, playerid, out_dir = '', plot=False):
    rows = clean_list_by_player(json_list, playerid)
    df = pd.DataFrame(rows, columns=config.use_columns)
    target = df['win'].astype(int)
    df = df.drop(['win'], axis='columns')

    #Encode Categorical Columns
    df_categorical = ordinal_encode(df)
    df = df.drop(df_categorical.columns.tolist(), axis='columns')
    df_new = pd.concat([df, df_categorical], axis='columns')
    
    x_train, x_test, y_train, y_test = train_test_split(df_new, target, test_size=0.2)
    x_train_fs, x_test_fs, fs = select_features(x_train, y_train, x_test)

    if out_dir != '':
       with open(f'{out_dir}/mutual_info_{date.today()}.txt', 'w') as f:
          sorted_scores = sorted(fs.scores_, reverse=True)
          for i in range(len(sorted_scores)):
             f.write(f'{config.use_columns[:-1][fs.scores_.tolist().index(sorted_scores[i])]}: {sorted_scores[i]}\n')
             f.close()

    if plot:
        pyplot.bar(config.use_columns[:-1], fs.scores_)
        pyplot.xticks(rotation=45)
        pyplot.show()
    return

def ordinal_encode(df):
    encoder = OrdinalEncoder().set_output(transform='pandas')
    encoded_df = encoder.fit_transform(df[config.categorical_columns])
    return encoded_df

def select_features(x_train, y_train, x_test):
 # configure to select all features
 fs = SelectKBest(score_func=mutual_info_classif, k='all')
 # learn relationship from training data
 fs.fit(x_train, y_train)
 # transform train input data
 X_train_fs = fs.transform(x_train)
 # transform test input data
 X_test_fs = fs.transform(x_test)
 return X_train_fs, X_test_fs, fs
    

json_list = get_data.get_replays(num=600, dir_path='Replays/Bungo_Data')
mutual_info_by_player(json_list, '76561198056469562', 'Scarlet')