from flask import Flask, request, jsonify
from flask_cors import CORS
from user import User
from userService import UserService
from bookService import BookService
from book import Book
from issue import Issue
from issueService import IssueService
from defaulterService import DefaultService
from defaulter import Defaulter
import stripe

app = Flask(__name__)

CORS(app)

stripe.api_key = 'sk_test_51NTPZSKPLgEWMpSqM2d8MJgzZc4b3aFlajWa8bDdSiTUDfxo0pe2WDVCVGjL7yLuZ7WmyexwMqhT3UZtVW8kUMMH00asHEQLgx'

@app.route('/fine', methods=['POST'])
def fine_payment():
    try:
        body = request.json
        fine = body['fine']
        email = body['email']

        payment_intent = stripe.PaymentIntent.create(
            amount = fine,
            currency = 'gbp',
            receipt_email = email
        )

        return jsonify({"secret": payment_intent['client_secret']}), 200
    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500
    
@app.route('/subscribe', methods = ['POST'])
def subscribe():
    body = request.json

    member = stripe.Customer.create(
        payment_method = body['payment_method'],
        email = body['email'],
        invoice_settings = {
            'default_payment_method': body['payment_method']
        },
    )

    subscription = stripe.Subscription.create(
        customer = member['id'],
        items = [
            {
                'plan': 'price_1NUZV2KPLgEWMpSqzopeSBhB',
            },
        ],
        expand = ['latest_invoice.payment_intent'],
    )

    status = subscription['latest_invoice']['payment_intent']['status']
    client_secret = subscription['latest_invoice']['payment_intent']['client_secret']

    print(status, client_secret)

    return jsonify({
        'status': status,
        'client_secret': client_secret
    })

@app.route("/register", methods = ['POST'])
def register_members():
    body = request.json

    user = User(body['firstname'], body['lastname'], body['email'], body['password'], "member")
    userservice = UserService()

    added_member = userservice.register(user.get_user())

    if added_member:
        return jsonify({
        "memberid": str(added_member.inserted_id),
        "email": body['email'],
        "role": 'member',
        "message": "New member added"
    })

    return jsonify({
        'message': 'User already exists'
    }), 400
    

@app.route("/login", methods = ['POST', 'GET'])
def login_users():
    userservice = UserService()
    if request.method == 'POST':
        body = request.json
        email = body['email']
        password = body['password']

        user = userservice.login(email, password)

        if user:
            return jsonify({
                'id': str(user['_id']),
                'email': user['email'],
                'role': user['role'],
                'message': 'Login successful!'
            })
        return jsonify({
            'message': 'Invalid credentials!'
        }), 400
    
    if request.method == 'GET':
        allMembers = userservice.get_all_members()
        return jsonify(allMembers)

@app.route('/resetpassword', methods=['PUT'])
def reset_password():
    userservice = UserService()
    body = request.json
    resp = userservice.reset_password(body['email'], body['newpassword'])
    if resp:
        return jsonify({
            'message': 'Password reset successful!'
        })
    return jsonify({
        'message': 'User does not exist! Please Subscribe!'
    })

@app.route("/books", methods = ['POST', 'GET'])
def books():
    bookservice = BookService()
    if request.method == 'POST':
        body = request.json
        
        book = Book(body['title'], body['author'], body['isbn13'], body['s_loc'], body['qty'])
        existingbook = bookservice.get_book(body['isbn13'])

        if existingbook:
            return jsonify({
            'message': 'Book entry already exists'
        }), 400
        
        added_book = bookservice.new_book(book.get_book())

        if added_book:
            return jsonify({
                'bookId': str(added_book.inserted_id),
                'message': 'New book added'
            })
    
    if request.method == 'GET':
        allbooks = bookservice.get_all_books()
        return jsonify(allbooks)
    
@app.route("/books/<string:id>", methods = ['GET', 'PUT', 'DELETE'])
def onebook(id):
    bookservice = BookService()
    if request.method == 'GET':
        book = bookservice.get_book_by_id(id)
        if book:
            return jsonify({
                    'id': id,
                    'title': book['title'],
                    'author': book['author'],
                    'isbn13': book['isbn13'],
                    's_loc': book['shelfloc'],
                    'qty': book['quantity']
                })
        return jsonify({
            'message': 'Wrong query!',
        })
        
    if request.method == 'PUT':
        body = request.json
        existingbook = bookservice.get_book_by_id(id)

        if existingbook:
            book = Book(body['title'], body['author'], body['isbn13'], body['s_loc'], body['qty'])
            bookservice.update_book(book.get_book(), id)
            return jsonify({
                'message': 'Book entry updated'
            })
        
        return jsonify({
            'message': 'Book entry not found.'
        }), 400
    
    if request.method == 'DELETE':
        existingbook = bookservice.get_book_by_id(id)
        if existingbook:
            bookservice.remove_book(id)
            return jsonify({
                'message': 'Book deleted.'
            })
        return jsonify({
            'message': 'Book not found!'
        })
    
@app.route("/issues", methods=['POST', 'GET'])
def book_issues():
    issueservice = IssueService()
    if request.method == 'POST':
        body = request.json
        bookservice = BookService()
        new_issue = Issue(body['book'], body['member'], body['idate'], body['rdate'], '', "pending")

        book = bookservice.get_book(body['book'])
        existing_issue = issueservice.get_issue(body['member'])

        if existing_issue:
            return jsonify({'message': 'Member might not have returned previous issued book or paid dues.'}), 400
        
        if book:
            if (book['quantity'] != 0):
                added_issue = issueservice.add_new_issue(new_issue.get_issue())
                return jsonify({
                    'issue_id': str(added_issue.inserted_id),
                    'book': str(book['_id']),
                    'message': 'New issue added'
                })
            else:
                return jsonify({
                    'message': 'This book is not currently available'
                }), 400
        else:
            return jsonify({
                'message': 'Book is not present!'
            }), 400
        
    if request.method == 'GET':
        allissues = issueservice.get_all_issues()
        return jsonify(allissues)
    
@app.route("/issues/<string:id>", methods=['PUT'])
def one_book_issue(id):
    issueservice = IssueService()

    if request.method == 'PUT':
        body = request.json
        existingissue = issueservice.get_issue_by_id(id)
        bookservice = BookService()
        book = bookservice.get_book(body['book'])
        if existingissue:
            issue = Issue(body['book'], body['member'], body['idate'], body['rdate'], body['actret'], body['status'])
            issueservice.update_issue(issue.get_issue(), id)
            return jsonify({
                'book': str(book['_id']),
                'message': 'Issue entry updated'
            })
        
        return jsonify({
            'message': 'Issue entry not found.'
        }), 400
    
@app.route('/generatereport', methods=['GET'])
def generate_report():
    issueservice = IssueService()
    startdate = request.args.get('startdate')
    enddate = request.args.get('enddate')
    reportData = issueservice.generate_report(startdate, enddate)
    return jsonify(reportData)

@app.route('/defaulter', methods=['POST', 'GET']) 
def defaulter():
    defaultservice = DefaultService()
    if request.method == 'POST':
        body = request.json

        existingdefaulter = defaultservice.get_defaulter(body['member'])
        defaulter = Defaulter(body['member'], body['dues'], body['status'])
        if body['dues'] == 0:
            return jsonify({
                'message':'No dues to add'
                })
        if existingdefaulter:
            defaultservice.update_defaulter(defaulter.get_defaulter(), str(existingdefaulter['_id']))
            return jsonify({
                'message': 'Due updated'
            })
        added_defaulter = defaultservice.new_defaulter(defaulter.get_defaulter())
        return jsonify({
            'id': str(added_defaulter.inserted_id),
            'message': 'Defaulter added'
        })
    
    if request.method == 'GET':
        alldef = defaultservice.get_all_defaulters()
        return jsonify(alldef)
    
@app.route('/defaulter/<string:id>', methods=['PUT'])
def one_defaulter(id):
    defaultservice = DefaultService()
    body = request.json
    existingdef = defaultservice.get_defaulter_by_id(id)
    if existingdef:
        updateddef = Defaulter(body['member'], body['dues'], body['status'])
        defaultservice.update_defaulter(updateddef.get_defaulter(), id)
        return jsonify({
            'message': 'Defaulter updated'
        })
    return jsonify({
        'message': 'Entry not found'
    }), 400

if __name__ == "__main__":
    app.run(debug=True)