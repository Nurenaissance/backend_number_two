from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from router.sentiment_router import router as senti_router

# Initialize the FastAPI app
app = FastAPI()

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins; adjust this if you need more specific origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, OPTIONS, etc.)
    allow_headers=["*"],  # Allows all headers
)

# Include routers
app.include_router(senti_router)

# Main entry point to run the application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=1234)
