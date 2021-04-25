from plaid_app.celery import app
from plaid_app.plaid_setting import get_transaction, get_account, plaid
import datetime
from plaid_app.models import Account, Transaction 

@app.task
def update_account(user_id, item_id, access_token):
    try:
        accounts_response = get_account(access_token)
        print(accounts_response)
        for i in accounts_response['accounts']:
            account_id = i.get('account_id')
            info = str(i)
            acc = Account(user_id=user_id, info=info, account_id=account_id)
            acc.save()

    except plaid.errors.PlaidError as e:
        pass



@app.task
def update_transaction(user_id, item_id, access_token):
    start_date = '{:%Y-%m-%d}'.format(datetime.datetime.now() + datetime.timedelta(-30))
    end_date = '{:%Y-%m-%d}'.format(datetime.datetime.now())
    try:
        transactions_response = get_transaction(access_token, start_date, end_date)
        for i in transactions_response['transactions']:
            account_id = i.get('account_id')
            trans_id = i.get('transaction_id')
            info = str(i)
            acc = Transaction(user_id=user_id, info=info, account_id=account_id, transaction_id= trans_id)
            acc.save()
        
    except plaid.errors.PlaidError as e:
        pass
    

