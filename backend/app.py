from fastapi import FastAPI

# Create the FastAPI instance
app = FastAPI(title="Meetro Backend API")


@app.get("/api/status")
async def get_status():
    """
    Check the status of the backend service.
    """
    return {"status": "Backend is running!", "framework": "FastAPI"}
