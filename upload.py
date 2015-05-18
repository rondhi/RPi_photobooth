#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import httplib2
import pprint
import logging

from apiclient.discovery import build
from apiclient.http import MediaFileUpload
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.file import Storage

logging.basicConfig()

# Copy your credentials from the console
CLIENT_ID = 'xxxxxxxxxxxxxxxxxxxxxxxxxxx.apps.googleusercontent.com'
CLIENT_SECRET = 'xxxxxxxxxxxxxxxxxxxxxxxxxxx'

# Check https://developers.google.com/drive/scopes for all available scopes
OAUTH_SCOPE = 'https://www.googleapis.com/auth/drive'

# Redirect URI for installed apps
REDIRECT_URI = 'urn:ietf:wg:oauth:2.0:oob'



# when you are looking at a folder on google drive the folder will look like this:
# https://drive.google.com/?authuser=0#folders/ZZZZZZZZZZZZZZZZZZZZZZZZZZZ

# below folder to upload files to, put those characters 
# from the link like above (Z's), into this string below
GOOGLE_DRIVE_FOLDER = 'ZZZZZZZZZZZZZZZZZZZZZZZZZZZ'




if(len(sys.argv)==2):
    # Path to the file to upload
    #FILENAME = 'document.txt'
    FILENAME = str(sys.argv[1])


    if (len(FILENAME.split('/'))> 1) :
        FILE = FILENAME.split('/')[1]
    else:
        FILE = FILENAME

    #IF NOT PREVIOUSLY STORED RUN THIS CODE INSTEAD
    #------------------------------------------------------
    # Run through the OAuth flow and retrieve credentials
    flow = OAuth2WebServerFlow(CLIENT_ID, CLIENT_SECRET, OAUTH_SCOPE, REDIRECT_URI)
    authorize_url = flow.step1_get_authorize_url()
    print 'Go to the following link in your browser: ' + authorize_url
    code = raw_input('Enter verification code: ').strip()
    credentials = flow.step2_exchange(code)
    print 'storing credentials' + str(credentials)
    storage = Storage('a_credentials_file')
    storage.put(credentials)
    #------------------------------------------------------
    
    #****IMPORTANT*****************************************************<<<<<<<<<<<<<
    ##USE THIS AFTER YOU GET THE STRING
    ##PREVIOUSLY STORED CREDENTIALS
    #storage = Storage('a_credentials_file')
    #print 'getting credentials from file'
    #credentials = storage.get()
    
    

    # Create an httplib2.Http object and authorize it with our credentials
    http = httplib2.Http()
    http = credentials.authorize(http)

    drive_service = build('drive', 'v2', http=http)

    # Insert a file
    media_body = MediaFileUpload(FILENAME, mimetype='text/plain', resumable=True)

    # File attributes
    body = {'title': FILE,'description': '','mimeType': 'image/jpg'}
    body['parents'] = [{'id': GOOGLE_DRIVE_FOLDER}]

    #print FILE

    file = drive_service.files().insert(body=body, media_body=media_body).execute()
    pprint.pprint(file)

else:
    print "wrong number of arguments: " +str(len(sys.argv))
    print "upload.py needs 2 (example: sudo python upload.py document.txt)"
