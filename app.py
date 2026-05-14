from flask import Flask, request, jsonify
from flask_cors import CORS
import re
import requests
from PyPDF2 import PdfReader

app = Flask(__name__)
CORS(app) 
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024 

def clean_text(text):
    return re.sub(r'[^a-z0-9\s]', '', str(text).lower())

def evaluate_resume(text):
    score = 45 
    text_lower = text.lower()
    words = len(text.split())
    if 150 <= words <= 800: score += 15
    if re.search(r'\d', text) or '%' in text: score += 15
    sections = ['experience', 'skills', 'education']
    score += min(15, sum(1 for sec in sections if sec in text_lower) * 5)
    return int(min(92, score))

def evaluate_portfolio(url):
    if not url: return 0 
    url = url.lower()
    if 'github.com' in url or 'behance.net' in url: return 94
    if 'linkedin.com' in url: return 82
    if 'http' in url: return 75
    return 0 

def evaluate_technical(text, target_role):
    text = text.lower()
    role_keywords = {
        'Data Scientist': ['python', 'sql', 'machine learning', 'data', 'model', 'statistics', 'analytics', 'algorithm'],
        'UI/UX Designer': ['design', 'figma', 'user', 'interface', 'wireframe', 'prototype', 'adobe', 'research'],
        'Software Engineer': ['java', 'javascript', 'react', 'node', 'api', 'git', 'code', 'development', 'backend'],
        'Product Manager': ['strategy', 'agile', 'roadmap', 'cross-functional', 'launch', 'stakeholder', 'scrum']
    }
    keywords = role_keywords.get(target_role, [])
    if not keywords: return 75 
    matches = sum(1 for k in keywords if k in text)
    return int(min(95, 45 + (matches * 10)))

@app.route('/api/evaluate', methods=['POST'])
def evaluate_profile():
    target_role = request.form.get('target_role', 'Data Scientist')
    portfolio_url = request.form.get('portfolio_url', '')
    
    resume_text = ""
    if 'resume_file' in request.files:
        file = request.files['resume_file']
        if file and file.filename.endswith('.pdf'):
            try:
                pdf_reader = PdfReader(file)
                for page in pdf_reader.pages:
                    extracted = page.extract_text()
                    if extracted: resume_text += extracted + " "
            except Exception:
                pass
    
    if not resume_text.strip():
        return jsonify({'error': 'No readable text found in PDF.'}), 400

    has_video = False
    video_score = None
    video_feedback = "Skipped (Optional)"
    
    if 'video_file' in request.files:
        file = request.files['video_file']
        if file and file.filename:
            has_video = True
            OPENAI_API_KEY = "" # Put your key back here!
            
            file_data = file.read()
            size_mb = len(file_data) / (1024 * 1024)
            
            if size_mb > 25:
                video_score = 0
                video_feedback = "File too large. OpenAI Whisper limit is 25MB."
            else:
                try:
                    headers = {'Authorization': f'Bearer {OPENAI_API_KEY}'}
                    files = {'file': (file.filename, file_data, file.content_type), 'model': (None, 'whisper-1')}
                    
                    response = requests.post('https://api.openai.com/v1/audio/transcriptions', headers=headers, files=files)
                    
                    if response.status_code != 200:
                        video_score = 0
                        video_feedback = "OpenAI API Error."
                    else:
                        transcript = response.json().get('text', '').lower()
                        word_count = len(transcript.split())
                        
                        if word_count < 15: 
                            video_score = 0
                            video_feedback = "No speech detected."
                        else:
                            fillers = sum(transcript.count(f) for f in [' um ', ' uh ', ' like ', ' you know '])
                            if 40 <= word_count <= 150: video_score = 92
                            elif word_count > 150: video_score = 75
                            else: video_score = 60
                            
                            if fillers > 3:
                                video_score -= (fillers * 2)
                                video_feedback = f"Used filler words {fillers} times."
                            else:
                                video_feedback = "Excellent verbal delivery."
                except Exception as e:
                    video_score = 0
                    video_feedback = "Error processing video."

    res_score = evaluate_resume(resume_text)
    port_score = evaluate_portfolio(portfolio_url)
    tech_score = evaluate_technical(resume_text, target_role)
    
    # DYNAMIC WEIGHTING
    if has_video and video_score is not None:
        overall_score = int((res_score * 0.35) + (tech_score * 0.30) + (video_score * 0.20) + (port_score * 0.15))
    else:
        # If no video, re-distribute the 20% weight to Resume and Technical
        overall_score = int((res_score * 0.45) + (tech_score * 0.40) + (port_score * 0.15))
    
    feedback = {
        "resume": "Solid structure." if res_score > 80 else "Add more measurable metrics.",
        "portfolio": "Great showcase link." if port_score > 80 else "Missing or invalid portfolio URL (Scored 0).",
        "communication": video_feedback,
        "technical": f"Strong alignment with {target_role}." if tech_score > 80 else f"Missing key {target_role} keywords."
    }
    
    return jsonify({
        'target_role': target_role,
        'overall_score': overall_score,
        'breakdown': {'resume': res_score, 'portfolio': port_score, 'communication': video_score, 'technical': tech_score},
        'feedback': feedback
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
