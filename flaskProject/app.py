import flask_sqlalchemy
from flask import Flask, request, redirect, url_for
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import delete, select, update, values

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Phone(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    brand = db.Column(db.String(32), nullable=False)
    model = db.Column(db.String(32), nullable=False)
    platform = db.Column(db.String(10), nullable=False)
    type_display = db.Column(db.String(10), nullable=False)
    display = db.Column(db.Float, nullable=False)
    resolution = db.Column(db.String(16), nullable=False)
    battery = db.Column(db.Integer, nullable=False)
    cpu = db.Column(db.String(32), nullable=False)
    ram = db.Column(db.Integer, nullable=True)
    rom = db.Column(db.Integer, nullable=False)
    front = db.Column(db.String(32))
    back = db.Column(db.String(32))
    url = db.Column(db.String(256))
    description = db.Column(db.Text)
    year = db.Column(db.Integer, default=2022)
    price = db.Column(db.Integer)

    def __repr__(self):
        return '<Phone %r>' % self.id


def create_item(req):
    brand = request.form['brand']
    model = request.form['model']
    platform = request.form['platform']
    type_display = request.form['type_display']
    display = request.form['display']
    resolution = request.form['resolution']
    battery = request.form['battery']
    cpu = request.form['cpu']
    ram = request.form['ram']
    rom = request.form['rom']
    url = request.form['url']
    front = request.form['front']
    back = request.form['back']
    description = request.form['description']
    price = request.form['price']

    phone = Phone(brand=brand, model=model, platform=platform,
                  display=display, resolution=resolution, battery=battery, type_display=type_display,
                  cpu=cpu, ram=ram, rom=rom, url=url, description=description,
                  price=price, front=front, back=back)
    try:
        db.session.add(phone)
        db.session.commit()
    except Exception as e:
        print(e)
        return "При добавлении телефона произошла ошибка"


def remove_item(pos):
    try:
        script = delete(Phone).where(Phone.id == pos)
        db.session.execute(script)
        db.session.commit()
    except:
        return "При удалении позиции произошла ошибка"


CPU = {'Apple A15 Bionic': 35, 'Apple A14 Bionic': 32, 'Apple A13 Bionic': 30,
       'Apple A12 Bionic': 25, 'Apple A11 Bionic': 20, 'Apple A10 Fusion': 12,
       'Qualcomm Snapdragon 8 Gen 1': 33, 'Qualcomm Snapdragon 888': 29, 'Qualcomm Snapdragon 865': 27,
       'Qualcomm Snapdragon 855': 23, 'Qualcomm Snapdragon 845': 19, 'Qualcomm Snapdragon 835': 11,
       'Qualcomm Snapdragon 765 5G': 21,
       'Exynos 2200': 31, 'Exynos 990': 26, 'Exynos 9825': 21, 'Exynos 9810': 17}

LIFE_UPDATE = {'Google': 3, 'Samsung': 2, 'Apple': 6, 'Xiaomi': 2, 'Huawei': 2}


def difference(first, second):
    score_first = 0
    score_second = 0

    score_first += CPU[first.cpu]
    score_second += CPU[second.cpu]

    best_first = []
    bad_first = []

    best_second = []
    bad_second = []

    if first.battery > second.battery:
        score_first += 10
        best_first.append(f'Батарея: {first.battery} мАч')
        bad_second.append(f'Батарея: {second.battery} мАч')
    elif first.battery < second.battery:
        score_second += 10
        best_second.append(f'Батарея: {second.battery} мАч')
        bad_first.append(f'Батарея: {first.battery} мАч')

    if first.rom > second.rom:
        score_first += 5
        best_first.append(f'Хранилище: {first.rom} ГБ')
        bad_second.append(f'Хранилище: {second.rom} ГБ')
    elif first.rom < second.rom:
        score_second += 5
        best_second.append(f'Хранилище: {second.rom} ГБ')
        bad_first.append(f'Хранилище: {first.rom} ГБ')


    if first.ram > second.ram:
        score_first += 7
        best_first.append(f'Оперативная память: {first.ram} ГБ')
        bad_second.append(f'Оперативная память: {second.ram} ГБ')
    elif first.ram < second.ram:
        score_second += 7
        best_second.append(f'Оперативная память: {second.ram} ГБ')
        bad_first.append(f'Оперативная память: {first.ram} ГБ')

    if first.price > second.price:
        score_first -= 10
    elif first.price < second.price:
        score_second -= 10

    if first.display > second.display:
        score_first += 12
        best_first.append(f'Размер экрана: {first.display}"')
        bad_second.append(f'Размер экрана: {second.display}"')
    elif first.display < second.display:
        score_second += 12
        best_second.append(f'Размер экрана: {second.display}"')
        bad_first.append(f'Размер экрана: {first.display}"')

    res_first = max([int(i) for i in first.resolution.split('x')])
    res_second = max([int(i) for i in second.resolution.split('x')])

    if res_first > res_second:
        score_first += 12
        best_first.append(f'Разрешение экрана: {first.resolution}')
        bad_second.append(f'Разрешение экрана {second.resolution}')
    elif res_first < res_second:
        score_second += 12
        best_second.append(f'Разрешение экрана {second.resolution}')
        bad_first.append(f'Разрешение экрана: {first.resolution}')

    os_first = first.platform
    os_second = second.platform

    # if os_first == os_second:
    #     if ver_first > ver_second:
    #         score_first += 8
    #     elif ver_first < ver_second:
    #         score_second += 8

    last_update_first = int(first.year) + LIFE_UPDATE[first.brand]
    last_update_second = int(second.year) + LIFE_UPDATE[second.brand]
    if last_update_first > last_update_second:
        score_first += 8
        best_first.append(f'Система: {first.platform} (обновление до {last_update_first} г.)')
        bad_second.append(f'Система: {second.platform} (обновление до {last_update_second} г.)')
    elif last_update_first < last_update_second:
        score_second += 8
        best_second.append(f'Система: {second.platform} (обновление до {last_update_second} г.)')
        bad_first.append(f'Система: {first.platform} (обновление до {last_update_first} г.)')

    if score_first > score_second:
        return first.id, best_first, second.id, bad_second
    elif score_first < score_second:
        return second.id, best_second, first.id, bad_first


@app.route('/edit', methods=['POST', 'GET'])
def create():
    if request.method == "POST":
        create_item(request)
        return redirect('/')
    else:
        return render_template("edit.html")


@app.route('/')
def index():
    phones = Phone.query.order_by(Phone.id).all()
    return render_template('index.html', items=phones)


@app.route('/edit')
def edit():
    return render_template('edit.html')


@app.route('/compare', methods=['GET', 'POST'])
def compare():
    phones = Phone.query.order_by(Phone.id).all()
    if request.method == 'POST':
        result = []
        first = request.form.get('first')
        second = request.form.get('second')
        if first.isdigit() and second.isdigit():
            first = phones[int(first) - 1]
            second = phones[int(second) - 1]
            if first.id != second.id:
                result = difference(first, second)
                win = result[0], result[1]
                lose = result[2], result[3]
                return render_template('compare.html', phones=phones, winner=win, looser=lose)
    return render_template('compare.html', phones=phones, comp=(-1, []))


if __name__ == '__main__':
    app.run(debug=True)
