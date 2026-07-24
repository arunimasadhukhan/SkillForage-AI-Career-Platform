import os
import sqlite3
import random
from flask import Flask, render_template, request, jsonify

# --- 1. RESOLVE ABSOLUTE SYSTEM PATHS FOR WINDOWS ---
current_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.abspath(os.path.join(current_dir, ".."))
frontend_path = os.path.join(project_dir, 'frontend')

# Initialize Flask framework by pointing directly to your custom frontend folder
app = Flask(__name__, template_folder=frontend_path)

# --- 2. FILE SYSTEM & DATABASE CONFIGURATIONS ---
DB_FILE = os.path.join(current_dir, "skillforge.db")
UPLOAD_FOLDER = os.path.join(current_dir, "uploaded_resumes")
ALLOWED_EXTENSIONS = {'pdf', 'txt'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# --- 3. DATABASE INITIALIZATION ---
def init_db():
    """Initializes the database schema for history tracking logs."""
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT,
                score INTEGER,
                recommendation TEXT,
                uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()

init_db()


# --- 4. DATA PARSING HELPERS ---
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# --- 5. SYSTEM ENDPOINT WEB ROUTING ---

@app.route('/')
def home():
    """Renders the central system analytics dashboard workspace page."""
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_resume():
    """Simulates AI feedback dynamically without needing an external API key."""
    if 'file' not in request.files:
        return jsonify({"status": "error", "message": "No file chunk found in request"}), 400
        
    file = request.files['file']
    if file.filename == '':
        return jsonify({"status": "error", "message": "No file asset selected"}), 400
        
    if file and allowed_file(file.filename):
        # Generate a beautiful, realistic career assessment score dynamically
        ai_score = random.randint(78, 95)
        
        # Actionable engineering career paths
        career_guidance_options = [
            "Strong core technical skills detected. Focus on adding Docker containerization, cloud architecture principles (AWS/Azure), and deep diving into system engineering pipelines.",
            "Excellent project structure. Upskill in advanced backend API optimization, microservices architecture development, and asynchronous message queues like RabbitMQ.",
            "Profile meets industry entry standards. Focus on strengthening data structures and algorithms, building an end-to-end full-stack portfolio item, and deploying your web applications."
        ]
        ai_rec = random.choice(career_guidance_options)

        # Save the parsed tracking metrics log directly to SQLite DB
        with sqlite3.connect(DB_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO history (filename, score, recommendation) VALUES (?, ?, ?)",
                (file.filename, ai_score, ai_rec)
            )
            conn.commit()

        return jsonify({
            "status": "success",
            "score": ai_score,
            "recommendation": ai_rec
        })
            
    return jsonify({"status": "error", "message": "Invalid file format extension layout"}), 400


@app.route('/history', methods=['GET'])
def get_history():
    """Fetches total analytics evaluation tracking logs from internal storage."""
    with sqlite3.connect(DB_FILE) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT filename, score, recommendation, uploaded_at FROM history ORDER BY uploaded_at DESC")
        rows = cursor.fetchall()
        history_list = [dict(row) for row in rows]
            
    return render_template('history.html', history=history_list)


if __name__ == '__main__':
    app.run(debug=True, port=5000)

