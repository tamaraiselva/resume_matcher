# Resume Matcher

![Resume Matcher Logo](static/logo.png)

A powerful tool that uses AI to match resumes against job descriptions, providing a match score and detailed analysis.

## Features

- **Resume Analysis**: Upload multiple resumes and match them against a job description
- **Multiple File Formats**: Supports PDF, DOCX, CSV, XLSX, and PPTX files
- **AI-Powered Matching**: Uses Google's Gemini 2.0 Flash model to analyze and score resumes
- **Detailed Feedback**: Provides match scores and explanations for each candidate
- **Simple Interface**: Clean, user-friendly web interface

## Technology Stack

- **Backend**: FastAPI
- **AI/ML**: LangChain + Google Gemini AI
- **Frontend**: HTML, Bootstrap CSS
- **Document Processing**: Various document loaders for different file formats

## Prerequisites

- Python 3.8+
- Google Gemini API key

## Installation

1. Clone the repository:

   ```git
   git clone https://github.com/tamaraiselva/resume-matcher-enhancement.git
   cd resume-matcher-enhancement
   ```

2. Create a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:

   ```python
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the root directory with your Google API key:

   ```bash
   GOOGLE_API_KEY = "your_google_api_key_here"
   ```

## Development Usage

1. Start the development server:

   ```python
   python app.py
   ```

2. Open your browser and navigate to:

   ```cmd
   http://127.0.0.1:8000
   ```

3. Enter a job description in the text area.

4. Upload one or more resumes (PDF, DOCX, etc.).

5. Click "Analyze" to process the resumes.

6. View the results with match scores and detailed analysis for each candidate.

## Production Deployment

1. Install Gunicorn (production WSGI server):

   ```bash
   pip install gunicorn
   ```

2. Create a systemd service file (Linux systems):

   ```bash
   sudo nano /etc/systemd/system/resume-matcher.service
   ```

   Add the following content:

   ```ini
   [Unit]
   Description=Resume Matcher Gunicorn Service
   After=network.target

   [Service]
   User=your_username
   Group=your_group
   WorkingDirectory=/path/to/resume-matcher-enhancement
   Environment="PATH=/path/to/resume-matcher-enhancement/venv/bin"
   Environment="GOOGLE_API_KEY=your_google_api_key_here"
   ExecStart=/path/to/resume-matcher-enhancement/venv/bin/gunicorn -w 4 -k uvicorn.workers.UvicornWorker app:app -b 0.0.0.0:8000

   [Install]
   WantedBy=multi-user.target
   ```

3. Start and enable the service:

   ```bash
   sudo systemctl start resume-matcher
   sudo systemctl enable resume-matcher
   ```

4. Install and configure Nginx as reverse proxy:

   ```bash
   sudo apt install nginx
   sudo nano /etc/nginx/sites-available/resume-matcher
   ```

   Add the following configuration:

   ```nginx
   server {
       listen 80;
       server_name your_domain.com;

       location / {
           proxy_pass http://127.0.0.1:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }

       location /static/ {
           alias /path/to/resume-matcher-enhancement/static/;
       }
   }
   ```

5. Enable the site and restart Nginx:

   ```bash
   sudo ln -s /etc/nginx/sites-available/resume-matcher /etc/nginx/sites-enabled/
   sudo nginx -t
   sudo systemctl restart nginx
   ```

6. Access your application at `http://your_domain.com`

## How It Works

1. The application accepts a job description and multiple resume files.
2. Each resume is processed and converted to text using appropriate document loaders.
3. The LangChain framework with Google's Gemini AI analyzes each resume against the job description.
4. The AI provides a match score out of 10 and explains the reasoning behind the score.
5. Results are displayed in a clean, easy-to-read format.

## Future Enhancements

- Streamlit interface option
- Batch processing for large numbers of resumes
- Export results to PDF or CSV
- More detailed analysis with skill matching
- User accounts and saved job descriptions

## License

[MIT License](LICENSE)

## Acknowledgements

- Google Generative AI
- LangChain Framework
- FastAPI
- Bootstrap CSS
