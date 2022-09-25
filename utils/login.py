import streamlit as st
import json
import requests
import pandas
import time

def get_tokens_init(client_id, client_secret, code):
    # Make Strava auth API call with your 
    # client_code, client_secret and code
    response = requests.post(
                        url = 'https://www.strava.com/oauth/token',
                        data = {
                                'client_id': int(client_id),
                                'client_secret': f'{client_secret}',
                                'code': f'{code}',
                                'grant_type': 'authorization_code'
                                }
                    )
        #Save json response as a variable
    strava_tokens = response.json()
    # Save tokens to file
    with open('configs/strava_tokens.json', 'w') as outfile:
        json.dump(strava_tokens, outfile)
    # Open JSON file and print the file contents 
    # to check it's worked properly
    # with open('configs/strava_tokens.json') as check:
    #     data = json.load(check)
    # # print(data)
    # return data

def tokens_automate():
    ## Get the tokens from file to connect to Strava
    with open('configs/strava_tokens.json') as json_file:
        strava_tokens = json.load(json_file)
    
    with open('configs/login_details.json') as json_file:
        login_details = json.load(json_file)

    ## If access_token has expired then use the refresh_token to get the new access_token
    if strava_tokens['expires_at'] < time.time():
        #Make Strava auth API call with current refresh token
        response = requests.post(
                            url = 'https://www.strava.com/oauth/token',
                            data = {
                                    'client_id': login_details['client_id'],
                                    'client_secret': login_details['client_secret'],
                                    'grant_type': 'refresh_token',
                                    'refresh_token': strava_tokens['refresh_token']
                                    }
                        )
        #Save response as json in new variable
        new_strava_tokens = response.json()
        # Save new tokens to file
        with open('configs/strava_tokens.json', 'w') as outfile:
            json.dump(new_strava_tokens, outfile)
        #Use new Strava tokens from now
        strava_tokens = new_strava_tokens

        return strava_tokens

def login():
    with st.form("Login", clear_on_submit=False):
        st.text_input('Client_id', key = 'id')
        st.text_input('Client_secret', key = 'secret')
        st.text_input('Code', key = 'code')

        submitted = st.form_submit_button("Submit")

        if submitted:

            if st.session_state.id != None and st.session_state.secret != None and st.session_state.code != None:
                login_dict = {
                    'client_id': int(st.session_state.id),
                    'client_secret': str(st.session_state.secret),
                    'code': str(st.session_state.code),
                }

                get_tokens_init(st.session_state.id, st.session_state.secret, st.session_state.code)

            with open('configs/login_details.json', 'w') as login:
                json.dump(login_dict, login)
                
            tokens_automate()

