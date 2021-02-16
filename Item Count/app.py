import numpy as np
import copy
import pickle
import os
import requests
from os import listdir, remove
from os.path import isfile, join
from flask import Flask, render_template, url_for, request, flash
import func
from OpenSSL import SSL



UPLOAD_FOLDER = '/path/to/the/uploads'
ALLOWED_EXTENSIONS = {'xls'}

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'the random string'

func.setup()

working_path = "telling/year/2020/"
working_shelves = [f for f in listdir(working_path) if isfile(join(working_path, f))]

done_path = "oversikt/year/2020/"
done_shelves = [f for f in listdir(done_path) if isfile(join(done_path, f))]

ferdig_path = "ferdig/"
ferdig_shelves = [f for f in listdir(ferdig_path) if isfile(join(ferdig_path, f))]

dictionary = np.load('my_file.npy', allow_pickle='TRUE').item()

@app.route('/')
def main():
    return render_template("home.html")

@app.route('/overview')
def overview():
    done_shelves = [f for f in listdir(done_path) if isfile(join(done_path, f))]
    return render_template("overview.html", len = len(done_shelves), shelves = done_shelves)

@app.route('/overview/<shelf>')
def view_shelf(shelf):
    liste = []
    try:
        with open("oversikt/year/2020/" + shelf, "r") as file:
            for i, line in enumerate(file):
                if len(line) <= 4:
                    continue
                liste.append(line.split("@"))
    except:
        with open("ferdig/" + shelf, "r") as file:
            for i, line in enumerate(file):
                if len(line) <= 4:
                    continue
                liste.append(line.split("@"))

    return render_template("view_shelf.html", file = liste, len = len(liste), shelf=shelf)

@app.route('/counting', methods=["GET", "POST"])
def counting():
    working_shelves = [f for f in listdir(working_path) if isfile(join(working_path, f))]
    done_shelves = [f for f in listdir(done_path) if isfile(join(done_path, f))]
    ferdig_shelves = [f for f in listdir(ferdig_path) if isfile(join(ferdig_path, f))]
    symbols = "%#&{}|\ <>*?/$!':;@+-="+'"'
    for _, value in request.form.items():
        for j in range(len(symbols)):
            value = value.strip(symbols[j])
        if value.split(".")[0].lower() != value.lower():
            break
        if (value.strip(" ").replace(" ", "_").lower() + ".txt") not in done_shelves and (value.strip(" ").replace(" ", "_").lower() + ".txt") not in working_shelves and (value.strip(" ").replace(" ", "_").lower() + ".txt") not in ferdig_shelves:
            f = open(working_path + value.strip(" ").replace(" ", "_").lower() + ".txt", "w+")

        else:
            flash(":(")
            return render_template("counting.html", len=len(working_shelves), shelves=working_shelves)
    working_shelves = [f for f in listdir(working_path) if isfile(join(working_path, f))]
    return render_template("counting.html", len = len(working_shelves), shelves = working_shelves)

@app.route('/counting/<shelf>')
def view_counting_shelf(shelf):
    liste = []
    with open("telling/year/2020/" + shelf, "r") as file:
        for i, line in enumerate(file):
            if len(line) <= 4:
                continue
            liste.append(line.split("@"))
    return render_template("new.html", file=liste, len=len(liste), shelf=shelf)

@app.route('/new')
def new():
    return render_template("new.html")

@app.route('/new_shelf', methods=["GET"])
def new_shelf():
    return render_template("new_shelf.html")

@app.route('/temp', methods=["GET", "POST"])
def temp():
    code=""
    shelf=""
    name=""
    for i, value in request.form.items():
        if i == "shelf":
            shelf += (value.replace(" ", "_")+".txt").lower()
        elif i == "code":
            code += value
    if code in dictionary:
        # url = f'https://barcode.tec-it.com/barcode.ashx?data={code}&code=EAN13'
        # page = requests.get(url)
        #
        # f_ext = os.path.splitext(url)[-1]
        # f_name = "barcodes/{code}.jpg"
        # with open(f_name, 'wb') as f:
        #     f.write(page.content)
        name = dictionary[code]
    return render_template("add_item.html", shelf=shelf, code=code, name=name, len=len(name), len2=len(code))

@app.route('/add_item/<shelf>&<code>', methods=["GET", "POST"])
def add_item(shelf, code):
    string = ""
    ean = ""
    name = ""
    for i, value in request.form.items():
        if i == "shelf":
            continue
        elif i == "barcode":
            ean = value
        elif i == "name":
            name = value
        elif i == "value" and value == "":
            value = "1"
        string += value + "@"

    with open("telling/year/2020/" + shelf, "r") as file:
        length = str(len(file.readlines()))

    with open("telling/year/2020/" + shelf, "a") as file:
        file.write(length+"@"+string)
        file.write("\n")

    dictionary[ean] = name

    np.save('my_file.npy', dictionary)

    return render_template("barcode.html", shelf=shelf)

@app.route('/barcode/<shelf>', methods=["GET", "POST"])
def barcode(shelf):
    return render_template("barcode.html", shelf=shelf)

@app.route('/move_done', methods=["GET", "POST"])
def move_done():
    for i, value in request.form.items():
        with open(working_path+f"/{i}") as file:
            with open(done_path+f"/{i}", "w") as file2:
                for line in file:
                    file2.write(line)
        remove(working_path+f"/{i}")
    return render_template("home.html")

@app.route('/move_ferdig', methods=["GET", "POST"])
def move_ferdig():
    for i, value in request.form.items():
        with open(done_path+f"/{i}") as file:
            with open(ferdig_path+f"/{i}", "w") as file2:
                for line in file:
                    file2.write(line)
        remove(done_path+f"/{i}")
    return render_template("home.html")

@app.route('/backup', methods=["GET", "POST"])
def hidden():
    ferdig_shelves = [f for f in listdir(ferdig_path) if isfile(join(ferdig_path, f))]
    return render_template("overview.html", len = len(ferdig_shelves), shelves = ferdig_shelves)

@app.route('/delete_all')
def delete_all():
    return render_template("delete_all.html")

@app.route('/delete_shelf')
def delete_shelf():
    return render_template("delete_shelf.html")

@app.route('/deleting_shelf', methods=["GET", "POST"])
def deleting_shelf():
    for i, value in request.form.items():
        if i == "hylle":
            try:
                remove(working_path+value.lower().replace(" ", "_")+".txt")
            except:
                break
    return render_template("home.html")

@app.route('/deleting_every_shelf', methods=["GET", "POST"])
def delete():
    for i, value in request.form.items():
        if i == "hylle" and value.lower() == "byggmix":
            working_shelves = [f for f in listdir(working_path) if isfile(join(working_path, f))]
            done_shelves = [f for f in listdir(done_path) if isfile(join(done_path, f))]
            ferdig_shelves = [f for f in listdir(ferdig_path) if isfile(join(ferdig_path, f))]
            for shelf in working_shelves:
                remove(working_path+shelf)
            for shelf in done_shelves:
                remove(done_path+shelf)
            for shelf in ferdig_shelves:
                remove(ferdig_path+shelf)
        return render_template("home.html")

@app.route('/remove_item', methods=["GET", "POST"])
def remove_item():
    row = -1
    shelf =""
    for i, value in request.form.items():
        if value != "Slett vare":
            shelf = i
            row = value
    with open(working_path+f"/{shelf}", "r") as file:
        lines = file.readlines()
    with open(working_path+f"/{shelf}", "w") as file:
        value = 0
        for i, line in enumerate(lines):
            line = line.split("@")
            if line[0] == row:
                continue
            else:
                file.write(f"{value}@{line[1]}@{line[2]}@{line[3]}@\n")
                value += 1
    liste = []
    with open("telling/year/2020/" + shelf, "r") as file:
        for i, line in enumerate(file):
            if len(line) <= 4:
                continue
            liste.append(line.split("@"))
    return render_template("new.html", file=liste, len=len(liste), shelf=shelf)

@app.route('/upload')
def index():
    return render_template('upload.html')

@app.route('/uploader', methods=['POST'])
def upload_file():
    global dictionary
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        uploaded_file.save("files/"+uploaded_file.filename)
        func.update_dictionary()
    dictionary = np.load('my_file.npy', allow_pickle='TRUE').item()
    return render_template("home.html")

@app.route('/guide')
def guide():
    return render_template('guide.html')

@app.route('/guide_telling')
def guide_telling():
    return render_template('guide_telling.html')

@app.route('/guide_oversikt')
def guide_oversikt():
    return render_template('guide_oversikt.html')

@app.route('/guide_nytt')
def guide_nytt():
    return render_template('guide_nytt.html')

@app.route('/send_varer')
def send_varer():
    return render_template('send_varer.html')

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", ssl_context=('cert.pem', 'key.pem'))
