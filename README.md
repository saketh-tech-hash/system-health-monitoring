# System Health Monitoring API

A web-based application for monitoring the health of complex systems represented as Directed Acyclic Graphs (DAG).

## Overview

This application allows you to:

- Upload JSON files describing your system components and their relationships
- Monitor the health status of each component
- Visualize the system as a graph with color-coded health indicators
- Track and persist health check results over time

## Directory Structure

system-health-monitor/
|
+-- app.py                      # Main FastAPI application
+-- requirements.txt            # Project dependencies
+-- example.json                # Example system configuration
+-- mixed_services.json         # Example with mixed health statuses
+-- real_world_websites.json    # Real-world websites example
+-- cloud_infrastructure.json   # Cloud infrastructure example
|
+-- models/
|   +-- __init__.py
|   +-- graph.py                # Graph data structure
|
+-- services/
|   +-- __init__.py
|   +-- health_checker.py       # Health checking logic
|
+-- utils/
|   +-- __init__.py
|   +-- data_loader.py          # JSON data loading
|   +-- graph_visualizer.py     # Graph visualization
|
+-- templates/
|   +-- index.html              # Main UI template
|   +-- health_view.html        # Health dashboard
|
+-- static/                     # Generated artifacts (created at runtime)


## Installation and Setup

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Git (for cloning the repository)

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/system-health-monitor.git
cd system-health-monitor
```

### Step 2: Create a Virtual Environment

```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

The `requirements.txt` file includes the following packages:

- fastapi
- uvicorn
- networkx
- matplotlib
- aiohttp
- python-multipart
- jinja2
- pydantic

### Step 4: Run the Application

```bash
python app.py
```

The application will start running on `http://localhost:8000`.

## API Endpoints

| Endpoint                  | Method | Description                                  |
|--------------------------|--------|----------------------------------------------|
| `/`                      | GET    | Main UI for uploading JSON files             |
| `/check-health/`         | POST   | Check health with uploaded JSON              |
| `/check-health-demo/`    | POST   | Run a demo with example JSON                 |
| `/health-view/`          | GET    | Dashboard view of system health              |
| `/latest-health-results/`| GET    | Get most recent health check results         |

## Using the Application

### 1. Upload a System Configuration

- Access the main page at `http://localhost:8000/`
- Click "Choose File" and select your JSON configuration file
- Click "Check Health" to analyze the system

### 2. Run a Demo

- On the main page, click "Run Demo" to test with example configurations
- The system will perform health checks on predefined components

### 3. View the Health Dashboard

- Navigate to `http://localhost:8000/health-view/`
- See a visual representation of your system with color-coded health status
  - Green nodes represent healthy components
  - Red nodes show unhealthy ones
- The dashboard automatically updates with your latest health check

## JSON Configuration Format

The system uses JSON files to define the components and their relationships. Here's the expected format:

```json
{
  "nodes": [
    {
      "id": "component_id",
      "name": "Component Name",
      "description": "Description of the component",
      "check_type": "http",
      "url": "http://example.com",
      "step": 1
    }
  ],
  "edges": [
    {"source": "source_component_id", "target": "target_component_id"}
  ]
}
```

### Node Properties

- `id`: Unique identifier for the component
- `name`: Display name for the component
- `description`: Brief description (optional)
- `check_type`: Type of health check to perform (`http`, `mock`)
- `url`: URL to check for HTTP health checks
- `step`: Logical layer number for visualization (optional)

### Edges

Define the relationships between components, with each edge having:

- `source`: ID of the source component
- `target`: ID of the target component

## Example JSON Files

The repository includes several example configurations:

- `example.json`: Basic example with mock components
- `real_world_websites.json`: Real public websites for testing
- `mixed_services.json`: Microservice architecture with mixed health statuses
- `cloud_infrastructure.json`: Cloud infrastructure setup

## Testing

### Testing Routes with Example JSON

#### Check Health with Custom JSON

```bash
curl -X POST -F "file=@example.json" http://localhost:8000/check-health/
```

#### Run the Demo

```bash
curl -X POST http://localhost:8000/check-health-demo/
```

#### Get Latest Results

```bash
curl -X GET http://localhost:8000/latest-health-results/
```

### Browser Testing

- Open your browser to `http://localhost:8000/`
- Test the upload functionality with the provided JSON files
- Try the "Run Demo" button to see example results
- Navigate to the dashboard at `/health-view/` to see visualizations

## Customization

### Adding New Health Check Types

Extend the `check_health` method in `services/health_checker.py`:

```python
async def check_health(self, node_id: str, node_data: Dict[str, Any]) -> Dict[str, Any]:
    check_type = node_data.get("check_type", "http")

    if check_type == "your_custom_type":
        return {
            "node_id": node_id,
            "status": True,
            "response_time": 0,
            "message": "Custom check result"
        }
```

### Modifying Graph Visualization

Adjust parameters in `utils/graph_visualizer.py`:

```python
def __init__(self):
    self.node_size = 2000
    self.font_size = 10
    self.arrow_size = 20
    self.figure_size = (14, 10)
```

## Troubleshooting

### Common Issues

- **Connection errors when checking URLs**: Check your internet connection or use the "mock" check type
- **Graph visualization issues**: Ensure `matplotlib` is properly installed
- **JSON parsing errors**: Verify your JSON file format matches the expected structure

### Debug Mode

Run the application in debug mode for more detailed logs:

```bash
uvicorn app:app --reload --log-level debug
```

## Features

- **Asynchronous Health Checks**: Uses `aiohttp` to check component health in parallel
- **Hierarchical Visualization**: Organizes components based on their logical layers
- **Persistent Storage**: Saves graph images and health reports to the static folder
- **Real-time Updates**: Dashboard can be refreshed to get the latest status
- **Multiple Health Check Types**: Supports HTTP checks and mock checks
- **Customizable Visualization**: Graph appearance can be adjusted through configuration

## License

This project is licensed under the MIT License.

## Contributing

Contributions are welcome! Please feel free to submit a pull request.