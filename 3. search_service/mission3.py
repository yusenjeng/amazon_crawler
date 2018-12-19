from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello():
    return 'Hello, World!'


@app.route('/ad')
def handler_ad():
    html = '''
<!DOCTYPE html>
<html>
<link rel="stylesheet" href="https://images-na.ssl-images-amazon.com/images/I/61yf4UF1RtL._RC|21j4aYuLqTL.css,318Lc7ZjZUL.css,310HgKKWalL.css_.css#AUIClients/AmazonUI.min" />
<link rel="stylesheet" href="https://images-na.ssl-images-amazon.com/images/G/01/AUIClients/RetailSearchAssets-2de0b41b61e77f4ade0e7400631211d4c3f6e02b._V2_.css#AUIClients/RetailSearchAssets.us.renderskin-pc.search-results-aui.secure.weblab-SEARCH_87269-T1.weblab-SSPA_85092-T1.min" />
<link rel="stylesheet" href="https://images-na.ssl-images-amazon.com/images/I/71pSmmb%2BprL._RC|01e2haXvvBL.css,31ePTgDGunL.css,21mxQA5OIcL.css,31oHW+XUmOL.css,01r3hsp1jOL.css,31UlxNhlUML.css_.css#AUIClients/NavDesktopMetaAsset" />
<link rel="stylesheet" type="text/css" href="https://images-na.ssl-images-amazon.com/images/G/01/x-locale/redirect-overlay/redirect-overlay-nav-mx-https-20150828._CB311575010_.css">

<head>
<meta charset="UTF-8">
<title>welcome to searchAds</title>
</head>
<body>
<ul class="s-result-list s-col-1 s-col-ws-1 s-result-list-hgrid s-height-equalized s-list-view s-text-condensed">
    <h2>ad 1</h2>
    <h2>ad 2</h2>
    <h2>ad 3</h2>
    <h2>ad 4</h2>
    <h2>ad 5</h2>
<ul>
</body>
</html>
'''
    return html


if __name__ == '__main__':
    app.run(debug=True)
