from gdrive.mods.file import remove, move, copy
import json

class sheet:
    class get:
        @staticmethod
        def id(service_drive, name, parent_id):
            query = f"'{parent_id}' in parents and mimeType = 'application/vnd.google-apps.spreadsheet' and name = '{name}'"
            results = service_drive.files().list(q=query, fields="files(id)").execute()
            items = results.get('files', [])
            return items[0]['id'] if items else None

        @staticmethod
        def name(service_sheets, sheet_id):
            sheet = service_sheets.spreadsheets().get(spreadsheetId=sheet_id).execute()
            return sheet.get('properties', {}).get('title', None)

        @staticmethod
        def creation(service_drive, sheet_id):
            sheet = service_drive.files().get(fileId=sheet_id, fields="createdTime").execute()
            return sheet.get('createdTime', None)

        @staticmethod
        def modified(service_drive, sheet_id):
            sheet = service_drive.files().get(fileId=sheet_id, fields="modifiedTime").execute()
            return sheet.get('modifiedTime', None)

        @staticmethod
        def all(service_drive, service_sheets, sheet_id):
            sheet = service_sheets.spreadsheets().get(spreadsheetId=sheet_id).execute()
            drive_meta = service_drive.files().get(fileId=sheet_id, fields="createdTime, modifiedTime").execute()
            return {
                'id': sheet.get('spreadsheetId'),
                'name': sheet.get('properties', {}).get('title', ''),
                'creation': drive_meta.get('createdTime', None),
                'modified': drive_meta.get('modifiedTime', None)
            }

    class read:
        def sheet(service_sheets, spreadsheet_id, sheet_name):
            cell_range = f'{sheet_name}'
            result = service_sheets.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range=cell_range).execute()
            return result.get('values', [])

        def cell(service_sheets, spreadsheet_id, sheet_name, row, line):
            cell_range = f'{sheet_name}!{row}{line}'
            result = service_sheets.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range=cell_range).execute()
            return result.get('values', [])

    class export:
        class sheet:
            def to_json(service_sheets, spreadsheet_id, sheet_name, headers=True, start_line="1", start_row="A"):
                cell_range = f"{sheet_name}!{start_row}{start_line}"
                result = service_sheets.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range=cell_range).execute()
                values = result.get('values', [])
                if not values:
                    print('No data found.')
                    return []
                if headers:
                    headers = values[0]
                    rows = values[1:]
                else:
                    headers = [f"Column{i+1}" for i in range(len(values[0]))]
                    rows = values
                json_data = [dict(zip(headers, row)) for row in rows]
                return json_data

    @staticmethod
    def list(service_drive, parent_id):
        query = f"'{parent_id}' in parents and mimeType = 'application/vnd.google-apps.spreadsheet'"
        results = service_drive.files().list(
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
    def create(service_drive, service_sheets, title, parent_id):
        sheet_metadata = {
            'properties': {
                'title': title
            }
        }

        sheet = service_sheets.spreadsheets().create(body=sheet_metadata).execute()
        service_drive.files().update(fileId=sheet['spreadsheetId'],
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
