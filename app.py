from flask import Flask, render_template, redirect, request, session
from werkzeug.utils import secure_filename
import ai
import os

app = Flask(__name__)

app.secret_key = os.getenv("SECRET_KEY")
UPLOAD_FOLDER= os.getenv("UPLOAD_FOLDER")
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
           
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        message=request.form['question']
        document = request.files['doc_file']
        
        if document and allowed_file(document.filename):
            filename = secure_filename(document.filename)
            document_path = os.path.join(UPLOAD_FOLDER, filename)
            document.save(document_path)
            print("**STEP 1")
            file_id=ai.upload_file(document_path)
            session['uploaded_file_id'] = file_id            
            print("**STEP 2")
            
        elif 'uploaded_file_id' in session :
            file_id =  session['uploaded_file_id']
            answer = ai.get_response(message, file_id)
            print("**SESSION****")
            
        else:
            answer = ai.get_response(message, file_id)
            print("**NASWER***")
    # print("ANSWER :", answer)      
    
    return render_template('index.html')
    
if __name__ == "__main__":
    app.run(debug = True)
