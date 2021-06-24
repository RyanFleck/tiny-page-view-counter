#Bottle Template created by @rediar
#bottle is good for smale scale web applications. It is easy to quickly make API's or small personal webpage using Bottle.

from bottle import request, Bottle
from truckpad.bottle.cors import CorsPlugin, enable_cors
from json import dumps
from replit import db

app = Bottle()


#this is the main page
@app.route('/')
def index():
    return '<pre>RCF Analytics Mk 0.0.0.9</pre>'


#this can only be accesed with a post request (visiting in browser will return 405 Method Not Allowed error)
@enable_cors
@app.post('/api/view-counts/page-tracker/')
def post_request_only():
    print("Analytics POST, collecting data...")
    path: str = str(request.json.get('page_url'))
    site: str = str(request.headers['origin'])
    if not path or not site:
        return dumps({})

    # ReplIT Database HATES '/', so remove 'em
    key: str = f"{site}-{path}".replace('/', ' ').strip().replace(' ', '-')
    print(f"key: {key}")
    try:
        views = db[key]
        print(views)
        db[key] = views + 1
        return dumps({'page_views': views + 1})
    except KeyError:
        print("KeyError, adding...")
        db[key] = 1
        return dumps({'page_views': 1})


#A 404 page if the url doesn't exist
@app.error(404)
def error404(error):
    return (
        "oops! the page you were looked for isn't here. <a href='/'>Return Home?</a>"
    )


app.install(
    CorsPlugin(origins=['http://localhost:1313', 'https://ryanfleck.ca']))
app.run(
    host='0.0.0.0',
    port=1234)  #this starts the webpage. any code after this line won't be run

#Good luck programming!
