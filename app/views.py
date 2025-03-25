from werkzeug.utils import secure_filename
from flask import request, render_template, redirect, url_for, session, request
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

    return render_template('visualizer.html', data=data, filename=filepath)

def info():
    return render_template('info.html', info="This is a simple CSV visualizer. Upload a CSV file to visualize its contents.")

def describe():
    return render_template('describe.html')

def remove():
    if 'uploaded_file' in session:
        filepath = session['uploaded_file']
        if os.path.exists(filepath):
            os.remove(filepath)
        session.pop('uploaded_file', None)
    session.clear()
