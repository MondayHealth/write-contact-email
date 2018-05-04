import datetime
import os

from apiclient import discovery
# noinspection PyPackageRequirements
from google.oauth2 import service_account
from pytz import timezone

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = os.path.abspath('./s_private_key.json')
TIMEZONE = "US/Eastern"


def service():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """

    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    return discovery.build('sheets', 'v4', credentials=credentials)


def add_values(values: tuple):
    spreadsheet_id = '1jvRLg9XgmK7TVjE-EsvXfu7_uIYKtqMCMYUkpd9kAl0'

    # The A1 notation of a range to search for a logical table of data.
    # Values will be appended after the last row of the table.
    range_ = 'A1:' + chr(ord('a') + len(values)).upper() + '1'

    value_range_body = {
        "majorDimension": "ROWS",
        "range": range_,
        "values": [values]
    }

    request = service().spreadsheets().values().append(
        spreadsheetId=spreadsheet_id,
        range=range_,
        valueInputOption='RAW',
        body=value_range_body)

    return request.execute()


def _error(reason: str) -> dict:
    return {"success": False, "reason": reason}


def lambda_entry(params: dict, context):
    if 'content' not in params:
        return _error("no content object")

    content = params['content']

    if 'email' not in content:
        return _error("no email in content")

    email = content['email']

    tz = timezone(TIMEZONE)
    now: datetime.datetime = datetime.datetime.now(tz)
    date = "{0:%m/%d/%Y %H:%M:%S}".format(now)
    print(date)
    values = (date, email)

    add_values(values)

    return {'success': True}


def command_line():
    result: str = lambda_entry({'content': {'email': 'test@test.com'}}, None)
    print(result)


if __name__ == '__main__':
    command_line()
