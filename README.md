# About

`gdrive` is an intuitive Python client for the basic utilities of Google Drive API.

# Install

With `pip`:
```bash
pip install git+https://github.com/ximenesyuri/gdrive
```

With [py](https://github.com/ximenesyuri/py):
```bash
py install ximenesyuri/gdrive
```

# Usage

Authentication:
```python
from gdrive import gd
cred = gd.auth('/path/to/credentials.json', '/path/to/token.json')
```
Generating services:
```python
drive  = gd.service.drive(cred)
docs   = gd.service.docs(cred)
sheets = gd.service.sheets(cred)
```

Executing commands:
```python
gd.folder.list(drive, parent_folder_id)
...
```
