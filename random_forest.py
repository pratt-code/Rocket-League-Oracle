from clean import clean_list_by_player
import get_data
import config
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import OrdinalEncoder

def randomforest_by_player(json_list, playerid):
    rows = clean_list_by_player(json_list, playerid)
    df = pd.DataFrame(rows, columns=config.use_columns)
    target = df['win'].astype(int)
    df = df.drop(['win'], axis='columns')

    #Encode Categorical Columns
    df_categorical = ordinal_encode(df)
    df = df.drop(df_categorical.columns.tolist(), axis='columns')
    df_new = pd.concat([df, df_categorical], axis='columns')
    
    x_train, x_test, y_train, y_test = train_test_split(df_new, target, test_size=0.2)
    model = RandomForestClassifier(n_estimators=50)
    model.fit(x_train, y_train)
    print(model.score(x_test, y_test))
    return

def ordinal_encode(df):
    encoder = OrdinalEncoder().set_output(transform='pandas')
    encoded_df = encoder.fit_transform(df[config.categorical_columns])
    return encoded_df
    

json_list = get_data.read_replays('Replays/Maseter_Data')
randomforest_by_player(json_list, '76561198354051269')