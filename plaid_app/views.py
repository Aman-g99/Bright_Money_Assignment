from django.views.generic import FormView, TemplateView
from django.http import (HttpResponse, HttpResponseRedirect, HttpResponseForbidden, Http404, HttpResponseBadRequest,
    QueryDict, JsonResponse)
from django.contrib.auth.models import User
from plaid_app.models import Account, Transaction, Item_table
from .palid_task import update_account, update_transaction
# from celery import app as celery_app
from plaid_app.plaid_setting import get_exchange_token, get_link_token, get_account, get_transaction

# import plaid
# from django.conf import settings

# client = plaid.Client(client_id=settings.PLAID_CLIENT_ID,
#                       secret=settings.PLAID_SECRET,
#                       environment=settings.PLAID_ENV,
#                       api_version='2019-05-29')



def format_error(e):
  return {'error': {'display_message': e.display_message, 'error_code': e.code, 'error_type': e.type, 'error_message': e.message } }


class Bmplaid(TemplateView):
    
    def post(self, request):
        if not request.user.is_authenticated:
            return HttpResponse('Unauthorized', status=401)
        # user = User.find(...)
        client_user_id = request.user.id    #user.id
        # Create a link_token for the given user
        response = get_link_token(client_user_id)
        print(response)
        link_token = response['link_token']
        return  HttpResponse(link_token) #JsonResponse(response)


    

class link_page(TemplateView):
    
    template_name = 'plaid_form.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return HttpResponseRedirect("/login/")
        return super().get(request)
    
    def post(self, request):
        public_token = request.POST['public_token']
        exchange_response, is_err = get_exchange_token(public_token)
        if is_err:
            return JsonResponse(exchange_response)
        # pretty_print_response(exchange_response)
        print(exchange_response)
        access_token = exchange_response['access_token']
        item_id = exchange_response['item_id']
        request.session['access_token'] = access_token
        request.session['item_id'] = item_id
        acc_user = Item_table(user_id=request.user.id, item_id= item_id, access_token=access_token)
        acc_user.save()
        update_account.delay(request.user.id, item_id, access_token)
        update_transaction.delay(request.user.id, item_id, access_token)
        return JsonResponse(exchange_response)
    

class AccountHandler(TemplateView):
    
    def get(self,request):
        # access_tokens = Item_table.objects.raw('SELECT access_token from plaid_app_item_table where user_id = 2')
        access_tokens = Item_table.objects.filter(user_id=request.user.id)
        access_token = access_tokens[0].access_token
        
        # access_token = select access_token from Item_table where user_id = request.user.id;
        # try:
        accounts_response = get_account(access_token)
        # except plaid.errors.PlaidError as e:
        #     console.log
        #     # return jsonify({'error': {'display_message': e.display_message, 'error_code': e.code, 'error_type': e.type } })
        # pretty_print_response(accounts_response)
        print(accounts_response)
        return JsonResponse(accounts_response)
        # return jsonify({'error': None, 'accounts': accounts_response})

    def post(self, request):
        if not request.user.is_authenticated:
            return HttpResponseBadRequest()
        # import ipdb; ipdb.set_trace()

        data = Account.objects.filter(user_id=request.user.id)
        return JsonResponse(data)

class TransactionHandler(TemplateView):

    def get(self,request):
        access_tokens = Item_table.objects.filter(user_id=request.user.id)
        access_token = access_tokens[0].access_token
        transaction_response = get_transaction(access_token,start_date='2018-01-01',end_date='2018-02-01')
        print(transaction_response)
        return JsonResponse(transaction_response)
        # return jsonify({'error': None, 'accounts': accounts_response})

    
    def post(self, request):
        if not request.user.is_authenticated:
            return HttpResponseBadRequest()
        # import ipdb; ipdb.set_trace()
        
        data = Transaction.objects.filter(user_id=request.user.id)
        return JsonResponse(data)
    

    
