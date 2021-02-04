"""Entry Point, speeds up uvicorn at port 8000"""
import uvicorn

if __name__ == "__main__":
    uvicorn.run("app.server.app:app", host="0.0.0.0", port=8000, reload=True)