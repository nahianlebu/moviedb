<p align="center">
  <img src="assets/clapper_gh.png" width=40%>
  <h1 align="center">MOVIE RATING DATABASE MANAGEMENT SYSTEM</h1>
</p>
<p align="justify">
A web based movie rating management system for the <b>Database Management System Lab (CSE312)</b> Course.
This project has been done under the <b><i>guidance</i></b> & <b><i>enlightment</i></b> by <a href="https://github.com/DIP-RO">Dipro Paul</a> (Lecturer at DIU) Sir. 
</p>

## Team Members

| ID         | Name                   |
| ---------- | ---------------------- |
| 242-15-173 | MD. NAHIAN LABIB LIMON |
| 242-15-831 | MOHAMMED SAKIN KHAN    |
| 242-15-361 | MD. FAHIM SHAHRIAR     |
| 242-15-454 | MST. HUMAYRA AFROZ MIM |

## Features

- Browse & search movies by title, genre, or director
- Full CRUD operations
- Rate movies on 5 criteria (story, acting, visual, sound, direction)
- Delete individual ratings
- Overall rating auto-computed by a **TRIGGER**
- Top-rated leaderboard powered by a SQL **VIEW** (`AVG` + `GROUP BY`)
- Modern, responsive & simple UI

# Project Structure

```
.
├── .github
│   └── workflows
│       └── ci.yaml
├── LICENSE
├── main.py
├── pyproject.toml
├── README.md
├── requirements.txt
├── schema.sql
└── templates
    ├── add.html
    ├── base.html
    ├── index.html
    ├── movie.html
    └── top.html

```

# Build & Run

## Prerequisite

- Python 3.14
- MYSQL Server 8

## Build

### Download the Project from Github (as zip) or using git:

```bash
git clone https://github.com/nahianlebu/moviedb.git
cd moviedb
```

### Set up virtual environment

```bash
# for windows
python -m venv .venv
.venv\Scripts\activate

# for mac or linux(i use fedora btw)
python3 -m venv .venv
source .venv/bin/activate

```

### Install dependency

```bash
pip install -r requirements.txt
```

### Load Database

```bash
mysql -u root -p < schema.sql
```

### Execute

```
# For windows
python main.py

# For mac/linux
python3 main.py
```

## Launch

Finally, Launch from any browser by just entering this url http://127.0.0.1:5000
