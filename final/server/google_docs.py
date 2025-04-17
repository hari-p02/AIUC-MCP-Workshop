from mcp.server.fastmcp import FastMCP
from utils.startlette import create_starlette_app
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from dotenv import load_dotenv
load_dotenv("../../.env")


SCOPES = ['https://www.googleapis.com/auth/documents']

flow = InstalledAppFlow.from_client_secrets_file(os.getenv("GOOGLE_CREDENTIALS_FILE"), SCOPES)
creds = flow.run_local_server(port=0)
service = build('docs', 'v1', credentials=creds)

mcp = FastMCP("finance-mail-server")

@mcp.tool()
def create_report(title: str, content: str) -> str:
    """
    Creates a new report with the given title and content
    Args:
        title: The title of the report
        content: The content of the report
    """
    doc = service.documents().create(body={'title': title}).execute()
    doc_id = doc.get('documentId')
    print(f'Document created! View at: https://docs.google.com/document/d/{doc_id}/edit')
    requests = [{
        'insertText': {
            'location': {'index': 1},
            'text': content
        }
    }]
    service.documents().batchUpdate(documentId=doc_id, body={'requests': requests}).execute()
    return f"Report created successfully with document id: {doc_id}"

if __name__ == "__main__":
    mcp_server = mcp._mcp_server
    import uvicorn
    starlette_app = create_starlette_app(mcp_server, debug=True)
    uvicorn.run(starlette_app, host="localhost", port=8030)