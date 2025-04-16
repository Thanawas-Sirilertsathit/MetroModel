## Steps to Install Weather x Metro Passenger Analysis

### 1. Clone the GitHub repository
```bash
git clone https://github.com/Thanawas-Sirilertsathit/MetroModel.git
```

### 2. Change directory to the project root
```bash
cd MetroModel
```

### 3. Create a Python virtual environment
```bash
python -m venv .venv
```

### 4. Activate the virtual environment
```bash
.venv\Scripts\activate        # On Windows
```
```bash
source .venv/bin/activate     # On macOS/Linux
```

### 5. Install backend dependencies
```bash
pip install -r requirements.txt
```

### 6. Configure environment variables
Rename or copy the `sample.env` to `.env` inside the `backend/` folder and update the values:

```env
DB_HOST=iot.cpe.ku.ac.th
DB_NAME=project
DB_USER=your_database_user
DB_PASSWORD=your_database_password
```

### 7. Apply Django migrations
```bash
cd backend
python manage.py migrate
```



### 8. Run the Django backend server
```bash
python manage.py runserver
```
Accessible at: [http://localhost:8000](http://localhost:8000)

---

## 🌐 Frontend 

### 9. Navigate to frontend folder
```bash
cd ../frontend
```

### 10. Configure environment variables
Rename or copy the `sample.env` to `.env` inside the `frontend/` folder:
```env
VUE_APP_BASE_URL = http://127.0.0.1:8000
```


### 11. Install frontend dependencies
```bash
npm install
```



### 12. Start the frontend development server
```bash
npm run serve
```
Accessible at: [http://localhost:8080](http://localhost:8080)

---

