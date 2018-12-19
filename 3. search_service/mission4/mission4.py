import uuid
import datetime
from flask import Flask
from flask import render_template


def AD():
    ret = {}
    ret['adId'] = str(uuid.uuid4())
    ret['campaignId'] = 0
    ret['keyWords'] = []
    ret['relevanceScore'] = 0
    ret['pClick'] = 0
    ret['bidPrice'] = 0
    ret['rankScore'] = 0
    ret['qualityScore'] = 0
    ret['costPerClick'] = 0
    ret['position'] = 0
    ret['title'] = ''
    ret['price'] = 0
    ret['thumbnail'] = ''
    ret['description'] = ''
    ret['brand'] = ''
    ret['detail_url'] = ''
    ret['query'] = ''
    ret['query_group_id'] = 0
    ret['category'] = ''
    return ret


app = Flask(__name__)


@app.route('/')
def home():
    data = {
        'tm': datetime.datetime.now(),
        'ads': [AD(), AD(), AD(), AD(), AD(), AD()]
    }
    return render_template('mission4_template.html', data=data)


if __name__ == '__main__':
    app.run(debug=True)
