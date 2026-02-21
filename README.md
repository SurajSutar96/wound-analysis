# WoundSense AI - Project Setup

## Backend (FastAPI)

1. Navigate to the `backend` folder:
   ```bash
   cd backend
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the server:
   ```bash
   uvicorn app.main:app --reload
   ```

## Frontend (Expo / React Native)

1. Navigate to the `frontend` folder:
   ```bash
   cd frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start the application:
   ```bash
   npm start
   ```

## Configuration

- Ensure your `GROQ_API_KEY` is set in `backend/.env`.
- Place your PyTorch model at `backend/app/models/wound_detector.pt`.
