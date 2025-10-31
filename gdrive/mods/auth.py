import json
import os
from typed import typed, Path, Json, Union, List, Any
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SCOPES = [
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/documents',
    'https://www.googleapis.com/auth/spreadsheets'
]

@typed
def auth(
    credentials_data: Union(Path, Json),
    token_data: Union(Path, Json),
    scopes: List=SCOPES
    ) -> Any:

    creds = None

    if token_data in Path and os.path.exists(token_data):
        creds = Credentials.from_authorized_user_file(token_data, SCOPES)
    elif token_data in Json:
        try:
            creds = Credentials.from_authorized_user_info(token_data, SCOPES)
        except ValueError as e:
            print(f"Error loading token from dictionary: {e}")
            creds = None

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if credentials_data in Path and os.path.exists(credentials_data):
                flow = InstalledAppFlow.from_client_secrets_file(
                    credentials_data, SCOPES)
            elif credentials_data in Json:
                flow = InstalledAppFlow.from_client_secrets_json(
                    json.dumps(credentials_data), SCOPES)
            else:
                raise ValueError("Invalid credentials_data: Must be a file path or a dictionary.")

            creds = flow.run_local_server(port=0)

        if token_data in Path:
            with open(token_data, 'w') as token_file:
                token_file.write(creds.to_json())

    return creds
