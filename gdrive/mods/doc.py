from gdrive.mods.service import service
from gdrive.mods.file import remove, copy, move

class doc:
    class get:
        @staticmethod
        def id(name, parent_id):
            query = f"'{parent_id}' in parents and mimeType = 'application/vnd.google-apps.document' and name = '{name}'"
            service_ = service.drive()
            results = service_.files().list(q=query, fields="files(id)").execute()
            items = results.get('files', [])
            return items[0]['id'] if items else None

        @staticmethod
        def name(doc_id):
            service_ = service.docs()
            doc = service_.documents().get(documentId=doc_id).execute()
            return doc.get('title', None)

        @staticmethod
        def creation(doc_id):
            service_ = service.drive()
            doc = service_.files().get(fileId=doc_id, fields="createdTime").execute()
            return doc.get('createdTime', None)

        @staticmethod
        def modified(doc_id):
            service_ = service.drive()
            doc = service_.files().get(fileId=doc_id, fields="modifiedTime").execute()
            return doc.get('modifiedTime', None)

        @staticmethod
        def all(doc_id):
            service_docs = service.docs()
            service_drive = service.drive()
            doc = service_docs.documents().get(documentId=doc_id).execute()
            drive_meta = service_drive.files().get(fileId=doc_id, fields="createdTime, modifiedTime").execute()

            return {
                'id': doc.get('documentId'),
                'name': doc.get('title', ''),
                'creation': drive_meta.get('createdTime', None),
                'modified': drive_meta.get('modifiedTime', None)
            }

    @staticmethod
    def list(parent_id):
        service_ = service.drive()
        query = f"'{parent_id}' in parents and mimeType = 'application/vnd.google-apps.document'"
        results = service_.files().list(
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
    def create(title, parent_id):
        doc_metadata = {
            'title': title
        }

        service_ = service.docs()
        doc = service_.documents().create(body=doc_metadata).execute()

        service_ = service.drive()
        service_.files().update(fileId=doc['documentId'],
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
