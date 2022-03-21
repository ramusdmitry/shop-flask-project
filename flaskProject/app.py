from flask import Flask, request, redirect, url_for
from flask import render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

<<<<<<< HEAD
CPU = {'A15': 20, 'A14': 18, 'A13': 16, 'A12': 14,
       '888': 18, '865': 16, '855': 14, '845': 12,
       '2200': 18, '2100': 16, '990': 12, '9810': 10}

=======
>>>>>>> 34626e1d73ceaa2e62665055d154baa60e524d42

class Phone(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    brand = db.Column(db.String(32), nullable=False)
    model = db.Column(db.String(32), nullable=False)
    platform = db.Column(db.String(10), nullable=False)
    display = db.Column(db.Float)
    resolution = db.Column(db.String(16), nullable=False)
    battery = db.Column(db.Integer)
<<<<<<< HEAD
    cpu = db.Column(db.String(32), nullable=False)
    ram = db.Column(db.Integer, nullable=False)
    rom = db.Column(db.Integer, nullable=False)
    front = db.Column(db.String(32))
    back = db.Column(db.String(32))
=======

    cpu = db.Column(db.String(32), nullable=False)
    ram = db.Column(db.String(32), nullable=False)
    rom = db.Column(db.String(32), nullable=False)
>>>>>>> 34626e1d73ceaa2e62665055d154baa60e524d42
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
<<<<<<< HEAD
        front = request.form['front']
        back = request.form['back']
=======
>>>>>>> 34626e1d73ceaa2e62665055d154baa60e524d42
        description = request.form['description']
        price = request.form['price']

        phone = Phone(brand=brand, model=model, platform=platform,
                      display=display, resolution=resolution, battery=battery,
                      cpu=cpu, ram=ram, rom=rom, url=url, description=description,
<<<<<<< HEAD
                      price=price, front=front, back=back)
=======
                      price=price)

>>>>>>> 34626e1d73ceaa2e62665055d154baa60e524d42
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


<<<<<<< HEAD
@app.route('/compare', methods=['GET', 'POST'])
def compare():
    phones = Phone.query.order_by(Phone.id).all()
    # if request.method == 'POST':
    #     first = request.form.get('first')
    #     second = request.form.get('second')
    #     if first.isdigit() and second.isdigit():
    #         pos_first = int(first)
    #         pos_second = int(second)
    #         first = phones[pos_first]
    #         second = phones[pos_second]
    #         if first != second:
    #             device, diff = compare_devices(first, second)
    #             return render_template('compare.html', phones=phones, device=device)

    return render_template('compare.html', phones=phones)


def compare_devices(first, second):
    first_score = 0
    second_score = 0

    first_best = {'cpu': None, 'ram': None, 'rom': None, 'battery': None,
                  'resolution': None, 'price': None}
    second_best = {'cpu': None, 'ram': None, 'rom': None, 'battery': None,
                   'resolution': None, 'price': None}

    if first.ram < second.ram:
        second_score += 7
        second_best['ram'] = True
    elif first.ram > second.ram:
        first_score += 7
        first_best['ram'] = True

    if first.rom < second.rom:
        second_score += 5
        second_best['rom'] = True
    elif first.rom > second.rom:
        first_score += 5
        first_best['rom'] = True

    if first.battery < second.battery:
        second_score += 8
        second_best['battery'] = True
    elif first.battery > second.battery:
        first_score += 8
        first_best['battery'] = True

    first_cpu = 0
    second_cpu = 0
    for k, v in CPU.items():
        if k in first.cpu:
            first_cpu = CPU[k]
        if k in second.cpu:
            second_cpu = CPU[k]

    if first_cpu < second_cpu:
        second_score += second_cpu
        second_best['cpu'] = True
    elif first_cpu > second_cpu:
        first_score += first_cpu
        first_best['cpu'] = True

    if first.resolution < second.resolution:
        second_score += 9
        second_best['resolution'] = True

    elif first.resolution > second.resolution:
        first_score += 9
        first_best['resolution'] = True

    if first.price < second.price:
        first_score += 12
        first_best['price'] = True
    elif first.price > second.price:
        second_score += 12
        second_best['price'] = True

    if first_score > second_score:
        return first, first_best
    else:
        return second, second_best
=======
@app.route('/compare')
def compare():
    return render_template('compare.html')
>>>>>>> 34626e1d73ceaa2e62665055d154baa60e524d42


if __name__ == '__main__':
    app.run(debug=True)
