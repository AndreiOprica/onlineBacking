from flask import Flask, render_template, request, flash
import json
import os.path

app = Flask(__name__)
app.secret_key = 'kbcaskkcnlfa56sfg651f1v5s6sdfafd1'

acc_num_global = {}


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/new-user')
def new_user():
    return render_template('new_user.html')


@app.route('/existing-user')
def existing_user():
    return render_template('existing_user.html')


@app.route('/customer-details', methods=['GET','POST'])
def customer_details():
    if request.method=='POST':
        login={}
        if os.path.exists('login.json'):
            with open('login.json') as login_file:
                login=json.load(login_file)
        if request.form['type'] == 'new':
            login[request.form['name']] = request.form['password']
            with open('login.json','w') as login_file:
                json.dump(login,login_file)
        if request.form['type'] == 'existing':
            if request.form['name'] not in login:
                flash('Access Denied!!')
                flash('Incorrect Username')
                return render_template('existing_user.html')
            if login[request.form['name']] != request.form['password']:
                flash('Access Denied!!')
                flash('Incorrect Password')
                return render_template('existing_user.html')
        return render_template('customer_details.html',name=request.form['name'])
    else:
        return render_template('home.html')


@app.route('/new-customer')
def new_customer():
    return render_template('new_customer.html')


@app.route('/existing-customer')
def existing_customer():
    return render_template('existing_customer.html')


@app.route('/transaction', methods=['GET','POST'])
def transaction():
    global acc_num_global
    if request.method=='POST':
        accounts={}
        if os.path.exists('accounts.json'):
            with open('accounts.json') as accounts_file:
                accounts=json.load(accounts_file)
        if request.form['type'] == 'new':
            accounts[request.form['acc_num']] = {'name' : request.form['name'],
                                                 'number' : request.form['acc_num'], 'balance' : request.form['balance']}
            with open('accounts.json','w') as accounts_file:
                json.dump(accounts,accounts_file)
        if request.form['type'] == 'existing':
            if request.form['acc_num'] not in accounts:
                flash('Access Denied!!')
                flash('Incorrect Account Number')
                return render_template('existing_customer.html')
        acc_num_global = request.form['acc_num']
        return render_template('transaction.html',name=accounts[acc_num_global]['name'],
                               number=accounts[acc_num_global]['number'],balance=accounts[acc_num_global]['balance'])
    else:
        return render_template('home.html')


@app.route('/transactions', methods=['GET','POST'])
def transactions():
    global acc_num_global
    if request.method == 'POST':
        accounts = {}
        if os.path.exists('accounts.json'):
            with open('accounts.json','r') as accounts_file:
                accounts = json.load(accounts_file)
        if request.form['option']=='deposit':
            accounts[acc_num_global]['balance'] = str(int(accounts[acc_num_global]['balance']) + int(request.form['amount']))
            flash('TRANSACTION SUCCESSFUL!!')
            flash('Amount Deposited: ' + str(request.form['amount']) + ' EURO')
        if request.form['option']=='withdraw':
            if (int(accounts[acc_num_global]['balance']) - int(request.form['amount'])) > 0:
                accounts[acc_num_global]['balance'] = str(int(accounts[acc_num_global]['balance']) - int(request.form['amount']))
                flash('TRANSACTION SUCCESSFUL!!')
                flash('Amount Withdrawn: ' + str(request.form['amount']) + ' EURO')
            else:
                flash('TRANSACTION FAILED!!')
                flash('Insufficient Balance')
        with open('accounts.json','w') as accounts_file:
            json.dump(accounts,accounts_file)
        return render_template('transaction.html', name=accounts[acc_num_global]['name'],
                               number=accounts[acc_num_global]['number'], balance=accounts[acc_num_global]['balance'])
    else:
        return render_template('home.html')


app.run(port=7000)
