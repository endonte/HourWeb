from flask import Flask, render_template
from flask_script import Manager
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Required, Length
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand


app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
app.config['SQLALCHEMY_DATABASE_URI'] =\
    'postgresql://donald:Iceman123+@localhost/hourdb'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

manager = Manager(app)
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Quote_Details(db.Model):
    __tablename__ = 'quote'
    id = db.Column(db.Integer, primary_key = True)
    customer = db.Column(db.String(64))
    company = db.Column(db.String(64), nullable = True)
    regno = db.Column(db.String(64), nullable = True)
    ship_address1 = db.Column(db.String(40))
    ship_address2 = db.Column(db.String(40))
    ship_postal = db.Column(db.String(6))
    bill_address1 = db.Column(db.String(64), nullable = True)
    bill_address2 = db.Column(db.String(64), nullable = True)
    bill_postal = db.Column(db.String(6), nullable = True)

class Quote_Form(FlaskForm):
    customer = StringField('Customer Name:', validators=[Required()])
    company = StringField('Company Name:')
    regno = StringField('Business Registration No.:')
    ship_address1 = StringField('Delivery Address Line 1', validators=[Required()])
    ship_address2 = StringField('Delivery Address Line 2', validators=[Required()])
    ship_postal = StringField('Delivery Postal Code', validators=[Length(6, 6, 'Please enter 6 digits only')])
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
	if form.validate_on_submit():
		Quotation = Quote_Details(
			customer = form.customer.data,
			company = form.company.data,
			regno = form.regno.data,
			ship_address1 = form.ship_address1.data,
			ship_address2 = form.ship_address2.data,
			ship_postal = form.ship_postal.data,
			bill_address1 = form.bill_address1.data,
			bill_address2 = form.bill_address2.data,
			bill_postal = form.bill_postal.data
		)
		db.session.add(Quotation)
		return render_template('quote_template.html', form=form, Quotation=Quotation)
    
	return render_template('hourweb.html', form=form)

if __name__ == '__main__':
    manager.run()
