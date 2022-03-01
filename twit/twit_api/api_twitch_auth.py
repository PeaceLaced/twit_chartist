'''
- testing twitch auth.
'''
import re
import sys
import json
import socket
import requests
import webbrowser
import urllib.parse

from twit.twit_api.api_progress_handler import Progress as progress

class RedirectTimeoutError(Exception):
    pass

# only call this using the CHART bot
def validate_player(player):

    from twit.twit_api.config.config_twitch import TWIT_CHART_CLIENT as CLIENT_ID
    from twit.twit_api.config.config_twitch import TWIT_CHART_SECRET as CLIENT_SECRET
    from twit.twit_api.config.config_twitch import TWIT_CHART_PATH_APP as APP_TOKEN_PATH
    
    with open(APP_TOKEN_PATH, 'rb') as f:
        token_data = f.read()
        token_json = json.loads(token_data.decode())
        app_token = token_json['access_token']
    
    #print(app_token)
    #input('this is app_token')
    
    headers = {'Authorization': 'Bearer ' + app_token, 'Client-Id' : CLIENT_ID}
    ret_data = requests.get('https://api.twitch.tv/helix/users?login=' + player, headers=headers)
    
    #print(ret_data.json())
    #input('this is ret_data')
    
    return ret_data.json()

'''
curl -X GET 'https://api.twitch.tv/helix/users?id=141981764' \
-H 'Authorization: Bearer cfabdegwdoklmawdzdo98xt2fo512y' \
-H 'Client-Id: uo6dggojyb8d6soh92zknwmi5ej1q2'

'''

def get_user_id(client_id, user_token):
    headers = {'Authorization': 'Bearer ' + user_token,'Client-Id': client_id}
    ret_data = requests.get('https://api.twitch.tv/helix/users?login=peacelaced',
                               headers=headers)
    print(ret_data.json())

# use these while testing
def print_app_data(app_data, app_verified):
    print(app_data)
    print(app_verified)
    
def print_user_data(user_data, user_verified):
    print(user_data)
    print(user_verified)

    
########################################################################################

# TODO: does this work with both USER and CLIENT???
def verify_token(token, clientid, clientsecret, refresh_token, token_path):
    ''' verify the token'''
    verify_return = requests.get("https://id.twitch.tv/oauth2/validate",
                                 headers={"Authorization": "Bearer " + token})
    content = verify_return.json()
    if "status" in content and content["status"] == 401:
        if refresh_token is None:
            return False
        if token_path is None:
            return False
        
        body = {
            'grant_type':'refresh_token',
            'refresh_token':refresh_token,
            'client_id':clientid,
            'client_secret':clientsecret}

        verify_return = requests.post('https://id.twitch.tv/oauth2/token', body)

        content = verify_return.json()

        progress.s('TOKEN_(refreshed)')
        with open(token_path, 'w') as f:
            f.write(json.dumps(content))
        progress.s('TOKEN_(saved)')
        
    return content   
'''
def validate(oauth: OAuth2Session, can_refresh=True):
    try:
        r = requests.get('https://id.twitch.tv/oauth2/validate',
                         headers={'Authorization': f'OAuth {oauth.token["access_token"]}'})
        # print(r.text)
        r.raise_for_status()
    except requests.HTTPError as e:
        if can_refresh:
            token = oauth.refresh_token(oauth.auto_refresh_url)
            token_saver(token)
            oauth_ = get_session(config.twitch_client_id, config.twitch_client_secret,
                                 'https://iarazumov.com/oauth/twitch')
            validate(oauth_, False)
        else:
            logging.fatal("Validation failed: " + str(e))
            raise RuntimeError("Validation failed")
'''
    
    
def get_user_token(user_token_path, app_client_id, app_secret, scopes, app_uri, port):
    ''' get the user access token, if it does not exist, create it and write'''
    
    progress.i('USER_TOKEN_(search)')
    try:
        with open(user_token_path, 'rb') as f:
            token_data = f.read()
            user_token_json = json.loads(token_data.decode())
            progress.s('USER_TOKEN_(found)')

    except FileNotFoundError:
        progress.w('USER_TOKEN_(create)')
        webbrowser.open("https://id.twitch.tv/oauth2/authorize?" + urllib.parse.urlencode(
            {"redirect_uri": app_uri,
             "client_id": app_client_id,
             "response_type": "code",
             "scope": scopes}))
        with socket.socket() as s:
            s.bind(("127.0.0.1", port))
            s.listen()
            print("Waiting for request...")
            conn, addr = s.accept()
            with conn:
                print("Got a connection...")
                data = ""
                while True:
                    currdata = conn.recv(1024)
                    if not currdata:
                        break
                    data += str(currdata.decode('utf-8'))
                    if data.endswith("\r\n\r\n"):  # means we are at the end of the header request
                        break
                # we expect a browser to be requesting the root page, but all we really care about is the code which is included in the first line.
                # For more info, look into how HTTP works.
                firstline = data.splitlines()[0]
                code = re.match(r"GET /\?code=(?P<code>.*)&scope=(?P<scopes>.*) HTTP/(?P<version>.*)",
                                firstline).group("code")
                responseContent = "Thank you, code received".encode("utf-8")
                conn.sendall((
                                         "HTTP/1.1 200 OK\r\nHost: localhost\r\nServer: MarenthyuTwitchPYthonExample/1.1\r\nContent-Type: text/plain\r\nContent-Length: " + str(
                                     len(responseContent)) + "\r\n\r\n").encode("utf-8") + responseContent)
            print("Connection closed.")
        print("Socket closed.")
        
        body = {
            'client_id':app_client_id,
            'client_secret':app_secret,
            'code':code,
            'grant_type':'authorization_code',
            'redirect_uri':app_uri}
        user_token_data = requests.post("https://id.twitch.tv/oauth2/token", body)
        user_token_json = user_token_data.json()
        
        # write it to file
        with open(user_token_path, 'w') as f:
            f.write(json.dumps(user_token_json))
        progress.s('USER_TOKEN_(saved)')
    
    
    # verify the app access token
    user_token = user_token_json['access_token']
    refresh_token = user_token_json['refresh_token']
    verified_token = verify_token(user_token, app_client_id, app_secret, refresh_token, user_token_path)
    
    if not verified_token:
        progress.e(f'USER token at {user_token_path} did not verify, delete the json and recreate')
        progress.s('exiting')
        sys.exit()
    progress.s('USER_TOKEN_(verified)')
    
    try: return verified_token['access_token']
    except: return user_token

# return the app_token, if it does not exist, create and write
def get_app_token(app_token_path, app_client_id, app_secret, refresh_token=None, user_token_path=None):
    ''' get the app access token, if it does not exist, create it and write'''
    
    progress.i('APP_TOKEN_(search)')
    try:
        # look in the file for the app access token
        with open(app_token_path, 'rb') as f:
            token_data = f.read()
            app_token_json = json.loads(token_data.decode())
            progress.s('APP_TOKEN_(found)')

    except FileNotFoundError:
        # generate token
        progress.w('APP_TOKEN_(create)')
        body = {
            'client_id':app_client_id,
            'client_secret':app_secret,
            'grant_type':'client_credentials'}
        app_token_data = requests.post("https://id.twitch.tv/oauth2/token", body)
        app_token_json = app_token_data.json()

        # write it to a file
        with open(app_token_path, 'w') as f:
            f.write(json.dumps(app_token_json))
        progress.s('APP_TOKEN_(saved)')
    
    # verify the app access token
    app_token = app_token_json['access_token']
    verified_token = verify_token(app_token, app_client_id, app_secret, refresh_token, user_token_path)
    if not verified_token:
        progress.e('APP token did not verify, delete the json and recreate')
        progress.s('exiting')
        sys.exit()
    
    # if verified, return it
    progress.s('APP_TOKEN_(verified)')
    #print_app_data(app_token_json, verified_token)
    #input()
    return app_token