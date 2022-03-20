from flask import Flask, request, redirect, url_for
from flask import render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Phone(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    brand = db.Column(db.String(32), nullable=False)
    model = db.Column(db.String(32), nullable=False)
    platform = db.Column(db.String(10), nullable=False)
    display = db.Column(db.Float)
    resolution = db.Column(db.String(16), nullable=False)
    battery = db.Column(db.Integer)

    cpu = db.Column(db.String(32), nullable=False)
    ram = db.Column(db.String(32), nullable=False)
    rom = db.Column(db.String(32), nullable=False)
    url = db.Column(db.String(256))
    description = db.Column(db.Text)
    price = db.Column(db.Integer)

    def __repr__(self):
        return '<Phone %r>' % self.id


@app.route('/edit', methods=['POST', 'GET'])
def create():
    if request.method == "POST":
        brand = request.form['brand']
        model = request.form['model']
        platform = request.form['platform']
        display = request.form['display']
        resolution = request.form['resolution']
        battery = request.form['battery']
        cpu = request.form['cpu']
        ram = request.form['ram']
        rom = request.form['rom']
        url = request.form['url']
        description = request.form['description']
        price = request.form['price']

        phone = Phone(brand=brand, model=model, platform=platform,
                      display=display, resolution=resolution, battery=battery,
                      cpu=cpu, ram=ram, rom=rom, url=url, description=description,
                      price=price)

        try:
            db.session.add(phone)
            db.session.commit()
            return redirect('/')
        except:
            return "При добавлении телефона произошла ошибка"
    else:
        return render_template("edit.html")


@app.route('/')
def index():
    phones = Phone.query.order_by(Phone.id).all()
    return render_template('index.html', items=phones)


@app.route('/edit')
def edit():
    return render_template('edit.html')


@app.route('/compare')
def compare():
    return render_template('compare.html')


if __name__ == '__main__':
    app.run(debug=True)
