import notdb # to intract with NotDB database
from flask import Flask, render_template, request, redirect # to create out webapp
from validators import url as url_validator # to validate given urls
from random import sample # to generate url code

urls = notdb.NotDBClient('urls.ndb') # creating our db

app = Flask(__name__) # creating our webapp

def generate_code(length=5):
   upper = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ' # ascii uppercase
   lower = 'abcdefghijklmnopqrstuvwxyz' # ascii lowercase
   upper_and_lower = list(upper) # add every letter in a list element
   upper_and_lower.extend(list(lower)) # extend the "upper_and_lower" [A, B, C... a, b, c...]

   return ''.join(sample(upper_and_lower, length)) # shuffle the list

@app.route('/', methods=['GET', 'POST']) # / stands for the index route (example.com/ <---)
def index():
   if request.method == 'POST': # if submit button was pressed
      url = request.form['url'] # access the url given in the form

      if not url_validator(url): # if url wasn't actually a url
         return 'Invalid url'
      else:
         url_code = generate_code() # generate a code for the url
         server_url = f'{request.base_url}/{url_code}'
         urls.appendOne({
            'code': url_code,
            'url': url
         }) # add the url and its code to the db

         return f'your url=<a href="{server_url}">{server_url}</a>'
   return render_template('add_url.html') # render "templates/add_url.html" file

@app.route('/<code>') # handle every route except "/", for example this will handle "/aKMlws"
def url_handler(code):
   url = urls.getOne({
      'code': code
   }) # get the entire document using the code

   if not url: # if the code doesn't belong to any document/404
      return f'Invalid code: {code}'
   
   return redirect(url['url']) # redirect the user to the url that belongs to the code

if __name__ == '__main__':
   app.run(debug=True)