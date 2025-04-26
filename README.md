# Resume Matcher

![Resume Matcher Logo](static/logo.png)

A modern web application that uses Google's Gemini AI to analyze and match resumes against job descriptions. Built with FastAPI and LangChain, this tool helps recruiters and hiring managers efficiently evaluate candidate resumes.

## Features

- **Smart Resume Analysis**: Leverages Google's Gemini AI to analyze resumes against job descriptions
- **Multiple Format Support**: Handles various file formats including PDF, DOCX, CSV, XLSX, and PPTX
- **Batch Processing**: Upload and analyze multiple resumes simultaneously
- **Scoring System**: Provides a match score out of 10 with detailed explanations
- **Clean UI**: Modern, responsive interface built with Bootstrap
- **Real-time Processing**: Instant feedback on resume matches

## Prerequisites

- Python 3.8 or higher
- Google API Key for Gemini AI

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/resume_matcher.git
cd resume_matcher
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the project root and add your Google API key:
```env
GOOGLE_API_KEY=your_api_key_here
```

## Usage

1. Start the application:
```bash
python app/main.py
```

2. Open your browser and navigate to `http://localhost:10000`

3. Enter the job description and upload resumes (PDF/DOCX format)

4. Click "Analyze" to get detailed matching results

## Project Structure

```bash
resume_matcher/
├── app/
│   └── main.py          # Main application file
├── static/              # Static files (images, etc.)
├── .env                 # Environment variables
└── requirements.txt     # Project dependencies
```

## Dependencies

- `FastAPI:` Web framework for building APIs
- `LangChain:` Framework for developing applications powered by language models
- `Google Generative AI:` Access to Google's Gemini model
- `Python-Multipart:` Handling file uploads
- `Python-dotenv:` Managing environment variables
- Various document loaders for different file formats

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.