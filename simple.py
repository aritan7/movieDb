from flask import Flask
from flask import render_template
from flask import request, redirect, url_for
import sqlite3
import pandas as pd
import re



app = Flask(__name__)

@app.route("/")
def hello():

    return render_template('index.html')



@app.route('/run', methods=['GET', 'POST'])
def exec():
    inputs = request.form.get("tbarea")
    if not inputs:
        return redirect(url_for('hello'))
    # inputs = re.sub("\n|\r", " ", inputs)
    conn = sqlite3.connect('movie.db')
    check_select = inputs.split(" ")[0]
    if check_select.lower() != "select":
        return render_template('index.html', query="", error = "Error: SELECT operation only.")
    


    try:
        df = pd.read_sql_query(inputs, conn)
    except Exception as e:
        err = e
        return render_template('index.html', query="", error = e, inputs = inputs)
    
    query = df.to_html()
    return render_template('index.html', query=query, inputs = inputs)








if __name__ == "__main__":

    app.run(host='0.0.0.0')