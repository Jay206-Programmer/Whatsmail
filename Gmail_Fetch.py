import pickle
import os.path
import email
import base64
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def search_messages(service, user_id, search_string):
    try:
        search_id = service.users().messages().list(userId = user_id, q=search_string).execute()
        id_list = list()
        if search_id['resultSizeEstimate']>0:
            message_id = search_id['messages']
            for ids in message_id:
                id_list.append(ids['id'])
        
            return id_list    

        else:
            print("0 results found for this subject.") 
            return None   


    except :
        print("An error occured:")

def get_message(service, user_id, msg_id):
    try:
        message_list = service.users().messages().get(userId = user_id, id =msg_id, format='raw').execute()
        msg_raw = base64.urlsafe_b64decode(message_list['raw'].encode('ASCII'))
        msg_str = email.message_from_bytes(msg_raw)

        content_types = msg_str.get_content_maintype()

        if content_types == 'multipart':
            ls = msg_str.get_payload()

            return ls[0].get_payload()
        else:
            return msg_str.get_payload()    

    except :
        print("An error occured:")


def get_service():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)
    
    return service

def Test_search():
    key = input("Enter Search Key:")
    s = get_service()    
    res = search_messages(s,'me',key)
    
    for ids in res:
        print(get_message(s,'me',ids))
        
        break

if __name__ == '__main__':
    Test_search()    