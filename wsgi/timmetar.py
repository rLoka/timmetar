"""
Routes and views for the flask application.
"""
import sqlite3, string, random
from database import *
from datetime import datetime
from flask import *
from flask_recaptcha import ReCaptcha
from functools import wraps

app = Flask(__name__)

#Spajanje na bazu
db = sqlite3.connect('timdb.db', check_same_thread=False)
app.secret_key = 'GspIYzGXABPOgAQnmSGxllPRxMhcCmLlZePTQtLehCcowXcvAstLFLHYNKmstRmDGFANwiGolBidnMadrGahdvZKZeiuPxQCYbgm'

app.config['RECAPTCHA_SITE_KEY'] = "6Lc4hxcTAAAAANwUUi-bSCTRvNK3Hx0FOO0BA0gz"
app.config['RECAPTCHA_SECRET_KEY'] = "6Lc4hxcTAAAAAPRQRHL78EXUS9_PBGyHguebPVgD"

recaptcha = ReCaptcha()
recaptcha.init_app(app)

@app.route('/')
@app.route('/pocetna')
def home():
    if True:#'korisnik' in session:
        #email = session['korisnik']
        ministarstva = dbMinInfo(db)
        obecanja = dbObecanja(db)
        postojeci = False
        if session.get('korisnik') != None:
            postojeci = True
        return render_template(
            'index.html',
            title='Timmetar',
            year = datetime.now().year,
            ministarstva = ministarstva,
            obecanja = obecanja,
            postojeci = postojeci
        )
    else:
        return redirect (url_for('prijava'))

@app.route('/prijava', methods=['GET', 'POST'])
def prijava():
    error = None
    if request.method == "POST":
        if recaptcha.verify():
            session['korisnik'] = ''.join(random.sample(string.letters*20,20))
            session['history'] = {}
            print session['korisnik']
            print session['history']
        return redirect (url_for('home'))

@app.route('/vote')
def vote():
    if session.get('korisnik') != None:
        print session['history']
        actionId = request.args.get('actionId', 0, type=int)
        promiseId = request.args.get('promiseId', 0, type=int)
        if str(promiseId) in session.get('history'):
            print "Vec si glasovao!"
            pastActionId = session['history'].get(str(promiseId), None)
            session['history'][str(promiseId)] = actionId
            dbPonovnoGlasaj(db,promiseId,pastActionId,actionId)
        else:
            session['history'][str(promiseId)] = actionId
            dbGlasaj(db, promiseId, actionId)
        result = dbGlasovi(db,promiseId)
        return jsonify(result)
    else:
        return jsonify(None)
    
if __name__ == "__main__":
	app.run(debug=True)
