"""
__init__.py
Author: @ Tan Zhao Yea

Flask is a microframework for Python based on Werkzeug, Jinja 2 and good intentions.
Form Validation with WTForms.

More Info:
Flask: http://flask.pocoo.org/
WTForms: http://flask.pocoo.org/docs/1.0/patterns/wtforms/
"""

from flask import Flask, render_template, request, redirect, flash, session
from flask_wtf.csrf import CSRFProtect

import os
import function1 as f1
import function3 as f3
import main
import ui

app = Flask(__name__)  # initialise the flask app
app.config['SECRET_KEY'] = 'secret!'  # create the secret key

csrf = CSRFProtect(app)  # protect the csrf app
csrf.init_app(app)  # initialise the csrf with the app

profiles_dir = []  # specify and empty list to store the directory of the profiles
name_list = []  # specify an empty name list to store the name
main_class = {}  # store the main class to call the main method in main.py


@app.route('/')
def index():
    if not session.get(
            'profiles'):  # if profiles directory not specified return to welcome.html to specify the profile directory
        return render_template('welcome.html')

    else:
        try:
            profiles = [file for file in os.listdir(profiles_dir[0]) if
                        file.endswith(".txt")]  # list out all the profiles in profiles folder

            # run the function to generate the profiles list
            f1_list = f1.FUNCTION_1(profiles_dir=profiles_dir[0], files=profiles)
            df = f1_list.profilesDF(f1_list.HEADERS, f1_list.DATA)

            m_class = main.MAIN(df)  # Create the main class method
            main_class['m_class'] = m_class  # store it in memory so can be accessible throughout

            data_list = f3.LIKES_DISLIKES(df).temp_list  # converts the entire df into a list

            # store the names of all the female, used to display the names of studnet B in the html
            female_list = [val['Name'].replace(' ', '') for val in data_list if val['Gender'] == 'F']
            # store the names of all the male, used to display the names of studnet B in the html
            male_list = [val['Name'].replace(' ', '') for val in data_list if val['Gender'] == 'M']

            # if the name exist in the name_list do no append, one of the dropdown feature in the html page
            for val in data_list:
                if val['Name'] not in name_list:
                    name_list.append(val['Name'])

            # creates the template data and pass it into the html for viewing of data
            templateData = {
                'data': data_list,  # return and pass the data to index.html
                'female_list': female_list,
                'male_list': male_list
            }
            return render_template('index.html', **templateData)

        except:
            # if session expire, set the session to False
            session['profiles'] = False
            flash('Session Expire')
            return redirect('/')


# handles the form when a dir is specifies
@app.route('/home', methods=["GET", "POST"])
def home():
    if request.method == 'POST':  # check form methods
        file_path = request.form['file_path']  # get the file path specifiedin the form

        if not os.path.exists(file_path):  # check if the file exist in the user system
            flash('Directory does not exist')  # display an error
            return redirect('/')  # trys again

        elif ui.checkFile(file_path) == "False":  # check if the file is the correct directory
            flash(
                'Profiles Directory specified is either empty or not in the correct format. Are you sure you point to the right directory?')  # display an error
            return redirect('/')  # trys again

        else:
            session['profiles'] = True  # set session to be true, the user can now access the dashboard
            profiles_dir.append(file_path)  # add the valid profiles path in the list to be about the data

            return redirect('/')


@app.route('/functions')
def functions():
    if not session.get(
            'profiles'):  # if profiles directory not specified return to welcome.html to specify the profile directory
        return render_template('welcome.html')
    else:
        if name_list == []:  # if the name list is empty set the session to be false
            session['profiles'] = False
            flash('Session Expire')  # display error
            return redirect('/')  # try again
        else:
            # parse the name list into the funtions html for usage of dropdown feature in functions.html
            templateData = {
                'name_list': name_list
            }
            return render_template('functions.html', **templateData)


@app.route('/result', methods=["GET", "POST"])
def handle_functions():
    if not session.get(
            'profiles'):  # if profiles directory not specified return to welcome.html to specify the profile directory
        return render_template('welcome.html')

    else:
        if request.method == 'POST':  # check form methods
            option = request.form['option']  # check the option from the form

            # get the m_class Class
            m_class = main_class.get('m_class')

            # Run function 2 if the option is 2
            if option == '2':
                f2_sb_name = request.form['f2_name']  # get the selected name from the f2 form

                """ This part get student B info """
                f2_sb_df = m_class.student_B(f2_sb_name)  # get the sutdent B dataframe from the selected name

                f2_df = m_class.function2(f2_sb_df, f2_sb_name)  # get the dataframe from function 2

                """ This part serves function 2 """
                f2_list = f3.LIKES_DISLIKES(f2_df).temp_list  # convert dataframe to list

                # parse the list into the results html to display the output of the function
                templateData = {
                    'name': f2_sb_name,
                    'data': f2_list
                }

                return render_template("results.html", **templateData)

            # Run function 3 if the option is 3
            if option == '3':
                """ This part serves function 3 """
                f3_sb_name = request.form['f3_name']  # get the selected name from the f3 form

                """ This part get student B info """
                f3_sb_df = m_class.student_B(f3_sb_name)  # get the sutdent B dataframe from the selected name
                f2_df = m_class.function2(f3_sb_df, f3_sb_name)  # get the dataframe from function 2

                f3_class = f3.LIKES_DISLIKES(f2_df)  # calling the class LIKES_DISLIKES
                f3_temp_profiles_list = f3_class.temp_list  # converting dataframe to list

                f3_df = m_class.function3(f3_class, f3_temp_profiles_list,
                                          f3_sb_df)  # get the dataframe from function 3

                f3_list = f3.LIKES_DISLIKES(f3_df).temp_list  # convert dataframe to list

                # parse the list into the results html to display the output of the function
                templateData = {
                    'name': f3_sb_name,
                    'data': f3_list
                }

                return render_template("results.html", **templateData)

            # Run function 4 and 5
            password = request.form['api-key-pwd']  # get the api password
            bk = m_class.updateBooksGenre(password)  # start of fucntion 4 to update the book

            # Run function 4 if the option is 4
            if option == '4':
                f4_sb_name = request.form['f4_name']  # get the selected name from the f4 form
                f4_sb_df = m_class.student_B(f4_sb_name)  # get the dataframe from the selected name
                f2_df = m_class.function2(f4_sb_df, f4_sb_name)  # get the dataframe from function 2
                f4_class = f3.LIKES_DISLIKES(f2_df)  # calling the class LIKES_DISLIKES
                f4_temp_profiles_list = f4_class.temp_list  # converting dataframe to list

                f4_df = m_class.function4(bk, f4_temp_profiles_list, f4_sb_df)  # get the dataframe from function 4
                f4_list = f3.LIKES_DISLIKES(f4_df).temp_list  # convert dataframe to list

                # parse the list into the results html to display the output of the function
                templateData = {
                    'name': f4_sb_name,
                    'data': f4_list
                }
                return render_template('results.html', **templateData)

            # Run function 5 if the option is 5
            if option == '5':
                name = request.form['name']  # get the selected name from the f5 form

                """ This part get student B info """
                f5_sb_df = m_class.student_B(name)  # get the dataframe from the selected name
                f2_df = m_class.function2(f5_sb_df, name)

                f3_class = f3.LIKES_DISLIKES(f2_df)  # calling the class LIKES_DISLIKES
                f3_temp_profiles_list = f3_class.temp_list  # get the dataframe from function 2
                f3_df = m_class.function3(f3_class, f3_temp_profiles_list,
                                          f5_sb_df)  # get the dataframe from function 3

                """ This part serves function 5 """
                f5_df = m_class.function4(bk, f3_temp_profiles_list, f5_sb_df)  # get the dataframe from function 5
                f5_list = f3.LIKES_DISLIKES(f5_df).temp_list  # convert dataframe to list

                # parse the list into the results html to display the output of the function
                templateData = {
                    'name': name,
                    'data': f5_list
                }

                return render_template('results.html', **templateData)

        return redirect('/functions')


# reset the session if the file cannot load the profiles dir
@app.route("/logout")
def logout():
    session['profiles'] = False
    return redirect('/')


# display the error if the user tries to attempt to go to a site without providing a profiles dir
@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404


# display the error if the user tries to attempt to go to a site without providing a profiles dir
@app.errorhandler(500)
def internal_server_error(e):
    # note that we set the 404 status explicitly
    return render_template('500.html'), 500
