from flask import *
import unicodedata
app = Flask(__name__)

@app.route('/')
def main():
   """
   Called if no route is entered
   """
   return redirect('message')


@app.route('/message', methods = ['GET','POST'])
def logMsg():
    if request.method == 'POST':
        text = request.form['text']
        print(text)
        text = text.replace("<3", "\u2764")
        print(">>>>>>text is " + text + "\n\tname: " + unicodedata.name(text))
        return render_template("index.html", text=text)
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)