# 🛠️ AI Technical Support Knowledge Search

A beginner-friendly, clean Django web application designed for academic projects. The application allows users to enter technical support questions, searches an internal SQLite knowledge database using Django ORM keyword lookups, and leverages the **Gemini AI API** to generate beginner-friendly, step-by-step troubleshooting solutions.

---

## 🌟 Key Features

1. **Home Page**: Modern search hero section, quick suggestion pills, category stats, and recent article cards.
2. **AI-Powered Technical Support**: Context-aware Gemini AI answers trained on database articles, formatted into clear markdown sections (*Short Explanation*, *Possible Cause*, *Step-by-Step Solution*, *Recommended Action*).
3. **Database Fallback Mode**: If the Gemini API key is missing or the AI service is offline, the app gracefully presents direct database solutions without crashing.
4. **Knowledge Base Directory**: Full index of technical articles with category filtering and keyword search.
5. **Django Admin Panel**: Full CRUD operations for administrators to add, edit, filter, search, and delete knowledge base articles.
6. **Pre-Seeded Sample Data**: Includes pre-populated articles covering Wi-Fi issues, Windows update failures, printer errors, password resets, Python installation & file errors, VS Code crashes, Git SSH key errors, and more.

---

## 📁 Project Structure

```text
c:/Users/bharg/OneDrive/Desktop/knowledge/
│
├── ai_support/                  # Main Django Project Directory
│   ├── __init__.py
│   ├── settings.py              # App settings, DB config, env loading
│   ├── urls.py                  # Root URL routing
│   ├── wsgi.py                  # WSGI entry point
│   └── asgi.py                  # ASGI entry point
│
├── support/                     # Django Application App
│   ├── __init__.py
│   ├── admin.py                 # Django Admin configuration for KnowledgeArticle
│   ├── apps.py                  # App configuration
│   ├── models.py                # KnowledgeArticle database model definition
│   ├── urls.py                  # App routes (/ask/, /articles/, /articles/<id>/)
│   ├── views.py                 # Core business logic & ORM search queries
│   ├── ai_service.py            # Gemini API integration & offline fallback logic
│   └── management/
│       └── commands/
│           └── seed_db.py       # Custom command to populate initial knowledge articles
│
├── templates/                   # HTML5 Templates (Django Template Language)
│   ├── base.html                # Global layout header, footer, & navigation
│   └── support/
│       ├── home.html            # Main home search page
│       ├── answer.html          # Solution page displaying AI answer & DB articles
│       ├── articles_list.html   # Browse directory with search & category filters
│       └── article_detail.html  # Full article viewer
│
├── static/                      # Static Web Assets
│   ├── css/
│   │   └── style.css            # Vanilla CSS design system (glassmorphism & dark theme)
│   └── js/
│       └── main.js              # Interactive UI scripts (quick query pills & form loader)
│
├── .env                         # Secret environment file (API keys & settings)
├── .env.example                 # Template for environment variables
├── .gitignore                   # Git ignore file (hides .env and db.sqlite3)
├── db.sqlite3                   # SQLite database file
├── manage.py                    # Django management script
├── README.md                    # Project documentation & execution guide
└── requirements.txt             # Python package dependencies
```

---

## 📄 File Explanation

- `support/models.py`: Defines the `KnowledgeArticle` database table schema with fields: `title`, `category`, `problem`, `solution`, `keywords`, `created_at`, `updated_at`.
- `support/admin.py`: Configures the Django Admin Panel interface with category filtering, search bars, and fieldsets.
- `support/views.py`: Implements Django `Q` object search algorithms to query the database and pass context to the views.
- `support/ai_service.py`: Connects to Gemini API using system prompts to restrict answers strictly to database facts, with automatic fallback when offline.
- `support/management/commands/seed_db.py`: Populate command to load real-world technical troubleshooting data into SQLite.
- `static/css/style.css`: Modern UI design using CSS grid/flexbox, custom variables, smooth transitions, and glassmorphic cards.

---

## 🚀 Setup & Execution Guide (VS Code on Windows PowerShell)

Follow these exact step-by-step instructions to set up and run the project:

### Step 1: Open Terminal in VS Code
1. Open **Visual Studio Code**.
2. Open the project folder (`File > Open Folder...` and select `knowledge`).
3. Open a new PowerShell terminal (`Ctrl + ~` or `Terminal > New Terminal`).

### Step 2: Create a Virtual Environment
Run the following command to create an isolated Python virtual environment named `.venv`:
```powershell
python -m venv .venv
```

### Step 3: Activate the Virtual Environment
Activate the virtual environment in PowerShell:
```powershell
.\.venv\Scripts\Activate.ps1
```
*(If PowerShell displays an Execution Policy error, run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` once, then re-run activation).*

### Step 4: Install Project Dependencies
Install all required Python packages (`Django`, `python-dotenv`, `google-genai`, `google-generativeai`):
```powershell
pip install -r requirements.txt
```

### Step 5: Configure Gemini API Key
1. Open the `.env` file located in the root folder.
2. Replace `your_gemini_api_key_here` with your actual Google Gemini API Key:
   ```env
   GEMINI_API_KEY=AIzaSy...your_actual_key_here
   ```
*(Get a free API key from [Google AI Studio](https://aistudio.google.com/)). If left blank or unconfigured, the app will automatically use Offline Database Mode.*

### Step 6: Apply Database Migrations
Create and apply SQLite database tables:
```powershell
python manage.py makemigrations
python manage.py migrate
```

### Step 7: Seed Database with Technical Articles
Populate the SQLite database with 9 sample technical support articles:
```powershell
python manage.py seed_db
```

### Step 8: Create Admin Superuser (Optional)
A default superuser account is already created:
- **Username**: `admin`
- **Password**: `adminpassword123`

To create another superuser manually:
```powershell
python manage.py createsuperuser
```

### Step 9: Run the Local Django Server
Start the development server:
```powershell
python manage.py runserver
```

### Step 10: Access the Application
Open your web browser and navigate to:
- **Main Web Application**: `http://127.0.0.1:8000/`
- **Knowledge Directory**: `http://127.0.0.1:8000/articles/`
- **Django Admin Panel**: `http://127.0.0.1:8000/admin/` (Login with `admin` / `adminpassword123`)

---

## 🔒 Security Best Practices

- Secret key and API keys are strictly loaded from `.env`.
- `.env` is listed in `.gitignore` to prevent secret leaks to public repositories.
- Standard Django CSRF token protection is enabled for all form submissions.
- Input string sanitization and parameter validation are enforced in Django views.
