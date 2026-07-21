# 🏏 CricVision Pro – India ODI Cricket Analytics (2021–2026)

## 📖 Overview

**CricVision Pro** is a Flask-based cricket analytics platform that provides detailed insights into the performance of the Indian Men's ODI cricket team from **2021 to June 2026**.

The project automatically extracts match data from Cricsheet JSON files, processes batting, bowling, partnership, and match statistics using Python and Pandas, stores the processed data as CSV files, and presents interactive visualizations through a modern Flask web application powered by Plotly.

---

## ✨ Features

### 🏠 Home Page

* Project introduction
* Featured Indian players
* Navigation to players and dashboard
* Quick project overview

### 👥 Players

* Complete list of Indian players
* Individual player profile pages

### 👤 Player Profile

* Career batting statistics
* Career bowling statistics
* Runs against each opponent
* Batting average against opponents
* Wickets against opponents
* Runs scored by year
* Wickets taken by year
* Interactive Plotly charts

### 📊 Dashboard

* Overall team performance
* Top run scorer
* Top wicket taker
* Best all-rounder
* Top 10 batters
* Top 10 bowlers
* Year-wise runs
* Year-wise wickets
* Match result distribution
* Win percentage against opponents
* Win percentage at different venues

---

# 📂 Project Structure

```text
CricVision-Pro/
│
├── app.py                     # Flask application
├── odi.py                     # Extract India ODI matches from Cricsheet
├── filtering.py               # Generate batting, bowling and partnership data
│
├── india.json
├── Batting.csv
├── Bowling.csv
├── Partnership.csv
├── Matches.csv
├── players.csv
│
├── templates/
│   ├── home.html
│   ├── players.html
│   ├── player_profile.html
│   ├── dashboard.html
│   └── about.html
│
├── static/
│   ├── style.css
│   ├── images/
│   └── javascript/
│
└── README.md
```

---

# ⚙️ Data Pipeline

The project consists of three major stages.

## Step 1 — Download Match Data

Download ODI JSON files from **Cricsheet**.

Required datasets:

* All Men's ODI Matches
* ICC Men's Cricket World Cup

---

## Step 2 — Filter India Matches

Run

```bash
python odi.py
```

This script

* Reads all JSON files from ZIP archives
* Filters:

  * India matches
  * Men's cricket
  * ODI format
  * Date ≥ 2021-01-01
* Creates

```text
india.json
```

---

## Step 3 — Generate Scorecards

Run

```bash
python scorecard.py
```

This script generates

* Batting.csv
* Bowling.csv
* Partnership.csv
* Matches.csv

using ball-by-ball match data.

---

## Step 4 — Launch Website

```bash
python app.py
```

Open

```
http://127.0.0.1:5000
```

---

# 📊 Dataset

The project analyzes

* Indian Men's ODI matches
* From January 2021
* Until June 2026

Data Source:

**Cricsheet**

---

# 🛠️ Technologies Used

### Backend

* Python
* Flask

### Data Processing

* Pandas
* JSON
* ZipFile

### Visualization

* Plotly Express

### Frontend

* HTML5
* CSS3
* Jinja2

---

# 📈 Analytics Generated

## Batting

* Runs
* Balls
* Strike Rate
* Fours
* Sixes
* Dot Balls
* Batting Average
* Fifties
* Hundreds
* Not Outs

---

## Bowling

* Wickets
* Economy
* Bowling Average
* Maidens
* Five Wicket Hauls
* Overs Bowled

---

## Team Statistics

* Match Results
* Win Percentage
* Venue Performance
* Opponent Performance
* Player of the Match
* Toss Winner

---

## Partnership Analysis

* Batter 1
* Batter 2
* Partnership Runs
* Partnership Balls

---

# 📸 Screenshots

Add screenshots of:

* Home Page
* Dashboard
* Player Profile
* Top Batters
* Top Bowlers

Example

```
screenshots/
    home.png
    dashboard.png
    player.png
```

---

# 🚀 Future Improvements

* Live match integration
* Player comparison
* Head-to-head analysis
* Advanced bowling analytics
* Partnership network visualization
* Search functionality
* Team comparison
* Match timeline analysis
* Responsive mobile dashboard
* AI-powered performance prediction

---

# 📚 Learning Outcomes

This project demonstrates practical knowledge of

* Flask
* Pandas
* Data Cleaning
* Data Aggregation
* Cricket Analytics
* Plotly Visualization
* Jinja Templates
* JSON Processing
* REST-style Routing
* Dashboard Development

---

# 👨‍💻 Author

**Pardhu**

B.Tech CSE Student

Aspiring AI & Data Science Engineer

---

# ⭐ If you found this project useful

Please consider giving the repository a **Star ⭐**.
