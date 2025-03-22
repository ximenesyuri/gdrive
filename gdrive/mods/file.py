from gdrive.mods.service import service

def remove(file_id):
    try:
        service_ = service.drive()
        service_.files().delete(fileId=file_id).execute()
        print(f"File with ID {file_id} was successfully deleted.")
    except Exception as e:
        print(f"An error occurred: {e}")

def move(file_id, parent_id):
    service_ = service.drive()
    file = service_.files().get(fileId=file_id, fields="parents").execute()
    previous_parents = ",".join(file.get('parents'))
    service_.files().update(fileId=file_id, addParents=parent_id, removeParents=previous_parents).execute()

def copy(file_id, parent_id):
    service_ = service.drive()
    copied_file = service_.files().copy(fileId=file_id, body={'parents': [parent_id]}).execute()
    return copied_file
