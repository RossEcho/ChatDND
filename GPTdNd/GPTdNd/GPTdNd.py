import openai
import random
from werkzeug.security import check_password_hash
from flask import Flask, render_template, request, session, redirect, url_for, flash, send_from_directory
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
from databaseConn import *

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

openai.api_key = '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'

# Mail settings
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'chatdnd.suport@gmail.com'
app.config['MAIL_PASSWORD'] = 'ogpgebmkfsqqpcoq'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)

# This is used to create a safe token
s = URLSafeTimedSerializer('Thisisasecret!')

#Home page
@app.route("/")
def home():
    session['message'] = ''
    session['dice_roll'] = ''
    if current_user.is_authenticated:  # Check if user is logged in using Flask-Login
        return render_template("index.html")  # User is logged in, show the game page
    else:
        return render_template("front_page.html")  # User is not logged in, show the home page

@app.route('/static/<path:path>')
def send_js(path):
    return send_from_directory('static', path)

@login_manager.unauthorized_handler
def unauthorized():
    flash('You must be logged in to view that page.')
    return redirect(url_for('login'))


#Load a user from the database return a User object or None if the user is not found
@login_manager.user_loader
def load_user(user_id):
    return get_user_by_id(user_id)



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        remember = 'remember' in request.form
        user = get_user_by_email(email)
        if user is None or not verify_password(password, user['password']):
            flash('Invalid email or password')
            return redirect(url_for('login'))

        user_obj = User(id=user['id'], email=user['email'], password=user['password'], username=user['username'])
        print("User Object: ", user_obj) # print user object

        login_user(user_obj, remember=remember)  # log in the user using Flask-Login 
        session['username'] = user_obj.username  # set username in session here
        return redirect(url_for('home'))
    else:
        return render_template('login.html')

#Forgot password
@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form['email']

        # Ensure the user exists
        user = get_user_by_email(email)
        if not user:
            return render_template('forgot_password.html', message="Email not found.")

        # Generate token
        token = s.dumps(email, salt='email-confirm')

        # Create email message
        msg = Message('Password Reset Request', 
                      sender='noreply@demo.com', 
                      recipients=[email])

        # Here url_for generates the URL for the reset token
        # _external=True is used to get an absolute URL
        link = url_for('reset_token', token=token, _external=True)

        # This is the email message
        msg.body = f'''To reset your password, visit the following link:
{link}
If you did not make this request then simply ignore this email and no changes will be made.
'''
        # Send the email
        mail.send(msg)
        return render_template('forgot_password.html', message="An email has been sent to reset your password.")
        
    return render_template('forgot_password.html')


# Reset mail token
@app.route('/reset_token/<token>', methods=['GET', 'POST'])
def reset_token(token):
    try:
        email = s.loads(token, salt='email-confirm', max_age=3600)
    except SignatureExpired:
        return '<h1>The token is expired!</h1>'

    if request.method == 'POST':
        password = request.form['password']

        # Update the user's password in your database
        update_password_in_db(email, password)

        return redirect(url_for('login', message="Your password has been updated. Please log in."))

    return render_template('reset_password.html', token=token)


#Logout
@app.route('/logout')
def logout():
    logout_user()
    session.pop('username', None)  # remove username from session
    return redirect(url_for('login'))



#Register page
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        password2 = request.form['password2'] # Confirm password
        username = request.form['uname']
        
        # Error dictionary
        errors = {}

        # Check if email already exists
        if get_user_by_email(email):
            errors['email_error'] = 'Email already exists'

        # Check if passwords match
        if password != password2:
            errors['password2_error'] = 'Passwords must match.'

        # If there are any errors, re-render the form with the errors
        if errors:
            return render_template('register.html', **errors)

        # Create new user
        create_user(email, password, username)

        return redirect(url_for('login'))

    return render_template('register.html')


#Character build
@app.route('/build_character', methods=['GET'])
def build_character_form():
    return render_template('build_character.html')

@app.route('/create_character', methods=['POST'])
def build_character():
    name = request.form['char_name']  # make sure to use the right key
    race = request.form['char_race']  # make sure to use the right key
    class_ = request.form['char_class']  # make sure to use the right key
    level = 0  # setting level to 0
    experience = 0  # setting experience to 0
    strength = request.form['strength']
    dexterity = request.form['dexterity']
    constitution = request.form['constitution']
    intelligence = request.form['intelligence']
    wisdom = request.form['wisdom']
    charisma = request.form['charisma']

    add_character(name, race, class_, level, experience, strength, dexterity, constitution, intelligence, wisdom, charisma)

    return render_template('character_sheet.html', name=name, race=race, class_=class_, level=level, experience=experience, strength=strength, dexterity=dexterity, constitution=constitution, intelligence=intelligence, wisdom=wisdom, charisma=charisma)

#Load profile
@app.route('/profile')
@login_required
def profile():
    user = current_user
    characters = get_characters_by_user_id(user.id)
    return render_template('profile.html', user=user, characters=characters)

#Character sheet
@app.route('/character_sheet')
def character_sheet():
    character = get_character()  # Replace with your actual function
    return render_template('character_sheet.html', name=character.name, race=character.race, class_=character.class_, level=character.level, strength=character.strength, dexterity=character.dexterity, constitution=character.constitution, intelligence=character.intelligence, wisdom=character.wisdom, charisma=character.charisma)


#Dice roll
@app.route('/dice_roll', methods=['POST'])
def dice_roll():
    dice = request.form['dice']
    roll = random.randint(1, int(dice[1:]))
    session['dice_roll'] = "You rolled a {} and got a {}".format(dice, roll)
    return render_template("index.html", message=session['message'], dice_roll=session['dice_roll'])


#ChatBot
@app.route("/chatbot", methods=["POST"])
def chatbot():
    prompt = request.form["prompt"]
    if prompt.strip() == "":
        session['message'] = "Please enter a prompt."
        message = "Please enter a prompt."
    else:
        with open('templates/bot_initialize.txt', 'r') as f:
            bot_initialize = f.read().strip()

            # Fetching character data from your database
            character = get_character_by_name('name_of_your_character')
            character_info = f'Character name: {character["name"]}, Race: {character["race"]}, Class: {character["class"]}, Level: {character["level"]}, Experience: {character["experience"]}, Strength: {character["strength"]}, Dexterity: {character["dexterity"]}, Constitution: {character["constitution"]}, Intelligence: {character["intelligence"]}, Wisdom: {character["wisdom"]}, Charisma: {character["charisma"]}\n'


        comp = openai.ChatCompletion.create(
            model = "gpt-3.5-turbo",
            messages = [
            {"role": "system", "content": bot_initialize},
            {"role": "user", "content":"Lets start a game, this is my character:"+ character_info}
        ]
        )
        message = comp['choices'][0]['message']['content']
    

    session['message'] = message
    session['dice_roll'] = ''
    return render_template("index.html", message=message)

#Races
@app.route('/races')
def races():
    return render_template('races.html')

#Classes
@app.route('/classes')
def classes():
    return render_template('classes.html')


if __name__ == "__main__":
    app.run(debug=False)
    