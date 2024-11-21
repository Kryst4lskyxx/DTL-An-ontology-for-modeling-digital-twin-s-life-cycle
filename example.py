import requests
import json
from datetime import datetime
from pprint import pprint

# API base URL
BASE_URL = "http://localhost:8000"

def print_response(response):
    print("\nResponse:")
    pprint(response.json())
    print("\nStatus Code:", response.status_code)
    print("-" * 80)

# Scenario 1: Complete Digital Twin Project Lifecycle for a Smart Factory
def smart_factory_dt_lifecycle():
    print("\n=== Scenario 1: Smart Factory Digital Twin Lifecycle ===\n")
    
    # 1. Design Phase - Create Project
    print("1. Creating Smart Factory Project...")
    project_data = {
        "projectName": "Smart Factory DT",
        "projectMotivation": "Optimize manufacturing processes and predict maintenance needs",
        "designers": ["John Doe", "Jane Smith"]
    }
    response = requests.post(f"{BASE_URL}/projects", json=project_data)
    print_response(response)

    # 2. Development Phase - Setup Repository
    print("\n2. Creating Development Repository...")
    repo_data = {
        "repositoryName": "smart-factory-dt",
        "projectRepository": "https://github.com/company/smart-factory-dt",
        "languageUsed": "Python, JavaScript",
        "packagesUsed": ["TensorFlow", "PyTorch", "FastAPI", "React"],
        "developers": ["Alice Johnson", "Bob Wilson"],
        "datasetLink": "https://factory-data.company.com/sensors"
    }
    response = requests.post(f"{BASE_URL}/repositories", json=repo_data)
    print_response(response)

    # 3. Deployment Phase - Deploy Docker Container
    print("\n3. Deploying Docker Container...")
    deployment_data = {
        "containerName": "smart-factory-predictor",
        "imageName": "factory-dt/predictor",
        "imageVersion": "1.0.0",
        "cloudProvider": "AWS"
    }
    response = requests.post(f"{BASE_URL}/deployment/docker", json=deployment_data)
    print_response(response)

    # 4. Provenance - Create Scenario
    print("\n4. Creating Monitoring Scenario...")
    scenario_data = {
        "scenarioName": "Production Line Monitoring",
        "description": "Real-time monitoring of assembly line performance",
        "parameters": {
            "sampling_rate": "1min",
            "alert_threshold": "0.85",
            "prediction_window": "4h"
        },
        "users": ["operator1", "supervisor1", "analyst1"]
    }
    response = requests.post(f"{BASE_URL}/scenarios", json=scenario_data)
    print_response(response)

# Scenario 2: Building Energy Management Digital Twin
def building_energy_dt_lifecycle():
    print("\n=== Scenario 2: Building Energy Management Digital Twin ===\n")
    
    # 1. Design Phase
    print("1. Creating Building Energy Project...")
    project_data = {
        "projectName": "Smart Building Energy DT",
        "projectMotivation": "Optimize energy consumption and maintain comfort levels",
        "designers": ["Emma Brown", "David Clark"]
    }
    response = requests.post(f"{BASE_URL}/projects", json=project_data)
    print_response(response)

    # 2. Development Phase
    print("\n2. Creating Development Repository...")
    repo_data = {
        "repositoryName": "building-energy-dt",
        "projectRepository": "https://github.com/company/building-energy-dt",
        "languageUsed": "Python, R",
        "packagesUsed": ["scikit-learn", "pandas", "numpy", "plotly"],
        "developers": ["Charlie Davies", "Eva Martinez"],
        "datasetLink": "https://building-data.company.com/energy"
    }
    response = requests.post(f"{BASE_URL}/repositories", json=repo_data)
    print_response(response)

    # 3. Deployment
    print("\n3. Deploying Energy Management System...")
    deployment_data = {
        "containerName": "building-energy-optimizer",
        "imageName": "building-dt/optimizer",
        "imageVersion": "2.1.0",
        "cloudProvider": "Azure"
    }
    response = requests.post(f"{BASE_URL}/deployment/docker", json=deployment_data)
    print_response(response)

    # 4. Provenance
    print("\n4. Creating Energy Optimization Scenario...")
    scenario_data = {
        "scenarioName": "HVAC Optimization",
        "description": "Optimize HVAC settings based on occupancy and weather",
        "parameters": {
            "temp_range": "20-24C",
            "humidity_range": "40-60%",
            "optimization_interval": "15min"
        },
        "users": ["facility_manager", "energy_analyst", "building_admin"]
    }
    response = requests.post(f"{BASE_URL}/scenarios", json=scenario_data)
    print_response(response)

# Scenario 3: Retrieve and Analyze Lifecycle Data
def analyze_lifecycle_data():
    print("\n=== Scenario 3: Analyzing Digital Twin Lifecycle Data ===\n")
    
    # 1. Get all projects
    print("1. Retrieving all projects...")
    response = requests.get(f"{BASE_URL}/projects")
    print_response(response)

    # 2. Get specific project lifecycle
    print("\n2. Retrieving lifecycle data for Smart Factory project...")
    response = requests.get(f"{BASE_URL}/lifecycle/Project_SmartFactory")
    print_response(response)

    # 3. Get provenance activities
    print("\n3. Retrieving provenance activities for Production Line Monitoring...")
    response = requests.get(
        f"{BASE_URL}/provenance/activities",
        params={"scenario_name": "Production Line Monitoring"}
    )
    print_response(response)

if __name__ == "__main__":
    print("=== Digital Twin Lifecycle API Usage Examples ===")
    print("Note: Make sure the API server is running on localhost:8000\n")
    
    try:
        # Run scenarios
        smart_factory_dt_lifecycle()
        building_energy_dt_lifecycle()
        analyze_lifecycle_data()
        
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the API server. Please ensure it's running on localhost:8000")
    except Exception as e:
        print(f"Error occurred: {str(e)}")