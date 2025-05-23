# 📰 Information Agency
[🌐 Visit the Website](https://info-agency.onrender.com)

This system helps track which editors are responsible for each newspaper issue.  
It also allows assigning one or more topics to each newspaper — making it easier for planning and content analysis.

---

## 🚀 Features

- Creating, editing, and deleting newspapers
- Assigning editors to each issue
- Adding topics to newspapers (one or more)
- Viewing all editors, newspapers, and topics
- Searching for newspapers and authors using filters
- User authentication
- Django admin panel for management

---

## 🛠 Technologies

- Python 3.x  
- Django 4.x  
- SQLite (default)
- Bootstrap 5  
- Django Crispy Forms

---

## ⚙️ Installation

```bash
1. Clone the project

git clone https://github.com/apmaz/info-agency.git
cd info-agency

2. If you are using PyCharm, it might suggest automatically creating a venv and installing requirements, but if not:
python -m venv venv
venv\Scripts\activate (on Windows)
source venv/bin/activate (on macOS)
pip install -r requirements.txt

3. Run migrations
python manage.py migrate

4. Use the following command to load prepared data from a fixture to get more familiar with the Information Agency system:
python manage.py loaddata information_agency_db_data.json

You can use the following test user:
- Login: test_user
- Password: SQ817Drt

5. Run the server
python manage.py runserver
```

---

## 🧩 Main Models

### 🏷 Topic
- **name** — title of the topic

### 👤 Redactor (AbstractUser)
- **years_of_experience** — years of experience

### 📄 Newspaper
- **title** — title of the newspaper  
- **content** — content of the newspaper  
- **published_date** — publication date  
- **topic** — many-to-many relationship with the `Topic` model  
- **publishers** — many-to-many relationship with the `Redactor` model

![diagram](docs/diagram.png)

---

## 📌 Examples of Use

![image](docs/01_home_page.png)
![image](docs/02_topics_page.png)
![image](docs/03_redactors_page.png)
![image](docs/04_newspapers_page.png)

---

## 🧪 Running Tests

```bash
To run tests, enter:
python manage.py test
```

---