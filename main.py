import requests
from requests import RequestException
from msal import ClientApplication


class Config:
    def __init__(self, username, password, client_id, authority):
        self.username = username
        self.password = password
        self.client_id = client_id
        self.authority = authority
        self.subject = 'Ticket Master Password Reset'


def get_email_messages(config):

    try:

        app = ClientApplication(client_id=config.client_id,
                                authority=config.authority)

        token = app.acquire_token_by_username_password(username=config.username, password=config.password,
                                                       scopes=['.default'])

        headers = {"Authorization": f"Bearer {token.get('access_token')}"}

        # filter the most recent email.
        params = {"$search": f'"subject:{config.subject}"',
                  "top": 1}

        response = requests.get(url='https://graph.microsoft.com/v1.0/me/messages',
                                headers=headers,
                                params=params)
        return response.json()
    except RequestException as re:
        print(f" Exception while getting email messages : {re} ")


if __name__ == '__main__':
    username = "aznprinze2k@hotmail.com"
    password = "okfrVFb1!"
    client_id = '<your-client-id>'
    authority = '<your-authority-url>'

    config = Config(username=username, password=password, client_id=client_id, authority=authority)
    result = get_email_messages(config)
    print(result)