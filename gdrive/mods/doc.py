from gdrive.mods.file import remove, copy, move

class doc:
    class get:
        def id(drive_service, name, parent_id):
            query = f"'{parent_id}' in parents and mimeType = 'application/vnd.google-apps.document' and name = '{name}'"
            results = drive_service.files().list(q=query, fields="files(id)").execute()
            items = results.get('files', [])
            return items[0]['id'] if items else None

        @staticmethod
        def name(service, doc_id):
            doc = service.documents().get(documentId=doc_id).execute()
            return doc.get('title', None)

        @staticmethod
        def creation(service, doc_id):
            doc = service.files().get(fileId=doc_id, fields="createdTime").execute()
            return doc.get('createdTime', None)

        @staticmethod
        def modified(service, doc_id):
            doc = service.files().get(fileId=doc_id, fields="modifiedTime").execute()
            return doc.get('modifiedTime', None)

        @staticmethod
        def all(service_docs, service_drive, doc_id):
            doc = service_docs.documents().get(documentId=doc_id).execute()
            drive_meta = service_drive.files().get(fileId=doc_id, fields="createdTime, modifiedTime").execute()

            return {
                'id': doc.get('documentId'),
                'name': doc.get('title', ''),
                'creation': drive_meta.get('createdTime', None),
                'modified': drive_meta.get('modifiedTime', None)
            }

        @staticmethod
        def content(service_docs, doc_id):
            document = service_docs.documents().get(documentId=doc_id).execute()
            return document.get('body').get('content')

        @staticmethod
        def lists(service_docs, doc_id):
            document = service_docs.documents().get(documentId=doc_id).execute()
            return document.get('lists', {})

    @staticmethod
    def list(service, parent_id):
        query = f"'{parent_id}' in parents and mimeType = 'application/vnd.google-apps.document'"
        results = service.files().list(
            q=query,
            fields="files(id, name)"
        ).execute()

        documents = [
            {
                'id': item['id'],
                'name': item['name']
            }
            for item in results.get('files', [])
        ]

        return {
            'parent_id': parent_id,
            'documents': documents
        }

    @staticmethod
    def create(service_docs, service_drive, title, parent_id):
        doc_metadata = {
            'title': title
        }

        doc = service_docs.documents().create(body=doc_metadata).execute()

        service_drive.files().update(fileId=doc['documentId'],
                                addParents=parent_id).execute()

        return {
            'id': doc['documentId'],
            'name': doc.get('title', ''),
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
