import os

from flask import Flask 
from flask import render_template
from flask import request, redirect

from twilio.rest import TwilioRestClient 

app = Flask(__name__) # Creating the Flask app
client = TwilioRestClient (os.environ['TWILIO_ACCOUNT_SID'], '0123')
twilio_number = os.environ['TWILIO_AUTH_TOKEN']

@app.route("/") # When you go to top page of app, this is what it will execute
def main():
    return render_template('form.html')
  
@app.route("/submit-form/", methods = ['POST']) 
def submit_number():
    number = request.form['number']
    formatted_number = "+1" + number # Switch to your country code of choice
    client.messages.create(to=formatted_number, from_ = twilio_number, body = "Message of your choice to text people.") # Replace body with your message of choice
    return redirect('/messages/')
  
@app.route("/messages/")
def list_messages():
    messages = client.messages.list(to=twilio_number)
    return render_template('messages.html', messages = messages)
    
    
if __name__ == '__main__': # If we're executing this app from the command line
    app.run("0.0.0.0", port = 3000, debug = True)