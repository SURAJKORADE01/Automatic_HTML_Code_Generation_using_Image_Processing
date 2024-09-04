from flask import *
import os

app = Flask(__name__, template_folder='',
            static_url_path='',
            static_folder='')
file = open(r'trial.py', 'r').read()


@app.route('/')
def index():
    return render_template("index.html")

@app.route('/success')
def success():
    return render_template("success.html")


@app.route('/upload_file', methods = ['POST','GET'])
def upload_file():
    if request.method == 'POST':
        img = request.files['file1']
    
        img.save("sample.png")

        
        exec(file)
        with open("sample.html", "r") as f:
            content = f.read()
        print("file1:",img)
        print("img:",img)
        return render_template("success.html",content=content,img = img)


if __name__ == '__main__':
    app.run(debug=True)