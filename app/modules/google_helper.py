from oauth2client.client import flow_from_clientsecrets
from googleapiclient.discovery import build

# Local imports
from app import settings


def get_auth_url(email_address: str) -> str:
    """
    Gets an authentication URL for a given email
    """
    flow = get_flow()
    flow.params['access_type'] = 'offline'
    flow.params['approval_prompt'] = 'force'
    flow.params['user_id'] = email_address
    return flow.step1_get_authorize_url()


def get_flow():
    """
    Creates an authentication flow based on
    the App's credentials and requested Scopes
    """
    flow = flow_from_clientsecrets(
        settings.CLIENTSECRETS_LOCATION,
        " ".join(settings.SCOPES),
        redirect_uri=settings.REDIRECT_URI
    )
    return flow


def get_service(auth_code: str):
    """
    Exchanges the auth_code for a credential
    and uses it to build a Google API Service
    """
    flow = get_flow()
    credentials = flow.step2_exchange(auth_code)
    service = build("gmail", "v1", credentials=credentials)
    return service


def get_labels(auth_code):
    service = get_service(auth_code)
    api_response = service.users().labels().list(userId="me").execute()
    return api_response


def get_headers(auth_code: str) -> list:
    """
    Exchanges an auth_code for a credential and uses it
    to retrieve the header of the 5 newest messages
    """
    service = get_service(auth_code)
    messages = (
        service
        .users()
        .messages()
        .list(userId="me", maxResults=5)
        .execute()
        )
    response = list()
    for item in messages["messages"]:
        response_item = {}
        message = (
            service
            .users()
            .messages()
            .get(userId="me", id=item["id"], format="metadata")
            .execute()
            )
        for header in message["payload"]["headers"]:
            if header["name"] == "From":
                response_item["from"] = header["value"]
            elif header["name"] == "Subject":
                response_item["subject"] = header["value"]
            else:
                continue
        response.append(response_item)
    return response


def set_watch(auth_code: str):
    service = get_service(auth_code)
    request = {
        'labelIds': ['INBOX'],
        'topicName': 'projects/alerts-304319/topics/ticket_alert'
        }
    response = service.users().watch(userId='me', body=request).execute()
    return response


def stop_watch(auth_code: str):
    service = get_service(auth_code)
    response = service.users().stop(userId='me').execute()
    return response
