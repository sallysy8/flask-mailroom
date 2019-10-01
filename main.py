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
    donations = Donation.select().order_by(Donation.donor.asc())
    return render_template('donations.jinja2', donations=donations)


@app.route('/createDonation', methods=['GET', 'POST'])
def createDonation():
    if request.method == 'GET':
        return render_template('createDonation.jinja2')
    else:
        # must be post
        requestDonorName = request.form['name']
        donor, created = Donor.get_or_create(name=requestDonorName)
        entry = Donation(donor=donor, value=float(request.form['amount']))
        entry.save()
        return redirect(url_for('all'))


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 6738))
    app.run(host='0.0.0.0', port=port)
