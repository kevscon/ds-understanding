# Input/Output App
# flask application to collect/modify user input and display output
# run by typing "python app.py" in terminal within app directory

# imports
from flask import Flask, render_template, request, redirect, flash
from config import Config

# initialize app
app = Flask(__name__)
# get configuration settings from config file and Config class
app.config.from_object(Config)

# define list of items for select box
select_items = [
    'add num2word',
    'multiply word by num',
    'add :/ to word'
]

# flask function to render webpage with variable
# decorator to link function to webpage
@app.route('/')
# function to run on webpage
def input():
    # render webpage
    return render_template(
        'home.html', # html script
        select_items=select_items # pass variable to html script
    )

# render app output on webpage
@app.route('/', methods=['POST'])
def output():
    # unless error returned while doing this, do this
    try:
        # retrieve user input and assign to variables
        txt_inp = request.form['txt_inp']
        num_inp = request.form['num_inp']
        cat_inp = request.form['cat_inp']
        # check if any user input is blank
        if not txt_inp or not num_inp or not cat_inp:
            # flash error message
            flash('Error: input must be entered for all items')
            # reset this webpage with flash message
            return redirect(request.url)
        else:
            # generate output based on selected task action
            if cat_inp == 'add num2word':
                result = txt_inp + num_inp
            elif cat_inp == 'multiply word by num':
                result = txt_inp * int(num_inp)
            else:
                result = txt_inp + ':/' * int(num_inp)
            return render_template(
                'result.html',
                txt_inp=txt_inp,
                num_inp=num_inp,
                cat_inp=cat_inp,
                result=result
            )
    # if error returned in try statement above, do this
    except:
        flash('Error: input must be entered for all items')
        return redirect(request.url)

# render about webpage
@app.route('/about')
def about():
    return render_template('about.html')

# check if code is being run as a script (not an import)
if __name__ == '__main__':
    # run function
    app.run(debug=True) # return error description
