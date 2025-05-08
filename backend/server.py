from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import os
import shutil
import zipfile
import threading
import subprocess
import asyncio
import tempfile  # add at top
import sys  # at top
import dropbox  # Dropbox SDK for upload
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv  # load environment from .env

load_dotenv()

app = FastAPI()
# Allow CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],  # Vite dev server origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global state for logs and graph HTML
logs: list[str] = []
processing = False
graph_html: str = ""

@app.post("/api/upload")
async def upload(file: UploadFile = File(...), email: str = Form(...)):
    """Receive ZIP file and email, start background processing"""
    global logs, processing, graph_html
    # Reset state
    logs.clear()
    graph_html = ""
    processing = True
    logs.append(f"[server] /api/upload called, email={email}, filename={file.filename}")
    # Create an isolated temp directory outside project root to avoid reload triggers
    temp_dir = tempfile.mkdtemp(prefix="code_scribe_")
    logs.append(f"[server] Using system temp directory at {temp_dir}")

    # Save and extract zip
    zip_path = os.path.join(temp_dir, file.filename)
    logs.append(f"[server] Saving uploaded zip to {zip_path}")
    content = await file.read()
    with open(zip_path, 'wb') as f:
        f.write(content)
    logs.append("[server] Zip saved, beginning extraction")
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(temp_dir)
    logs.append("[server] Extraction complete")

    # Start background thread to run main.py
    def run_process():
        global logs, processing, graph_html
        logs.append("[server] Starting background processing thread")
        # Diagnostics: log cwd and script location
        cwd_before = os.getcwd()
        script_path = os.path.abspath(__file__)
        backend_dir = os.path.dirname(script_path)
        logs.append(f"[server] cwd before launch: {cwd_before}")
        logs.append(f"[server] server.py path: {script_path}")
        logs.append(f"[server] using backend_dir: {backend_dir}")
        try:
            # Use the same Python interpreter and absolute script path
            python_exec = sys.executable or 'python'
            main_script = os.path.join(backend_dir, 'main.py')
            logs.append(f"[server] Launching subprocess: {python_exec} -u {main_script}")
            proc = subprocess.Popen(
                [python_exec, '-u', main_script],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                env=os.environ
            )
        except Exception as ex:
            logs.append(f"[server] Failed to start subprocess: {ex}")
            processing = False
            return
        # Provide project root input
        proc.stdin.write(temp_dir + '\n')
        proc.stdin.flush()
        logs.append(f"[server] Provided project root to subprocess: {temp_dir}")
        # Read output lines
        for line in proc.stdout:
            logs.append(line.strip())
            # Update graph HTML if file exists
            html_file = f"{temp_dir}.html"
            logs.append(f"[server] Checking for graph HTML file at location: {temp_dir}")
            if os.path.exists(html_file):
                try:
                    with open(html_file, 'r', encoding='utf-8') as hf:
                        graph_html = hf.read()
                except Exception:
                    pass
        proc.wait()
        logs.append(f"[server] Subprocess completed with exit code {proc.returncode}")
        processing = False

        # Create a zip of the documented project for download
        result_zip = f"{temp_dir}.zip"
        logs.append(f"[server] Creating result ZIP at {result_zip}")
        shutil.make_archive(temp_dir, 'zip', temp_dir)
        logs.append("[server] Result ZIP created")

        # Upload result ZIP to Dropbox and get shareable link
        dropbox_token = os.getenv('DROPBOX_ACCESS_TOKEN')
        if not dropbox_token:
            logs.append("[server] ERROR: DROPBOX_ACCESS_TOKEN is not set in the environment")
            return
        dbx = dropbox.Dropbox(dropbox_token)
        dest_path = '/' + os.path.basename(result_zip)
        with open(result_zip, 'rb') as f:
            dbx.files_upload(f.read(), dest_path, mute=True)
        shared_url = dbx.sharing_create_shared_link_with_settings(dest_path).url
        link = shared_url.replace('?dl=0', '?dl=1')  # direct download link
        logs.append(f"[server] Uploaded to Dropbox: {link}")

        # Send email notification with MEGA link
        email_subject = "Your documented code is ready"
        email_body = f"Your code has been documented. Download it here: {link}"
        send_email(email, email_subject, email_body)
        logs.append(f"[server] Sent email notification to {email}")

    thread = threading.Thread(target=run_process, daemon=True)
    thread.start()
    return {"message": "Processing started"}

@app.get("/api/logs")
def get_logs():
    """Return current logs and processing status"""
    try:
        return {"logs": logs, "processing": processing}
    except Exception as e:
        # On error, return empty logs, not processing
        return JSONResponse(status_code=200, content={"logs": [], "processing": False})

@app.get("/api/graph")
def get_graph():
    """Return latest graph HTML"""
    try:
        return HTMLResponse(content=graph_html, status_code=200)
    except Exception:
        # On error return empty content
        return HTMLResponse(content="", status_code=200)

def send_email(recipient_email: str, subject: str, body_text: str):
    """Send a simple plaintext email via SMTP using environment vars"""
    smtp_server = os.getenv('SMTP_SERVER')
    smtp_port = int(os.getenv('SMTP_PORT', '587'))
    smtp_user = os.getenv('SMTP_USER')
    smtp_password = os.getenv('SMTP_PASSWORD')
    msg = MIMEText(body_text)
    msg['Subject'] = subject
    msg['From'] = smtp_user
    msg['To'] = recipient_email
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_user, smtp_password)
        server.send_message(msg)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)