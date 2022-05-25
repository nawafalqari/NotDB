import notdb
from flask import Flask, render_template, request, Response

app = Flask(__name__)
db = notdb.NotDBClient('db.ndb')

@app.route('/', methods=['GET', 'POST'])
def index():
   if request.method == 'POST':
      file = request.files['file']
      name = request.form['name']

      db.files.appendFileWerkzeug(file, name=name)

      return 'Uploaded successfully'
   return render_template('index.html')

@app.route('/<name>')
def render_image(name):
   file = db.files.getFile({'name': name})

   if not file:
      return 'Invalid name'

   return Response(file['data'], mimetype=file['mimetype'])

app.run(debug=True)