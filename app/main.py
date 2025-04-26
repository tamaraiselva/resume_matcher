import os
import uuid
import logging
from typing import List

from fastapi import FastAPI, File, UploadFile, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR

from dotenv import load_dotenv
import markdown

from langchain.docstore.document import Document
from langchain.prompts import PromptTemplate
from langchain.chains.llm import LLMChain
from langchain.chains import StuffDocumentsChain
from langchain_community.document_loaders import (
    PyPDFLoader,
    UnstructuredCSVLoader,
    UnstructuredExcelLoader,
    Docx2txtLoader,
    UnstructuredPowerPointLoader,
    UnstructuredFileLoader,
)
from langchain_google_genai import ChatGoogleGenerativeAI
import google.generativeai as genai

load_dotenv()

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s]: %(message)s")

API_KEY = os.getenv("GOOGLE_API_KEY")
if not API_KEY:
    raise EnvironmentError("Missing GOOGLE_API_KEY in .env")

genai.configure(api_key=API_KEY)
GEMINI_MODEL = "gemini-2.0-flash"
llm = ChatGoogleGenerativeAI(model=GEMINI_MODEL, google_api_key=API_KEY)

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


def select_loader(file_path: str):
    ext = file_path.lower()
    if ext.endswith(".pdf"):
        return PyPDFLoader(file_path)
    elif ext.endswith(".docx"):
        return Docx2txtLoader(file_path)
    elif ext.endswith(".csv"):
        return UnstructuredCSVLoader(file_path)
    elif ext.endswith(".xlsx"):
        return UnstructuredExcelLoader(file_path)
    elif ext.endswith(".pptx"):
        return UnstructuredPowerPointLoader(file_path)
    return UnstructuredFileLoader(file_path)


@app.get("/", response_class=HTMLResponse)
async def upload_form():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Resume Matcher</title>
        <link rel="icon" href="/static/logo.png" type="image/png">
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">
        <style>
            body {
                background: linear-gradient(to right, #e9f3df, #ffffff);
                min-height: 100vh;
                background-size: cover;
            }
            .img-col {
                background-image: url('/static/image.png');
                background-size: contain;
                background-repeat: no-repeat;
                background-position: center;
                min-height: 500px;
            }
        </style>
    </head>
    <body>
        <div class="container-fluid">
            <div class="row min-vh-100">
                <div class="col-md-6 d-flex flex-column justify-content-center p-5">
                    
                    <h2 class="mb-4">Resume Matcher</h2>
                    <form action="/analyze/" enctype="multipart/form-data" method="post">
                        <div class="mb-3 text-start">
                            <label class="form-label">Job Description</label>
                            <textarea class="form-control" name="prompt" rows="6" required></textarea>
                        </div>
                        <div class="mb-3 text-start">
                            <label class="form-label">Upload Resumes (PDF/DOCX)</label>
                            <input class="form-control" type="file" name="files" multiple required>
                        </div>
                        <button type="submit" class="btn btn-primary">Analyze</button>
                    </form>
                </div>
                <div class="col-md-6 img-col d-none d-md-block"></div>
            </div>
        </div>
    </body>
    </html>
    """


@app.post("/analyze/", response_class=HTMLResponse)
async def analyze_resumes(files: List[UploadFile] = File(...), prompt: str = Form(...)):
    task_id = str(uuid.uuid4())
    logging.info(f"Start resume analysis: Task {task_id}")
    os.makedirs("static", exist_ok=True)
    results = []

    try:
        file_paths = []
        for file in files:
            path = os.path.join("static", f"{task_id}_{file.filename}")
            with open(path, "wb") as f:
                f.write(await file.read())
            file_paths.append(path)

        docs = []
        for path in file_paths:
            loader = select_loader(path)
            chunks = loader.load()
            full_text = "\n".join(chunk.page_content for chunk in chunks)
            docs.append(Document(page_content=full_text))

        template = PromptTemplate.from_template(f"""
        You are an expert at analyzing resumes against a job description.

        Job Description:
        {prompt}

        Resume Content:
        {{text}}

        Instructions:
        - Analyze how well the resume matches the job description.
        - Identify key skills, experience, and qualifications.
        - Provide a match score out of 10.
        - Explain the score briefly.

        Return the final score and explanation clearly.
        """)

        for idx, doc in enumerate(docs):
            logging.info(f"Analyzing Candidate {idx+1}")
            llm_chain = LLMChain(llm=llm, prompt=template)
            stuff_chain = StuffDocumentsChain(
                llm_chain=llm_chain,
                document_variable_name="text"
            )
            output = stuff_chain.invoke([doc])
            results.append(output["output_text"])

    except Exception as e:
        logging.error(f"Processing error: {str(e)}")
        return HTMLResponse(content=f"<h3>Error: {str(e)}</h3>", status_code=500)

    finally:
        for path in file_paths:
            try:
                os.remove(path)
            except Exception as e:
                logging.warning(f"Failed to delete {path}: {e}")

    html_results = "<h3 class='mb-3'>Candidate Rankings</h3><ul class='list-group'>"
    for idx, res in enumerate(results, 1):
        html_results += f"""
        <li class='list-group-item'>
            <strong>Candidate {idx}</strong><br>
            {markdown.markdown(res)}
        </li>"""
    html_results += "</ul><br><a href='/' class='btn btn-secondary'>Back</a>"

    return HTMLResponse(content=f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Results - Resume Matcher</title>
        <link rel="icon" href="/static/logo.png" type="image/png">
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">
        <style>
            body {{
                background: linear-gradient(to right, #e9f3df, #ffffff);
                min-height: 100vh;
                background-repeat: no-repeat;
                background-size: cover;
            }}
        </style>
    </head>
    <body class="bg-light">
        <div class="container py-5 text-center">
            
            <h2 class="mb-4">Resume Matcher</h2>
            <form action="/analyze/" enctype="multipart/form-data" method="post">
                <div class="mb-3 text-start">
                    <label class="form-label">Job Description</label>
                    <textarea class="form-control" name="prompt" rows="6" required>{prompt}</textarea>
                </div>
                <div class="mb-3 text-start">
                    <label class="form-label">Upload Resumes</label>
                    <input class="form-control" type="file" name="files" multiple required>
                </div>
                <button type="submit" class="btn btn-primary">Analyze</button>
            </form>
            <div class="mt-5 text-start">{html_results}</div>
        </div>
    </body>
    </html>
    """)


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logging.exception("Unhandled exception:")
    return JSONResponse(
        status_code=HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Internal Server Error. Please try again."},
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")
