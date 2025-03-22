from googleapiclient.discovery import build

class service:
    def drive(creds):
        return build('drive', 'v3', credentials=creds)

    def docs(creds):
        return build('docs', 'v1', credentials=creds)

    def sheets(creds):
        return build('sheets', 'v4', credentials=creds)
