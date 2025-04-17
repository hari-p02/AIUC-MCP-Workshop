# AI User Conference
## Developer Day: Workshop 3 @ 12:00PM - Hari Patchigolla

Link to Workshop: https://www.aiuserconference.com/speaker/hari-patchigolla

Video Recording: (Coming Soon!)

### Overview

In this 50 minute workshop we will go over the conceptual topics regarding MCPs and then go into creating our own MCP Clients and Servers using `mcp[cli]`, `FastMCP`, and `PaydanticAI` with `LogFire`! More specifically we will see how MCP address the current limitations of LLMs bound to tools with a real example of creating an Agentic perosnal finance system!

### Set Up

1. Git Clone this repository:

```
git clone https://github.com/hari-p02/AIUC-MCP-Workshop.git
cd AIUC-MCP-Workshop
```

2. Sync with `uv`:

```
uv sync
```

3. Create a `.env` file in the root directory of the repository:

```
ANTHROPIC_API_KEY=
GOOGLE_CREDENTIALS_FILE=
GOOGLE_SHEETS_ID=
LOGFIRE_TOKEN=
SERVER_DETAILS=../server/server_details.yaml
```

4. Create OAuth 2 Secrets from Google: [Video Tutorial](https://www.youtube.com/watch?v=OKMgyF5ezFs&pp=ygUrY3JlYXRpbmcgT0F1dGgyIHNlY2VydHMgZnJvbSBnb2dvbGUgZm9yIGFwaQ%3D%3D)

5. Enable the Gmail, Docs, Sheets, and Drive APIs

6. Copy the path to the downloaded `.json` credentials and save it in `GOOGLE_CREDENTIALS_FILE` on the `.env` file

7. Create a free LogFire account [here](https://logfire.pydantic.dev/).

8. Once you make an account you will get a token, this will be the value of `LOGFIRE_TOKEN` in the `.env` file.

9. Run `logfire auth` on the terminal, and you will be prompted to log in

10. Create a new google sheet **in the same account as your OAuth Credentials**!

11. Copy the sheet id (in the url) and set it to `GOOGLE_SHEETS_ID` in the `.env` file.

12. Download [this Personal Finance dataset](https://www.kaggle.com/datasets/bukolafatunde/personal-finance) from kaggle

13. Cope the contents of `personal_transactions.csv` into the google sheet you made above.

14. Delete the `Transation Type` and `Account Name` columns.

15. Make sure all the columns are in a row!!!
