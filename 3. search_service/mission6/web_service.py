import uuid
import datetime
import advertising

from flask import Flask
from flask import request
from flask import render_template


app = Flask(__name__)

engine = advertising.engine.AdEngine()

@app.route('/find', methods=['POST'])
def find():
    query = request.form['query']
    ads = engine.selectAds(query)
    var = {
        'tm': datetime.datetime.now(),
        'query': query,
        'ads': ads
    }
    print(ads)
    return render_template('find.html', var=var)


@app.route('/')
@app.route('/index')
def home():
    var = {
        'tm': datetime.datetime.now(),
    }
    return render_template('home.html', var=var)


if __name__ == '__main__':
    app.run(debug=True)
