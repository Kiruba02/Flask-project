from flask import *

from model import *

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

#bwith app.app_context():
   #if not Company.query.filter_by(company_name="Namma Kadai").first():
    #    com = Company(company_name="Namma Kadai", cash_balance=1000)
     #   db.session.add(com)
      #  db.session.commit()


@app.route('/create_item/', methods=['POST'])
def create_item():
    if request.method == 'POST':
        item_name = request.form['item_name']
        price = request.form['price']
        item = Item(item_name=item_name, price=price)
        db.session.add(item)
        db.session.commit()
        return redirect(url_for('dashboard'))


@app.route('/<int:item_id>/update_item/', methods=['POST'])
def update_item(item_id):
    item = Item.query.get_or_404(item_id)
    if request.method == 'POST':
        item_name = request.form['item_name']
        price = request.form['price']
        qty = request.form['quantity']
        item.item_name = item_name
        item.price = price
        item.qty = qty
        print(item_name,price,qty)
        db.session.add(item)
        db.session.commit()
        return redirect(url_for('dashboard'))


@app.route('/purchase_item/', methods=['POST'])
def purchase_item():
    company = Company.query.first()
    if request.method == 'POST':
        item_id = request.form['item_id']
        quantity = request.form['quantity']
        item = Item.query.get_or_404(item_id)
        amount = int(quantity) * int(item.price)
        if company.cash_balance > amount:
            purchase = Purchase(item_id=item_id, qty=quantity, rate=item.price, amount=amount)
            company.cash_balance = company.cash_balance - amount
            item.qty = int(item.qty) + int(quantity)
            db.session.add(item)
            db.session.add(company)
            db.session.add(purchase)
            db.session.commit()
        else:
            flash("Insufficient Cash")
        return redirect(url_for('dashboard'))


@app.route('/sale_item/', methods=['POST'])
def sale_item():
    company = Company.query.first()
    if request.method == 'POST':
        item_id = request.form['item_id']
        quantity = request.form['quantity']
        rate = request.form['rate']
        amount = int(quantity) * int(rate)
        item = Item.query.get_or_404(item_id)

        if item.qty >= int(quantity):
            sale = Sales(item_id=item_id, qty=quantity, rate=rate, amount=amount)
            company.cash_balance = company.cash_balance + amount
            item.qty = int(item.qty) - int(quantity)
            db.session.add(item)
            db.session.add(company)
            db.session.add(sale)
            db.session.commit()
        else:
            flash("Insufficient Quantity")
    return redirect(url_for('dashboard'))


@app.route('/')
def dashboard():
    company = Company.query.first()
    items = Item.query.all()
    purchases = Purchase.query.all()
    sales = Sales.query.all()
    return render_template('company/index.html', company=company, items=items, purchases=purchases, sales=sales)


if __name__ == '__main__':
    app.run()
