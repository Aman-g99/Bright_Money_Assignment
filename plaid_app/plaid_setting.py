import plaid
from django.conf import settings

client = plaid.Client(client_id=settings.PLAID_CLIENT_ID,
                      secret=settings.PLAID_SECRET,
                      environment=settings.PLAID_ENV,
                      api_version='2019-05-29')


def format_error(e):

  return {'error': {'display_message': e.display_message, 'error_code': e.code, 'error_type': e.type, 'error_message': e.message }}


def get_link_token(client_user_id):
    resp = client.LinkToken.create({
            'user': {
                'client_user_id': str(client_user_id),
            },
            'products': ['transactions'],
            'client_name': 'bm_code',
            'country_codes': ['US'],
            'language': 'en',
            'webhook': 'https://webhook.sample.com',
        })
    return resp


def get_exchange_token(public_token):
    try:
            exchange_response = client.Item.public_token.exchange(public_token)
    except plaid.errors.PlaidError as e:
        return format_error(e), True
    return exchange_response, False

def get_transaction(access_token, start_date, end_date):
    transactions_response = client.Transactions.get(access_token, start_date, end_date)
    return transactions_response

def get_account(access_token):
    return client.Accounts.get(access_token)
