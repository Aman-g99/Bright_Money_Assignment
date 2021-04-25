# brightMoney_assignment
 Plaid Assignment
 
### Make a Test Environment
virtualenv test
source test/bin/activate

### Install the requirement.txt
python3 install -r requirements.txt

Note: For some cases you need to install the requirements separately(installing the whole requirements.txt file doesn't work sometimes)

### Now migrate your database Model
python3 manage.py makemigrations
python3 manage.py migrate

### Add a superuser for admin portal
python3 manage.py createsuperuser

Note: It will ask for a username, email and password. This user credentials would be used to login in admin portal of the website.

### Now you are all set with your SQLITE db and dependencies installed on the test environment and can run the sever.
python3 manage.py runserver

### API's to hit
/admin : you can register a new individual here by adding user here.
/login : you can login using the credentials for the users made yet. After login, there will be a button to connect the user with the bank account.***
/logout : logout the user.
/account : fetch the account details for the logged in user and the connected account recognised by the access_token provided.
/transaction : fetch the transaction details for the access_token for the user.


*** Test Username for Plaid : user_good
*** Test Password for Plaid : pass_good
