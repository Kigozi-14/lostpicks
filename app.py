from flask import Flask, render_template, request, redirect, Response, url_for
from flask_sqlalchemy import SQLAlchemy
import re


#APP CONFIGURATIONS HERE
app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1234@localhost/lostpicks'
db = SQLAlchemy(app)
app.app_context().push()

# DEFINING THE MODELS FOR OUR DATABASE

class National_ids(db.Model):
    __tablename__ = 'National Ids'
    id = db.Column(db.Integer, primary_key=True)
    Names = db.Column(db.Text, nullable=False)
    Nin = db.Column(db.String(15), nullable=False)
    Card_number = db.Column(db.Integer, nullable=False)
    Contact = db.Column(db.Integer, nullable=False)
    Photo = db.Column(db.LargeBinary)
    def __init__(self, Names, Nin, Card_number, Contact, Photo):
        self.Names = Names
        self.Nin = Nin
        self.Card_number = Card_number
        self.Contact = Contact
        self.Photo = Photo

class Number_plates(db.Model):
    __tablename__ = 'Number Plates'
    id = db.Column(db.Integer, primary_key=True)
    Plate_number = db.Column(db.String(7), nullable=False)
    Contact = db.Column(db.Integer, nullable=False)
    Photo = db.Column(db.LargeBinary)
    def __init__(self, Plate_number, Contact, Photo):
        self.Plate_number = Plate_number
        self.Contact = Contact
        self.Photo = Photo

class Driving_permits(db.Model):
    __tablename__ = 'Driving Permits'
    id = db.Column(db.Integer, primary_key=True)
    Names = db.Column(db.Text, nullable=False)
    Card_number = db.Column(db.Integer, nullable=False)
    Contact = db.Column(db.Integer, nullable=False)
    Photo = db.Column(db.LargeBinary)
    def __init__(self, Names, Card_number, Contact, Photo):
        self.Names = Names
        self.Card_number = Card_number
        self.Contact = Contact
        self.Photo = Photo

class Other_cards(db.Model):
    __tablename__ = 'Other Cards'
    id = db.Column(db.Integer, primary_key=True)
    Names = db.Column(db.Text, nullable=False)
    Card_number = db.Column(db.Integer, nullable=False)
    Contact = db.Column(db.Integer, nullable=False)
    Photo = db.Column(db.LargeBinary)
    def __init__(self, Names, Card_number, Contact, Photo):
        self.Names = Names
        self.Card_number = Card_number
        self.Contact = Contact
        self.Photo = Photo

class Documents(db.Model):
    __tablename__ = 'Documents'
    id = db.Column(db.Integer, primary_key=True)
    Names = db.Column(db.Text, nullable=False)
    Contact = db.Column(db.Integer, nullable=False)
    Photo = db.Column(db.LargeBinary)
    def __init__(self, Names, Contact, Photo):
        self.Names = Names
        self.Contact = Contact
        self.Photo = Photo

#DEFINING THE FUNCTIONS TO CHECK WHETHER THE INPUTS WILL BE VALID BEFORE ADDING THEM TO THE DATABASE

def image_checking(image_name):
    file_types = {'jpg', 'png', 'PNG', 'JPG'}
    exte = None
    for i in range(len(image_name)-1, -1, -1):
        if image_name[i] == '.':
            exte = image_name[i+1:]
            break
    if exte in file_types:
        return True
    else:
        return False

def contact_checking(contact):
    regex_pattern = r"^(075|070|077|074|078|076)\d{7}$"
    if re.match(regex_pattern, contact):
        return True
    else:
        return False

def names_checking(names):
    regex_match1 = r"^[A-Z]+ [A-Z]+$"
    regex_match2 = r"[A-Z]+ [A-Z]+ [A-Z]+$"
    if re.match(regex_match1, names) or re.match(regex_match2, names):
        return True
    else:
        return False

def nin_checking(nin):
    regex_pattern = r"^(CM|CF)\d{2}[A-Z0-9]{10}$"
    if re.match(regex_pattern, nin):
        return True
    else:
        return False

def cardNum_checking(card_num):
    if len(card_num) == 9:
        return True
    else:
        return False

def numberPlate_checking(numberPlate):
    regex_pattern = r"^U[A-Z]{2}\d{3}[A-Z]$"
    if re.match(regex_pattern, numberPlate):
        return True
    else:
        return False

#DEFINING ROUTES TO ALLOW SWITCHING ON NAV LINKS AND FETCH DATA FROM OUR DATABASE

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/national_id_page')
def nationalid():
    my_ids = National_ids.query.all()
    return render_template('national_ids.html', my_ids=my_ids)

@app.route('/number_plate_page')
def numberplates():
    plates = Number_plates.query.all()
    return render_template('number_plates.html', plates=plates)

@app.route('/driving_permit_page')
def drivingpermit():
    permits = Driving_permits.query.all()
    return render_template('driving_permits.html', permits=permits)

@app.route('/other_card_page')
def othercard():
    cards = Other_cards.query.all()
    return render_template('other_card.html', cards=cards)

@app.route('/documents_page')
def documents():
    documents = Documents.query.all()
    return render_template('documents.html', documents=documents)

@app.route('/contact_page')
def contact():
    return render_template('contact.html')

#DEFINING THE ROUTES THAT FETCH THE DATA FROM OUR HTML FORMS AND THEN ADD IT TO THE DATABASE

@app.route('/post_national_id', methods = ['POST'])
def post_national_id():
    if request.method == 'POST':
        card_names = request.form['names']
        card_number = request.form['cardnumber']
        card_nin = request.form['nin']
        card_contact = request.form['contact']
        card_image = request.files['image_file'].read()
        photo_name = request.files['image_file']
        file_name = photo_name.filename
        if names_checking(card_names) == True:
            if cardNum_checking(card_number) == True:
                if nin_checking(card_nin) == True:
                    if contact_checking(card_contact) == True:
                        if image_checking(file_name) == True:
                            our_data = National_ids(card_names, card_nin, card_number, card_contact, card_image )
                            db.session.add(our_data)
                            db.session.commit()
                            print('THX FOR UPLOADING')
                            return redirect('/national_id_page')
                        else:
                            return redirect('/national_id_page')
                    else:
                        return redirect('/national_id_page')
                else:
                    return redirect('/national_id_page')
            else:
                return redirect('/national_id_page')
        else:
            print('Wrong Names')
            return redirect('/national_id_page')        

            # return render_template('national_ids.html', message = 'PLEASE ENTER CORRECT NAMES IN CAPITAL LETTERS')
    
@app.route('/post_number_plates', methods = ['POST'])
def post_number_plates():
    if request.method == 'POST':
        plate_number = request.form['number']
        plate_contact = request.form['contact']
        plate_image = request.files['image_file'].read()
        image_name = request.files['image_file']
        file_name = image_name.filename
        if numberPlate_checking(plate_number) == True:
            if contact_checking(plate_contact) == True:
                if image_checking(file_name) == True:
                    plate_data = Number_plates(plate_number, plate_contact, plate_image)
                    db.session.add(plate_data)   
                    db.session.commit() 
                    print('THX FOR UPLOADING')
                    return redirect('/number_plate_page')
                else:
                    return redirect('/number_plate_page')
            else:
                return redirect('/number_plate_page')    
        else:
            return redirect('/number_plate_page')    
        

@app.route('/post_driving_permit', methods = ['POST'])
def post_driving_permits():
    if request.method == 'POST':
        permit_names = request.form['names']
        permit_number = request.form['permit_number']
        permit_contact = request.form['contact']
        permit_image = request.files['image_file'].read()
        photo_name = request.files['image_file']
        file_name = photo_name.filename
        if names_checking(permit_names) == True:
            if contact_checking(permit_contact) == True:
                if image_checking(file_name) == True:
                    permit_data = Driving_permits(permit_names, permit_number, permit_contact, permit_image )
                    db.session.add(permit_data)
                    db.session.commit()
                    print('THX FOR UPLOADING')
                    return redirect('/driving_permit_page')
                else:
                    print('WRONG IMAGE')
                    return redirect('/driving_permit_page')
            else:
                print('WRONG CONTACT')
                return redirect('/driving_permit_page')
        else:
            print('WRONG NAMES')
            return redirect('/driving_permit_page')

@app.route('/post_other_cards', methods = ['POST'])
def post_other_cards():
    if request.method == 'POST':
        cards_names = request.form['names']
        cards_number = request.form['cardnumber']
        cards_contact = request.form['contact']
        cards_image = request.files['image_file'].read()
        photo_name = request.files['image_file']
        file_name = photo_name.filename
        if names_checking(cards_names) == True:
            if contact_checking(cards_contact) == True:
                if image_checking(file_name) == True:
                    cards_data = Other_cards(cards_names, cards_number, cards_contact, cards_image )
                    db.session.add(cards_data)
                    db.session.commit()
                    print('THX FOR UPLOADING')
                    return redirect('other_card_page')
                else:
                    return redirect('other_card_page')
            else:
                return redirect('other_card_page')
        else:
            return redirect('other_card_page')
        
@app.route('/post_documents', methods = ['POST'])
def post_documents():
    if request.method == 'POST':
        documents_names = request.form['names']
        documents_contact = request.form['contact']
        documents_image = request.files['image_file'].read()
        photo_name = request.files['image_file']
        file_name = photo_name.filename
        if names_checking(documents_names) == True:
            if contact_checking(documents_contact) == True:
                if image_checking(file_name) == True:
                    documents_data = Documents(documents_names, documents_contact, documents_image )
                    db.session.add(documents_data)
                    db.session.commit()
                    return redirect('/documents_page')
                else:
                   return redirect('/documents_page')
            else:
                return redirect('/documents_page')
        else:
            return redirect('/documents_page')


#DEFINING OUR API'S TO FETCH DATA FROM THE DATABASE FOR THE SEARCHING POURPOSE

@app.route('/nationalid_search')
def search_nationalid():
    return render_template('national_ids.html')

@app.route('/numberplate_search')
def search_numberplate():
    return render_template('national_ids.html')

@app.route('/drivingpermit_search')
def search_drivingpermit():
    return render_template('national_ids.html')

@app.route('/othercards_search')
def search_othercards():
    return render_template('national_ids.html')

@app.route('/documents_search')
def search_documets():
    return render_template('national_ids.html')


if __name__ == '__main__':
    app.run(debug=True)