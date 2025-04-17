from mcp.server.fastmcp import FastMCP
from utils.startlette import create_starlette_app
import base64
from email.message import EmailMessage
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os
from oauth2client.service_account import ServiceAccountCredentials
from google.oauth2 import service_account
from googleapiclient.discovery import build
from email.mime.text import MIMEText
from dotenv import load_dotenv
load_dotenv("../../.env")


SCOPES = ['https://www.googleapis.com/auth/gmail.send']

flow = InstalledAppFlow.from_client_secrets_file(os.getenv("GOOGLE_CREDENTIALS_FILE"), SCOPES)
creds = flow.run_local_server(port=0)
service = build('gmail', 'v1', credentials=creds)

mcp = FastMCP("finance-mail-server")

@mcp.tool()
def send_email(subject: str, message: str) -> str:
    """
    Sends an email to the user
    Args:
        subject: The subject of the email
        message: The body of the email
    """
    print(f"Sending email with subject: {subject} and message: {message}")
    message = MIMEText(message)
    message['to'] = 'aiuc.mcp.demo@gmail.com'
    message['subject'] = subject
    create_message = {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}
    sent_message = service.users().messages().send(userId="me", body=create_message).execute()
    return "Email sent successfully"

if __name__ == "__main__":
    mcp_server = mcp._mcp_server
    import uvicorn
    starlette_app = create_starlette_app(mcp_server, debug=True)
    uvicorn.run(starlette_app, host="localhost", port=8020)