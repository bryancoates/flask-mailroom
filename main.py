""" Main application and page routing """

import os
import base64

from flask import Flask, render_template, request, redirect, url_for, session

from model import Donation, Donor

app = Flask(__name__)

@app.route('/')
def home():
    return redirect(url_for('all'))

@app.route('/donations/')
def all():
    donations = Donation.select()
    return render_template('donations.jinja2', donations=donations)

@app.route('/add_donation', methods=['GET', 'POST'])
def add_donation():
    """ Show page to add new donation or add new from form submission """

    if request.method == 'POST':
        # Get donor name from form, and query DB for donor
        donor_name = request.form['donor']
        donor = Donor.get(Donor.name == donor_name)

        # Create new donation for donor and amount from form
        donation = Donation(donor=donor.id, value=request.form['amount'])

        # Save new donation to the DB
        donation.save()

        # Redirect to homepage
        return redirect(url_for('home'))
    else:
        # Create list of donors to populate dropdown and show page
        donors = Donor.select()
        return render_template('add_donation.jinja2', donors=donors)
    
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 6738))
    app.run(host='0.0.0.0', port=port)
