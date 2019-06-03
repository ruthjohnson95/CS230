from __future__ import print_function
import pickle
import io
import os.path
import shutil
import sys
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.http import MediaIoBaseDownload

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive', 
            'https://www.googleapis.com/auth/drive.file', 
            'https://www.googleapis.com/auth/drive.metadata']

# A list of filenames to be downloaded
download_list = []

DRIVEAPI_DIR = os.path.dirname(os.path.abspath(__file__))

def main():
    
    if len(sys.argv) != 3:
        print("Usage: python3 ./google_drive_downloader.py download_list.txt <download path>")
        sys.exit()

    out_path = sys.argv[2]
    download_list_filename = sys.argv[1]

    with open(download_list_filename, 'r') as dl_file:
        for line in dl_file:
            dlf = line.rstrip()
            download_list.append(dlf)
        
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open(DRIVEAPI_DIR+'/token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                DRIVEAPI_DIR+'/credentials.json', SCOPES)
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open(DRIVEAPI_DIR+'/token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('drive', 'v3', credentials=creds)

    # List all the shared drives and find CS230-Benchmarks
    drives = service.drives().list().execute()
    drives_list = drives.get('drives')
    drive_id = ''
    for drive in drives_list:
        if drive.get('name') == 'CS230-Benchmarks':
            drive_id = drive.get('id')
    
    if drive_id == '':
        print("Cannot find CS230-Benchmarks drive")
        return
    
    print("Drive ID: "+drive_id)
    # Call the Drive v3 API
    results = service.files().list(
        orderBy="name",
        supportsAllDrives=True, 
        pageSize=1000,
        fields="nextPageToken, files(id, name)", 
        includeItemsFromAllDrives=True, 
        driveId=drive_id, 
        corpora='drive').execute()
    items = results.get('files', [])

    if not items:
        print('No files found.')
    else:
        print("item number: " + str(len(items)))
        print('Files:')
        for item in items:
            file_id = item['id']
            filename = item['name']
            if filename in download_list:
                request = service.files().get_media(fileId=file_id)
                fh = io.BytesIO()
                downloader = MediaIoBaseDownload(fh, request)
                done = False
                while done is False:
                    status, done = downloader.next_chunk()
                    print("Download %d%%." % int(status.progress() * 100))
                with open(out_path + item['name'], "wb") as outfile:   
                    buf = fh.getvalue()
                    if not buf:
                        continue
                    outfile.write(buf)
                print(u'{0} ({1})'.format(item['name'], item['id']))

if __name__ == '__main__':
    main()