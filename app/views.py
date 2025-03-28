from werkzeug.utils import secure_filename
from flask import request, render_template, redirect, url_for, session, request, jsonify
import csv
import glob
import os
from .config import Config
import uuid


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS

def index():
    """
    Carga un archivo CSV y lo almacena en la sesión.
    """
    remove()
    if request.method == 'POST':
        if 'file' not in request.files:
            return render_template('upload.html', error="No file part in the request.")

        file = request.files['file']

        if file.filename == '':
            return render_template('upload.html', error="No file selected.")

        if file and allowed_file(file.filename):
            unique_id = str(uuid.uuid4())
            filename = f"{unique_id}_{secure_filename(file.filename)}"
            filepath = os.path.join(Config.UPLOAD_FOLDER, filename)
            file.save(filepath)
            session['uploaded_file'] = filepath
            return redirect(url_for('visualizer'))

        return render_template('upload.html', error="Invalid file type. Only CSV files are allowed.")

    return render_template('upload.html')


def visualizer():
    """
    Visualiza el contenido del archivo CSV cargado.
    """
    if 'uploaded_file' not in session:
        return redirect(url_for('index'))

    filepath = session['uploaded_file']
    if not os.path.exists(filepath):
        return render_template('visualizer.html', error="File not found.")

    data = []
    with open(filepath, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        data = [row for row in reader]

    return render_template('visualizer.html', data=data)

def info():
    return render_template('info.html', info="This is a simple CSV visualizer. Upload a CSV file to visualize its contents.")

def describe():
    return jsonify({"PassengerId":{"count":891.0,"mean":446.0,"std":257.3538420152,"min":1.0,"25%":223.5,"50%":446.0,"75%":668.5,"max":891.0},"Survived":{"count":891.0,"mean":0.3838383838,"std":0.4865924543,"min":0.0,"25%":0.0,"50%":0.0,"75%":1.0,"max":1.0},"Pclass":{"count":891.0,"mean":2.3086419753,"std":0.836071241,"min":1.0,"25%":2.0,"50%":3.0,"75%":3.0,"max":3.0},"Age":{"count":714.0,"mean":29.6991176471,"std":14.5264973323,"min":0.42,"25%":20.125,"50%":28.0,"75%":38.0,"max":80.0},"SibSp":{"count":891.0,"mean":0.5230078563,"std":1.1027434323,"min":0.0,"25%":0.0,"50%":0.0,"75%":1.0,"max":8.0},"Parch":{"count":891.0,"mean":0.3815937149,"std":0.8060572211,"min":0.0,"25%":0.0,"50%":0.0,"75%":0.0,"max":6.0},"Fare":{"count":891.0,"mean":32.2042079686,"std":49.6934285972,"min":0.0,"25%":7.9104,"50%":14.4542,"75%":31.0,"max":512.3292}})

def remove():
    if 'uploaded_file' in session:
        filepath = session['uploaded_file']
        if os.path.exists(filepath):
            os.remove(filepath)
        session.pop('uploaded_file', None)
    session.clear()
