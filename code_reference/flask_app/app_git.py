# run by typing "python app.py" in terminal within app directory

# imports
from flask import Flask, render_template, request

# initialize app
app = Flask(__name__)

# define list of items for select box
select_items = [
    'husky',
    'greyhound',
    'unknown',
    'german shephard',
    'labrador',
    'collie',
    'golden retriever'
]

# decorator to link function to webpage
@app.route('/')
# function to run on webpage
def home():
    # render webpage
    return render_template(
        'home.html', # html script
        select_items=select_items # pass list to webpage
    )

@app.route('/', methods=['POST'])
def home_post():
    # retrieve user input
    txt_inp = request.form['txt_inp']
    num_inp = request.form['num_inp']
    cat_inp = request.form['cat_inp']

    return render_template(
        'result.html',
        txt_inp=txt_inp,
        num_inp=num_inp,
        cat_inp=cat_inp
    )


@app.route('/about')
def about():
    return render_template('about.html')

# run function with error return
if __name__ == '__main__':
    app.run(debug=True)
