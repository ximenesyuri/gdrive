from gdrive.mods.file import remove

class folder:
    class get:
        @staticmethod
        def id(service_drive, name, parent_id):
            query = f"'{parent_id}' in parents and mimeType = 'application/vnd.google-apps.folder' and name = '{name}'"
            results = service_drive.files().list(q=query, fields="files(id)").execute()
            items = results.get('files', [])
            return items[0]['id'] if items else None

        @staticmethod
        def name(service_drive, folder_id):
            folder = service_drive.files().get(fileId=folder_id, fields="name").execute()
            return folder.get('name', None)

        @staticmethod
        def creation(service_drive, folder_id):
            folder = service_drive.files().get(fileId=folder_id, fields="createdTime").execute()
            return folder.get('createdTime', None)

        @staticmethod
        def modified(service_drive, folder_id):
            folder = service_drive.files().get(fileId=folder_id, fields="modifiedTime").execute()
            return folder.get('modifiedTime', None)

        @staticmethod
        def all(service_drive, folder_id):
            folder = service_drive.files().get(fileId=folder_id, fields="id, name, createdTime, modifiedTime").execute()
            return {
                'id': folder.get('id'),
                'name': folder.get('name'),
                'creation': folder.get('createdTime'),
                'modified': folder.get('modifiedTime')
            }

    @staticmethod
    def list(service_drive, parent_id):
        parent_details = folder.get.all(service_drive, parent_id)
        query = f"'{parent_id}' in parents and mimeType = 'application/vnd.google-apps.folder'"
        results = service_drive.files().list(
            q=query,
            fields="files(id, name, createdTime, modifiedTime)"
        ).execute()

        subfolders = [
            {
                'id': item['id'],
                'name': item['name'],
                'creation': item['createdTime'],
                'modified': item['modifiedTime']
            }
            for item in results.get('files', [])
        ]

        return {
            'parent': parent_details,
            'subfolders': subfolders
        }
    ls = list

    @staticmethod
    def create(service_drive, name, parent_id):
        folder_metadata = {
            'name': name,
            'mimeType': 'application/vnd.google-apps.folder',
            'parents': [parent_id]
        }
        folder = service_drive.files().create(body=folder_metadata, fields='id, name, createdTime, modifiedTime').execute()

        return {
            'id': folder['id'],
            'name': folder['name'],
            'creation': folder['createdTime'],
            'modified': folder['modifiedTime']
        }
    mk = create

    remove = remove
    rm     = remove

    @staticmethod
    def move(service_drive, folder_id, parent_id, recursive=True):
        if recursive:
            query = f"'{folder_id}' in parents"
            results = service_drive_.files().list(q=query, fields="files(id, mimeType)").execute()
            for item in results.get('files', []):
                if item['mimeType'] == 'application/vnd.google-apps.folder':
                    Folder.mv(item['id'], parent_id, recursive)
                else:
                    service_drive.files().update(fileId=item['id'], addParents=parent_id, removeParents=folder_id).execute()
        service_drive.files().update(fileId=folder_id, addParents=parent_id, removeParents=folder_id).execute()
    mv = move

    @staticmethod
    def copy(service_drive, folder_id, parent_id, recursive=True):
        copied_folder = service_drive.files().copy(fileId=folder_id, body={'parents': [parent_id]}).execute()

        if recursive:
            query = f"'{folder_id}' in parents and mimeType != 'application/vnd.google-apps.folder'"
            results = service_drive.files().list(q=query, fields="files(id)").execute()
            for item in results.get('files', []):
                service_drive_.files().copy(fileId=item['id'], body={'parents': [copied_folder['id']]}).execute()

            subfolders_query = f"'{folder_id}' in parents and mimeType = 'application/vnd.google-apps.folder'"
            subfolders = service_drive.files().list(q=subfolders_query, fields="files(id)").execute()
            for item in subfolders.get('files', []):
                Folder.copy(item['id'], copied_folder['id'], recursive)

        return copied_folder
    cp = copy
