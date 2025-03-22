def remove(service_drive, file_id):
    try:
        service_drive.files().delete(fileId=file_id).execute()
        print(f"File with ID {file_id} was successfully deleted.")
    except Exception as e:
        print(f"An error occurred: {e}")

def move(service_drive, file_id, parent_id):
    file = service_drive.files().get(fileId=file_id, fields="parents").execute()
    previous_parents = ",".join(file.get('parents'))
    service_drive.files().update(fileId=file_id, addParents=parent_id, removeParents=previous_parents).execute()

def copy(service_drive, file_id, parent_id):
    copied_file = service_drive.files().copy(fileId=file_id, body={'parents': [parent_id]}).execute()
    return copied_file
