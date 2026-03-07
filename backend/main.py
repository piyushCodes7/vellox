from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import pandas as pd
import io
import os
from fastapi.staticfiles import StaticFiles

# Import the DataAnalyzer we created earlier
from analyzer import DataAnalyzer

app = FastAPI(
    title="Vellox Data Insight API",
    description="API for analyzing CSV datasets and generating structured insights.",
    version="1.0.0"
)

# Configure CORS so the frontend can communicate with this backend
# In a real production app, you'd restrict this to your specific frontend URL
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allows all origins (good for student projects/local dev)
    allow_credentials=True,
    allow_methods=["*"], # Allows all methods (GET, POST, etc.)
    allow_headers=["*"], # Allows all headers
)

@app.get("/api/status")
async def root():
    return {"message": "Welcome to the Vellox API. Use /api/analyze to process CSVs."}

@app.post("/api/analyze")
async def analyze_csv(file: UploadFile = File(...)):
    """
    Endpoint that accepts a CSV file, passes it to the DataAnalyzer,
    and returns a full analytical report as JSON.
    """
    
    # 1. Validate that the uploaded file is a CSV
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload a CSV file.")
    
    try:
        # 2. Read the file contents into memory
        contents = await file.read()
        
        # 3. Use pandas to parse the CSV content
        # We use io.BytesIO because pandas read_csv expects a file-like object
        df = pd.read_csv(io.BytesIO(contents))
        
        # 4. Check if the dataframe is completely empty
        if df.empty:
            raise HTTPException(status_code=400, detail="The uploaded CSV file is empty.")
            
        # 5. Initialize our analyzer with the loaded dataframe
        analyzer = DataAnalyzer(df)
        
        # 6. Generate the full report
        report = analyzer.generate_full_report()
        
        # 7. Return the report as a JSON response
        return JSONResponse(content=report)
        
    except pd.errors.EmptyDataError:
        raise HTTPException(status_code=400, detail="The CSV file contains no data or could not be parsed.")
    except Exception as e:
        # Catch any other unexpected errors during processing
        raise HTTPException(status_code=500, detail=f"An error occurred while analyzing the data: {str(e)}")

# Serve the frontend static files
frontend_dir = os.path.join(os.path.dirname(__file__), "..", "frontend", "dist")

# Ensure the directory exists before mounting to avoid errors, 
# although in production it should always exist
if os.path.exists(frontend_dir):
    app.mount("/", StaticFiles(directory=frontend_dir, html=True), name="frontend")
else:
    @app.get("/")
    async def frontend_missing():
        return {"message": "Frontend build not found. Please run 'npm run build' in the frontend directory."}

# To run this server manually during development:
# uvicorn main:app --reload --host 0.0.0.0 --port 8000
