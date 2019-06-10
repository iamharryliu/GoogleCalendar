# Google API
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# Token Pickle
from os import path
import pickle

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']


def getService():
    ''' get google calender api service'''
    credentials = None
    credentials = getCredentials()
    # If there are no (valid) credentials available, let the user log in.
    credentials_not_valid = not credentials or not credentials.valid
    if credentials_not_valid:
        attemptToResolveCredentials(credentials)
    service = build('calendar', 'v3', credentials=credentials)
    return service


def getCredentials():
    if path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            credentials = pickle.load(token)
    return credentials


def attemptToResolveCredentials(credentials):
    credentialsExpiredAndRefreshTokenAvailable = credentials and credentials.expired and credentials.refresh_token
    if credentialsExpiredAndRefreshTokenAvailable:
        refreshCredentials(credentials)
    else:
        flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
        credentials = flow.run_local_server()
    saveCredentials(credentials)


def refreshCredentials(credentials):
    credentials.refresh(Request())


def saveCredentials(credentials):
    with open('token.pickle', 'wb') as token:
        pickle.dump(credentials, token)
