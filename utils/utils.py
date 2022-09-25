import json

def read_configs():
    with open('configs/strava_tokens.json') as json_file:
        strava_tokens = json.load(json_file)
    
    with open('configs/login_details.json') as json_file:
        login_details = json.load(json_file)

    return strava_tokens, login_details