from gdrive.mods.service import service
from gdrive.mods.file import remove, move, copy

class spreadsheet:
    class get:
        @staticmethod
        def id(name, parent_id):
            query = f"'{parent_id}' in parents and mimeType = 'application/vnd.google-apps.spreadsheet' and name = '{name}'"
            service_ = service.drive()
            results = service_.files().list(q=query, fields="files(id)").execute()
            items = results.get('files', [])
            return items[0]['id'] if items else None

        @staticmethod
        def name(sheet_id):
            service_ = service.sheets()
            sheet = service_.spreadsheets().get(spreadsheetId=sheet_id).execute()
            return sheet.get('properties', {}).get('title', None)

        @staticmethod
        def creation(sheet_id):
            service_ = service.drive()
            sheet = service_.files().get(fileId=sheet_id, fields="createdTime").execute()
            return sheet.get('createdTime', None)

        @staticmethod
        def modified(sheet_id):
            service_ = service.drive()
            sheet = service_.files().get(fileId=sheet_id, fields="modifiedTime").execute()
            return sheet.get('modifiedTime', None)

        @staticmethod
        def all(sheet_id):
            service_sheets = service.sheets()
            service_drive = service.drive()
            sheet = service_sheets.spreadsheets().get(spreadsheetId=sheet_id).execute()
            drive_meta = service_drive.files().get(fileId=sheet_id, fields="createdTime, modifiedTime").execute()
            return {
                'id': sheet.get('spreadsheetId'),
                'name': sheet.get('properties', {}).get('title', ''),
                'creation': drive_meta.get('createdTime', None),
                'modified': drive_meta.get('modifiedTime', None)
            }

    @staticmethod
    def list(parent_id):
        service_ = service.drive()
        query = f"'{parent_id}' in parents and mimeType = 'application/vnd.google-apps.spreadsheet'"
        results = service_.files().list(
            q=query,
            fields="files(id, name)"
        ).execute()

        spreadsheets = [
            {
                'id': item['id'],
                'name': item['name']
            }
            for item in results.get('files', [])
        ]

        return {
            'parent_id': parent_id,
            'spreadsheets': spreadsheets
        }
    ls = list

    @staticmethod
    def create(title, parent_id):
        sheet_metadata = {
            'properties': {
                'title': title
            }
        }

        service_ = service.sheets()
        sheet = service_.spreadsheets().create(body=sheet_metadata).execute()

        service_ = service.drive()
        service_.files().update(fileId=sheet['spreadsheetId'],
                                addParents=parent_id).execute()

        return {
            'id': sheet['spreadsheetId'],
            'name': sheet.get('properties', {}).get('title', ''),
            'createdTime': 'N/A',
            'modifiedTime': 'N/A'
        }
    mk = create

    remove = remove
    rm     = remove

    copy = copy
    cp   = copy

    move = move
    mv   = move
