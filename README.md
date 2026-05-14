# AI CareerForge | UnsaidTalks B2B Assessment Engine

** [WATCH THE 3-MINUTE DEMO VIDEO HERE] ([Insert_Your_Google_Drive_Link_Here](https://drive.google.com/file/d/1kjIOcQMGgkRGjQj2kEATZEWlksOcxfrF/view?usp=sharing))**

## The Vision
Every year, millions of students discover gaps in their interview preparation only after failing the actual interview. AI CareerForge is a robust, B2B white-label engine built for mentorship platforms (like UnsaidTalks) to instantly evaluate candidate readiness across four critical pillars in under 90 seconds.

## The 4 Evaluation Pillars (Problem Statement Delivered)
1. **Technical Skills:** Evaluates candidate text against industry-specific keyword matrices (e.g., Data Science vs. UI/UX).
2. **Resume Quality:** Analyzes formatting, quantifiable metrics (%), and action verbs.
3. **Communication Gaps:** Uses **OpenAI Whisper API** to transcribe uploaded video pitches, analyzing pacing and penalizing filler words ("um", "uh").
4. **Portfolio Setup:** Validates the presence of high-value industry links (GitHub, Behance, etc.).

## Tech Stack
* **Frontend:** React.js, HTML5, CSS3 (Styled to match UnsaidTalks brand guidelines)
* **Backend:** Python, Flask, Flask-CORS
* **Machine Learning & AI:** scikit-learn (Logistic Regression / TF-IDF for role prediction), OpenAI Whisper API (Audio processing)
* **Data Extraction:** PyPDF2

## Dynamic Scoring Engine
The app does not rely on simple AI wrappers. It utilizes a custom Python scoring heuristic. If a candidate skips the optional video pitch, the backend mathematically redistributes the 100-point weight entirely to their Resume and Technical Skills, ensuring realistic scoring at all times.

## How to Run Locally
1. Clone the repository.
2. Install dependencies: `pip install flask flask-cors PyPDF2 requests scikit-learn pandas`
3. Add your OpenAI API key in `app.py` (Line 72).
4. Run the backend engine: `python app.py`
5. Open `index.html` in any modern web browser to access the React dashboard.
