from flask import Flask, request, render_template,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, LargeBinary
from io import BytesIO
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///Stock.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class myStock(db.Model):
    sno = db.Column(db.Integer,primary_key = True)
    product = db.Column(db.String(200),nullable = False)
    price = db.Column(db.String(200),nullable = False)
    link = db.Column(db.String(200),nullable = False)
    image_link = db.Column(db.String(200),nullable = False)
    
    

db.create_all()
@app.route('/', methods = ['POST', 'GET'])
def hello():
    all_products =  myStock.query.all()
    return render_template('index.html',all_products=all_products)

@app.route('/admin', methods = ['POST', 'GET'])
def admin():
    
    if request.method == 'POST':
        product_name = request.form['product_name']
        price = request.form['price']
        link = request.form['link']
        image_link = request.form['image_link']
    
        final_Upload = myStock(product=product_name,price=price,link=link,image_link=image_link)

        db.session.add(final_Upload)
        db.session.commit()
        # redirect the user to the same route with a GET request to avoid form resubmission
        return redirect(url_for('admin'))

    all_products =  myStock.query.all()

    return render_template('admin.html',all_products=all_products)

@app.route('/delete/<int:sno>/')
def delete(sno):
    stock = myStock.query.filter_by(sno=sno).first()
    db.session.delete(stock)
    db.session.commit()
    return redirect('/admin')
if __name__ =='__main__':
    app.run(debug=True)