# Apriori Algorithm Web Application

This is my **Master’s Project** in Computer Science (CIS 550: Intro to Algorithms).  
It is a **Flask-based web application** that implements the **Apriori Algorithm** for mining frequent itemsets from transaction datasets.  

The app allows you to upload a CSV dataset, set a minimum support threshold, and view the **maximal frequent itemsets** discovered.

---

## 🚀 Features

- Upload CSV transaction data
- Accepts **integer** or **fractional** minimum support (e.g., `2` or `0.3`)
- Displays **maximal frequent itemsets** in a formatted output
- Shows **total itemsets** and **execution time**
- Includes `/health` endpoint for deployment monitoring
- Runs locally or deployed on **Render**

---
## 🔧 Tech Stack

- Backend: Flask (Python 3)
- Algorithm: Apriori (custom implementation)
- Frontend: HTML, CSS
- Deployment: Render + Gunicorn

---

## 📂 Project Structure
Apriori-Algorithm-Project/
│
├── apriori_shaikhovesh_app.py # Flask web app
├── apriori_123456.py # Apriori algorithm implementation
├── requirements.txt # Dependencies
├── templates/
│ ├── index.html # Upload form
│ └── output.html # Results page
├── static/
│ └── style.css # Styling
└── uploads/ # Local uploads (Render uses /tmp)

---

## ⚙️ Installation & Setup (Local)

1. **Clone the repo**
   ```bash
   git clone https://github.com/oveshshaikh786/Apriori-Algorithm-Project.git
   cd Apriori-Algorithm-Project

2. Create and activate virtual environment
   ```bash
   python -m venv .venv
   source .venv/Scripts/activate   # Windows
 # OR
   source .venv/bin/activate       # macOS/Linux

3. Install dependencies
   ```bash
     pip install -r requirements.txt

4. Run Flask app
   ```bash
     flask --app apriori_shaikhovesh_app run

5. Open browser → http://127.0.0.1:5000


## 🌐 Deployment on Render
1. Push this repo to GitHub.
2. On Render, create a New Web Service:

- Build Command:
  ```bash
     pip install -r requirements.txt

- Start Command:
  ```bash
     gunicorn apriori_shaikhovesh_app:app

- Environment Variables:
     RENDER=true
     SECRET_KEY=your_random_secret

3. Health check path: /health
4. Visit your Render URL (e.g. https://apriori-algorithm-project.onrender.com).


## 🧪 Example Input
- CSV File (sample.csv):
milk,bread
bread,eggs
milk,eggs,bread
milk
eggs

- Minimal Support: 2

📊 Example Output
{ {milk, bread} {eggs, bread} {milk, eggs} }

- End - total items: 3
- Elapsed Time: 0.002 seconds


## ✨ Author
- 👨‍💻 Ovesh Shaikh
- 📧 oveshshaikh814@gmail.com

