# NutriTrack — Intelligent Malnutrition Analysis and Early Risk Identification System

An educational full-stack prototype using Python, FastAPI, HTML/CSS/JavaScript, SQLite, scikit-learn, Docker and GitHub Actions.

## Important scope and safety
This software is **not a medical device** and does not diagnose malnutrition or provide treatment advice. BMI is stored as a descriptive measurement only. For people under 20, BMI must be interpreted using appropriate age- and sex-specific growth references; this starter deliberately does not assign child/adolescent BMI categories. Adult records are also marked for professional review rather than classified from BMI alone. The ML component is an unsupervised dataset-anomaly demonstration, not a malnutrition prediction model. Use synthetic/demo data only; do not enter identifiable patient information.

## Run locally in VS Code
1. Install Python 3.11+.
2. Open this folder in VS Code.
3. Open Terminal in the project folder.
4. Create and activate a virtual environment:

   Windows PowerShell:
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```
   macOS/Linux:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
5. Install packages:
   ```bash
   pip install -r requirements.txt
   ```
6. Start the backend:
   ```bash
   uvicorn backend.main:app --reload
   ```
7. Open http://localhost:8000/frontend/ in your browser.
8. API documentation: http://localhost:8000/docs

## Run tests
```bash
pytest -q
```

## Run with Docker
Install and start Docker Desktop, then run:
```bash
docker compose up --build
```
Open http://localhost:8000/frontend/ . Stop with `Ctrl+C`, or run `docker compose down`. Persistent SQLite data is stored in a Docker volume.

## GitHub Actions
Push the repository to GitHub. The workflow in `.github/workflows/ci-cd.yml` runs tests and builds the Docker image on pushes and pull requests to `main`/`master`. This starter demonstrates CI and container-image build; it does **not** yet publish an image or deploy to a cloud host. A real deployment stage requires choosing a hosting provider and configuring secrets.

## API endpoints
- `GET /api/health`
- `POST /api/assessments`
- `GET /api/assessments`
- `GET /api/summary`
- `GET /api/ml/status`
- `DELETE /api/assessments/{id}`

## Next project extensions
- Integrate official, versioned growth-reference data and validated z-score calculations for children/adolescents.
- Add a documented, ethically sourced dataset and data dictionary.
- Add authentication, access controls, audit logs and privacy protections before any real-world deployment.
- Validate any model with a suitable labelled dataset, documented metrics, bias checks and expert review.
- Configure a cloud deployment and protected GitHub Actions secrets.
