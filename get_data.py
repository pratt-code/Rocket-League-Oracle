import api
import config
import json
import os

def get_replays(params=config.params, num=200, dir_path=''):
    json_list = []
    conn = api.ballchasing()
    next_call = None
    count = 0

    while count<num:
        if next_call is None:
            group_json = conn.get_group(params)
        else:
            group_json = conn.get_with_link(next_call)

        for item in group_json['list']:
            replay_json = conn.get_replay(item['id'])
            json_list.append(replay_json)

            if dir_path != '':
                if not os.path.exists(dir_path):
                    os.makedirs(dir_path)
                with open(f'{dir_path}/{count}.txt', 'w') as f:
                    json.dump(replay_json, f, indent=4)
                    f.close()

            count += 1
            print(count)
        
        if 'next' in group_json.keys():
            next_call = group_json['next']
        else:
            break

    return json_list

def read_replays(dir_path):
    path_list = os.listdir(dir_path)
    json_list = []
    for replay in path_list:
        f = open(f'{dir_path}/{replay}', 'r')
        json_list.append(json.load(f))
    return json_list