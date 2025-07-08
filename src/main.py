from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)

# Configure the PostgreSQL database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://hotel_user:password@172.16.25.167/hotel_management'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Meal model
class Meal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    category = db.Column(db.String(50), nullable=False)  # New column

# Order model
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(200), nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    payment_method = db.Column(db.String(50), nullable=False)
    total_price = db.Column(db.Integer, nullable=False)

# Routes
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/breakfast')
def breakfast():
    meals = Meal.query.filter(Meal.name.ilike('%breakfast%')).all()
    return render_template('breakfast.html', meals=meals)

@app.route('/lunch')
def lunch():
    meals = Meal.query.filter(Meal.name.ilike('%lunch%')).all()
    return render_template('lunch.html', meals=meals)

@app.route('/supper')
def supper():
    meals = Meal.query.filter(Meal.name.ilike('%supper%')).all()
    return render_template('supper.html', meals=meals)

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if request.method == 'POST':
        location = request.form['location']
        phone = request.form['phone']
        payment_method = request.form['payment-method']
        selected_meal_ids = request.form.getlist('meal_ids')  # Get selected meal IDs

        # Calculate total price on the backend
        selected_meals = Meal.query.filter(Meal.id.in_(selected_meal_ids)).all()
        total_price = sum(meal.price for meal in selected_meals)

        # Save the order to the database
        new_order = Order(location=location, phone=phone, payment_method=payment_method, total_price=total_price)
        db.session.add(new_order)
        db.session.commit()

        return redirect(url_for('home'))

    # Pass selected meals to the template for rendering
    selected_meals = Meal.query.all()  # Replace this with actual selected meals logic
    return render_template('checkout.html', selected_meals=selected_meals)

if __name__ == '__main__':
    # Create the database tables
    with app.app_context():
        db.create_all()

    app.run(debug=True, host='0.0.0.0')
