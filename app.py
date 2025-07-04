from flask import Flask, render_template, redirect, request, session, flash
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
    if 'history' not in session:
        session['history'] = []
        
    if request.method == 'POST':
        message=request.form['question']
        document = request.files['doc_file']
        
        file_id=None
        answer=""
        
        if document and allowed_file(document.filename):
            print("I came here")
            filename = secure_filename(document.filename)
            document_path = os.path.join(UPLOAD_FOLDER, filename)
            document.save(document_path)            
            file_id=ai.upload_file(document_path)
            
            # save then file_id in session
            if file_id:
                session['uploaded_file_id'] = file_id
                session.modified = True                     
            
            # if user also sends message with file
            if message:
                print(" Im in ONLY_QUESTION app.py")
                answer = ai.get_response(message,file_id)
            
            # if users only uploads file and asks no questions
            else:
                prompt = "Give a summary for this document in 5 lines"
                answer = ai.get_response(prompt, file_id)
                
            session['history'].append((message, answer))
            session.modified = True
            return render_template('index.html', history=session['history'])
        
        # Already file is uploaded + ask questions about it    
        elif 'uploaded_file_id' in session and message :
            print("Im in SESSION")
            file_id =  session['uploaded_file_id']
            answer = ai.get_response(message, file_id)   
            
            session['history'].append((message, answer))
            session.modified = True
            return render_template('index.html', history=session['history'])         
        
        # No file uload, only questions about space    
        elif  message:
            answer = ai.handle_message_only(message)
            print("I got Only msg or MSG and ID")                   

            session['history'].append((message, answer))
            session.modified = True
            return render_template('index.html', history=session['history'])            
        else:        
            flash("Please upload a file or ask a question.")
    
    return render_template('index.html', history=session.get('history', []))
    
if __name__ == "__main__":
    app.run(debug = True)
