from googleapiclient.discovery import build
from gdrive.mods.auth import creds

class service:
    def drive():
        return build('drive', 'v3', credentials=creds)

    def docs():
        return build('docs', 'v1', credentials=creds)

    def sheets():
        return build('sheets', 'v4', credentials=creds)
