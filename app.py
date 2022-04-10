from flask import Flask, render_template, request, redirect, url_for
import csv 
app = Flask(__name__)

CLASS_PATH = app.root_path + '/classes.csv'
CLASS_KEYS = ['name', 'yoga_type', 'yoga_level', 'date', 'duration', 'trainer', 'description']

# with open(CLASS_PATH, 'r') as csvfile:
#     data = csv.DictReader(csvfile)
#     classes = {row['name']:{'type':row['type'],'level':row['level'],'date':row['date'],'duration':row['duration'],'trainer':row['trainer'],'description':row['description']} for row in data}

def get_classes():
    try:
        with open(CLASS_PATH) as csvfile:
            data = csv.DictReader(csvfile)
            classes = {}
            for class_id in data:
                classes[class_id['name']] = class_id
    except Exception as e:
        print(e)
    return classes

def set_classes(classes):
    try:
        with open(CLASS_PATH, mode='w', newline='') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=CLASS_KEYS)
            writer.writeheader()
            for yo_cl in classes.values():
                writer.writerow(yo_cl)
    except Exception as err:
        print(err)

@app.route('/')
def index():
    return render_template('index.html')
@app.route('/classes')
@app.route('/classes/<class_id>')
def classes(class_id=None):
    yoga_classes = get_classes()
    if class_id and class_id in yoga_classes.keys():
        yc = yoga_classes[class_id]
        return render_template('class.html', yc=yc)
    else:
        return render_template('classes.html', yoga_classes=yoga_classes)

@app.route('/add_class', methods=['GET', 'POST'])
def add_class():
    if request.method == 'POST':
        yoga_classes = get_classes()
        newClass = {}

        newClass['name'] = request.form['name']
        newClass['yoga_type'] = request.form['yoga_type']
        newClass['yoga_level'] = request.form['yoga_level']
        newClass['date'] = request.form['date']
        newClass['duration'] = request.form['duration']
        newClass['trainer'] = request.form['trainer']
        newClass['description'] = request.form['description']

        yoga_classes[request.form['name']] = newClass
        set_classes(yoga_classes)

        return redirect(url_for('classes'))
    else:
       return render_template('class_form.html')

@app.route('/classes/<class_id>/edit', methods=['GET', 'POST'])
def edit_class(class_id=None):
    yoga_classes = get_classes()
    if request.method == 'POST':
        yc = yoga_classes[class_id] #YC IS equal to the yoga_classes[class_id] to be a shortcut
        newClass = {}
    
        newClass['name'] = request.form['name']
        newClass['yoga_type'] = request.form['yoga_type']
        newClass['yoga_level'] = request.form['yoga_level']
        newClass['date'] = request.form['date']
        newClass['duration'] = request.form['duration']
        newClass['trainer'] = request.form['trainer']
        newClass['description'] = request.form['description']
        yoga_classes[class_id]=newClass
        set_classes(yoga_classes)

        return redirect(url_for('classes', yc=yc))
    else:
        yc = yoga_classes[class_id]
        return render_template('class_form.html', yc=yc, class_id=class_id)

#class id = something, display info