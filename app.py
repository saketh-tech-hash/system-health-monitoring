from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import networkx as nx
import matplotlib.pyplot as plt
import io
import base64
import json
import datetime
import aiohttp
import asyncio
from pydantic import BaseModel
from typing import Dict, List, Any, Optional
import os
import uvicorn
from contextlib import asynccontextmanager

# Import modules
from models.graph import Graph
from services.health_checker import HealthChecker
from utils.graph_visualizer import GraphVisualizer
from utils.data_loader import load_graph_from_json

# Store the latest health check results
latest_health_results = None

# Create FastAPI app
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    os.makedirs("static", exist_ok=True)
    yield
    # Shutdown
    pass

app = FastAPI(lifespan=lifespan)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/check-health/")
async def check_health(request: Request):
    global latest_health_results
    try:
        # Get uploaded JSON file
        form = await request.form()
        if "file" not in form:
            raise HTTPException(status_code=400, detail="No file uploaded")
        
        file = form["file"]
        if not file.filename.endswith('.json'):
            raise HTTPException(status_code=400, detail="Only JSON files are supported")
        
        # Read JSON content
        content = await file.read()
        json_data = json.loads(content)
        
        # Load graph from JSON
        graph = load_graph_from_json(json_data)
        
        # Check health of components
        health_checker = HealthChecker()
        health_results = await health_checker.check_all(graph)
        
        # Visualize graph - now returns a dict with base64 and filename
        visualizer = GraphVisualizer()
        image_result = visualizer.visualize(graph, health_results)
        
        # Store results for later retrieval
        latest_health_results = {
            "graph_image": image_result["base64"],
            "filename": image_result["filename"],
            "health_results": health_results,
            "system_status": "Healthy" if all(result["status"] for result in health_results.values()) else "Unhealthy"
        }
        
        # Return results
        return latest_health_results
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/check-health-demo/")
async def check_health_demo():
    global latest_health_results
    try:
        # Load sample JSON
        with open("real_world_websites.json", "r") as f:
            json_data = json.load(f)
        
        # Load graph from JSON
        graph = load_graph_from_json(json_data)
        
        # Check health of components
        health_checker = HealthChecker()
        health_results = await health_checker.check_all(graph)
        
        # Visualize graph - now returns a dict with base64 and filename
        visualizer = GraphVisualizer()
        image_result = visualizer.visualize(graph, health_results)
        
        # Store results for later retrieval
        latest_health_results = {
            "graph_image": image_result["base64"],
            "filename": image_result["filename"],
            "health_results": health_results,
            "system_status": "Healthy" if all(result["status"] for result in health_results.values()) else "Unhealthy"
        }
        
        # Return results
        return latest_health_results
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Then modify the latest-health-results route
@app.get("/latest-health-results/")
async def get_latest_health_results():
    if latest_health_results is None:
        # If no health check has been run yet, return empty results
        return {
            "graph_image": "",
            "health_results": {},
            "system_status": "No data available"
        }
    
    # Save results to a text file
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    results_filename = f"health_results_{timestamp}.txt"
    results_filepath = os.path.join("static", results_filename)
    
    with open(results_filepath, "w") as f:
        # Write the system status
        f.write(f"System Status: {latest_health_results['system_status']}\n")
        f.write(f"Timestamp: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        # Write the graph image filename if available
        if "filename" in latest_health_results:
            f.write(f"Graph Image: {latest_health_results['filename']}\n\n")
        
        # Write component details
        f.write("Component Health Details:\n")
        f.write("-" * 80 + "\n")
        f.write(f"{'Component ID':<20} {'Status':<10} {'Response Time':<15} {'Message':<35}\n")
        f.write("-" * 80 + "\n")
        
        # Sort components by ID
        sorted_components = sorted(latest_health_results["health_results"].items())
        
        for component_id, details in sorted_components:
            status = "Healthy" if details["status"] else "Unhealthy"
            response_time = f"{details['response_time']:.3f}s"
            message = details.get("message", "N/A")
            f.write(f"{component_id:<20} {status:<10} {response_time:<15} {message:<35}\n")
    
    # Add the text file path to the results
    latest_health_results["results_file"] = results_filename
    
    return latest_health_results

@app.get("/health-view/", response_class=HTMLResponse)
async def health_view(request: Request):
    """View health status in HTML format"""
    return templates.TemplateResponse("health_view.html", {"request": request})

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)