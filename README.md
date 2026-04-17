# PitchLab API: Arsenal Optimization & Pitch Design MVP

PitchLab is a backend architecture proof-of-concept designed to manage and evaluate minor league pitcher development. It provides a RESTful API to track bullpen sessions, log pitch movement profiles (Velocity, Spin Rate, IVB), and structurally associate those metrics with individual pitcher profiles.

## ⚾ The Product Vision
"Get Players Better." 
While game-level data is useful, player development requires tracking high-frequency, granular repetitions inside a controlled environment (the bullpen). This MVP focuses on the backend data architecture necessary to ingest tracking data (e.g., TrackMan or Rapsodo) and serve it to development coaches for arsenal optimization. 

## 🏗️ Architecture & Tech Stack
* **Backend Framework:** Python, FastAPI 
* **Database:** SQLite (MVP) via SQLAlchemy ORM
* **Data Validation:** Pydantic
* **DevOps:** Docker, Docker Compose

## 🧮 Engineering Decisions
1. **Relational Data Modeling:** Architected a One-to-Many relationship between `Pitchers` and `BullpenSessions`. This allows the API to seamlessly retrieve a pitcher's entire historical movement profile in a single query.
2. **Database-Layer Aggregation:** Designed a `/analytics` endpoint that pushes computational heavy lifting (averages, pitch counts) down to the database layer via SQLAlchemy, optimizing API performance for large sports datasets.
3. **Containerization:** The application is fully Dockerized to ensure parity across local development and cloud production environments, mitigating "it works on my machine" issues.
4. **Auto-Generated Documentation:** Leveraging FastAPI, the API automatically generates OpenAPI (Swagger) documentation, creating an immediate interface for stakeholders without requiring frontend development.

## 🚀 Future Roadmap (Production Ready)
To scale this to a full organizational "Terminal" state:
* Migrate the SQLite database to a managed **PostgreSQL** instance (e.g., AWS RDS or Azure Database).
* Implement JWT-based authentication so scouts and coaches can securely log data.
* Integrate an automated CI/CD pipeline for unit testing and cloud deployment.

## 🛠️ How to Run Locally

**Use Docker**
```bash
docker-compose up --build
```

**If Docker doesn't work, try this**
```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## View the Interactive API Docs:
Navigate to http://127.0.0.1:8000/docs to test the API endpoints directly in your browser.
