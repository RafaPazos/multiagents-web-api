# FastAPI Project README  

## Project Overview  

This project is built using FastAPI, a modern web framework for Python. It provides a robust API for managing multi-agent systems.  

## Prerequisites  

- Python 3.8 or higher  
- Docker (optional, for containerized deployment)  

## Setting Up the Python Environment  

### Step 1: Create a Virtual Environment  

To isolate dependencies, create a virtual environment using `venv`:  
```bash  
python -m venv .agents-venv  
```  

### Step 2: Activate the Virtual Environment  

- **Windows**:  
    ```bash  
    .agents-venv\Scripts\activate  
    ```  
- **macOS/Linux**:  
    ```bash  
    source .agents-venv/bin/activate  
    ```  

### Step 3: Install Dependencies  

Once the virtual environment is activated, install the required dependencies:  
```bash  
pip install -r requirements.txt  
```  

## Running the Application  

After setting up the environment, start the FastAPI application:  
```bash  
uvicorn main:app 
```  
Replace `main:app` with the appropriate module and application name if different.  

## Using Docker  

### Step 1: Build the Docker Image  

A `Dockerfile` is provided to containerize the application. Build the image using:  
```bash  
docker build -t fastapi-app .  
```  

### Step 2: Run the Docker Container  

Run the container with the following command:  
```bash  
docker run -p 8000:8000 fastapi-app  
```  

The application will be accessible at `http://localhost:8000`.  

## Project Structure  
- `main.py`: Entry point for the FastAPI application.  
- `requirements.txt`: Contains the list of dependencies.  
- `Dockerfile`: Configuration for building the Docker image.
- `app/`: Directory containing the application code.
    - `api/`: API route definitions.
    - `models/`: Pydantic models for request/response payloads.
    - `services/`: Business logic for handling requests.
    - `utils/`: Utility functions and helper modules.
    - `__init__.py`: Package initialization file.  

## Additional Notes  
- Ensure `requirements.txt` is up-to-date with all dependencies.  
- Use `venv` for local development and Docker for production deployment.  
