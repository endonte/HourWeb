from flask import Flask, render_template
from flask_script import Manager
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Required

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
manager = Manager(app)
bootstrap = Bootstrap(app)

class Quote_Form(FlaskForm):
    customer = StringField('Customer Name:', validators=[Required()])
    company = StringField('Company Name:')
    regno = StringField('Business Registration No.:')
    ship_address1 = StringField('Delivery Address Line 1')
    ship_address2 = StringField('Delivery Address Line 2')
	ship_postal = StringField('Delivery Postal Code')
    bill_address1 = StringField('Billing Address Line 1')
    bill_address2 = StringField('Billing Address Line 2')
	bill_postal = StringField('Billing Postal Code')
    
    create = SubmitField('Create Quote')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/products')
def products():
    return render_template('products.html')

@app.route('/pricing')
def pricing():
    return render_template('pricing.html')

@app.route('/support')
def support():
    return render_template('support.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/hourweb', methods=['GET', 'POST'])
def hourweb():
    form = Quote_Form()
    return render_template('hourweb.html', form=form)

if __name__ == '__main__':
    manager.run()
