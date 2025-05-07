🧪 WikiPytestRepo
Automated UI testing project using Playwright, Pytest, and Allure Reports.
This project focuses on end-to-end testing of a Wikipedia-like interface, including UI preferences, search behavior, and session management using cookies.

📁 Project Structure
wikiPytestRepo/
├── tests/                   # All test files
│   ├── test_homePage.py
│   └── test_search.py
├── login.py                 # Script to generate or load login.json with Playwright cookies
├── login.json              # Session state file (Playwright storage), stored in the root
├── .env                    # Your Wikipedia credentials (not committed)
├── pytest.ini              # Pytest configuration (runs tests only from ./tests)
├── requirements.txt
└── README.md
🚀 Setup Instructions
Create virtual environment:
python -m venv .venv
source .venv/bin/activate  
# On Windows: .venv\Scripts\activate
Install dependencies:
pip install -r requirements.txt
Install Playwright browsers:
playwright install
**Create a .env file in the project root and add your Wikipedia login credentials:
WIKIPEDIA_USERNAME=your_username WIKIPEDIA_PASSWORD=your_password

🧠 Usage Guide
✅ Run login.py to create cookies
pytest login.py
✅ Run all the tests
pytest
🧁 Generate Allure Reports
Run createAllureReportWindows.bat to create an Allure report in Windows or Run create_allure_reportLinux_Mac.sh to create an Allure report in Linux/Mac

⚠️ Make sure allure is installed and added to your system PATH. You can download Allure CLI here.

🔐 Login Session (login.json)
The project uses Playwright's storage state to persist sessions.

The login.json file should be placed in the root folder, not inside tests/.
All tests will reference it using a relative path to the root: ../login.json.
To generate a new login session, run:

python login.py
⚙️ pytest.ini Configuration
[pytest]
testpaths = tests
addopts = --alluredir=allure-results
📦 Dependencies
Minimal required dependencies in requirements.txt:

pytest
pytest-playwright
playwright
python-dotenv
allure-pytest
📄 License
MIT License
