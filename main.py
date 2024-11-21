from fastapi import FastAPI, HTTPException, Query, Path
from SPARQLWrapper import SPARQLWrapper, JSON, POST
from typing import List, Dict, Optional
from pydantic import BaseModel, HttpUrl
import uvicorn
from enum import Enum
from datetime import datetime

app = FastAPI(
    title="Digital Twin Lifecycle API",
    description="REST API for Digital Twin Lifecycle Ontology",
    version="1.0.0"
)

# Configuration
GRAPHDB_URL = "http://localhost:7200"
REPOSITORY_ID = "dt-lifecycle"
BASE_URI = "http://www.example.org/dtlifecycle#"

# Initialize SPARQLWrapper
sparql = SPARQLWrapper(f"{GRAPHDB_URL}/repositories/{REPOSITORY_ID}")
sparql.setReturnFormat(JSON)

sparql_post = SPARQLWrapper(f"{GRAPHDB_URL}/repositories/{REPOSITORY_ID}/statements")
sparql_post.setReturnFormat(JSON)

# Pydantic models based on your ontology
class LifecyclePhase(str, Enum):
    DESIGN = "DTDesign"
    DEVELOPMENT = "DTDevelopment"
    DEPLOYMENT = "DTDeployment"
    PROVENANCE = "DTProvenance"

class Project(BaseModel):
    projectName: str
    projectMotivation: str
    designers: List[str] = []

class Repository(BaseModel):
    repositoryName: str
    projectRepository: HttpUrl
    languageUsed: str
    packagesUsed: List[str]
    developers: List[str] = []
    datasetLink: Optional[HttpUrl]

class DockerDeployment(BaseModel):
    containerName: str
    imageName: str
    imageVersion: str
    cloudProvider: str

class ScenarioConfig(BaseModel):
    scenarioName: str
    description: str
    parameters: Dict[str, str]
    users: List[str]

# Helper Functions
def execute_sparql_query(query: str) -> Dict:
    """Execute a SPARQL query and return results"""
    print(query)
    sparql.setQuery(query)
    try:
        results = sparql.queryAndConvert()
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
def execute_sparql_query_post(query: str) -> Dict:
    """Execute a SPARQL query and return results"""
    print(query)
    sparql_post.setQuery(query)
    sparql_post.setMethod(POST)
    try:
        results = sparql_post.queryAndConvert()
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# API Routes
@app.get("/", tags=["Health Check"])
async def root():
    """Health check endpoint"""
    return {"status": "healthy", "service": "GraphDB API"}
@app.get("/projects", tags=["Design Phase"])
async def get_all_projects():
    """Get all Digital Twin projects"""
    query = f"""
    SELECT ?project ?name ?motivation
    WHERE {{
        ?project a <{BASE_URI}Project> ;
                <{BASE_URI}projectName> ?name ;
                <{BASE_URI}projectMotivation> ?motivation .
    }}
    """
    results = execute_sparql_query(query)
    return results["results"]["bindings"]

@app.post("/projects", tags=["Design Phase"])
async def create_project(project: Project):
    """Create a new Digital Twin project"""
    project_uri = f"{BASE_URI}Project_{project.projectName.replace(' ', '_')}"
    query = f"""
    INSERT DATA {{
        <{project_uri}> a <{BASE_URI}Project> ;
            <{BASE_URI}projectName> "{project.projectName}" ;
            <{BASE_URI}projectMotivation> "{project.projectMotivation}" .
    """
    for designer in project.designers:
        query += f"""
        <{project_uri}> <{BASE_URI}hasDesigner> "{designer}" .
        """
    query += "}"
    
    execute_sparql_query_post(query)
    return {"status": "success", "project_uri": project_uri}

@app.post("/repositories", tags=["Development Phase"])
async def create_repository(repository: Repository):
    """Create a new repository record"""
    repo_uri = f"{BASE_URI}Repository_{repository.repositoryName}"
    query = f"""
    INSERT DATA {{
        <{repo_uri}> a <{BASE_URI}Repository> ;
            <{BASE_URI}repositoryName> "{repository.repositoryName}" ;
            <{BASE_URI}projectRepository> "{repository.projectRepository}" ;
            <{BASE_URI}languageUsed> "{repository.languageUsed}" .
    """
    for package in repository.packagesUsed:
        query += f"""
        <{repo_uri}> <{BASE_URI}packagesUsed> "{package}" .
        """
    for developer in repository.developers:
        query += f"""
        <{repo_uri}> <{BASE_URI}hasDeveloper> "{developer}" .
        """
    if repository.datasetLink:
        query += f"""
        <{repo_uri}> <{BASE_URI}datasetLink> "{repository.datasetLink}" .
        """
    query += "}"
    execute_sparql_query_post(query)
    return {"status": "success", "repository_uri": repo_uri}

@app.post("/deployment/docker", tags=["Deployment Phase"])
async def create_docker_deployment(deployment: DockerDeployment):
    """Register a Docker container deployment"""
    container_uri = f"{BASE_URI}Container_{deployment.containerName.replace(' ', '_')}"
    query = f"""
    INSERT DATA {{
        <{container_uri}> a <{BASE_URI}DockerContainer> ;
            <{BASE_URI}dockerContainerName> "{deployment.containerName}" ;
            <{BASE_URI}imageName> "{deployment.imageName}" ;
            <{BASE_URI}imageVersion> "{deployment.imageVersion}" ;
            <{BASE_URI}hasCloudProvider> "{deployment.cloudProvider}" .
    }}
    """
    execute_sparql_query_post(query)
    return {"status": "success", "container_uri": container_uri}

@app.post("/scenarios", tags=["Provenance"])
async def create_scenario(scenario: ScenarioConfig):
    """Create a new scenario configuration"""
    scenario_uri = f"{BASE_URI}Scenario_{scenario.scenarioName.replace(' ', '_')}"
    query = f"""
    PREFIX dtlifecycle: <http://www.example.org/dtlifecycle#>
    
    INSERT DATA {{
        <{scenario_uri}> a <{BASE_URI}Scenario> ;
            <{BASE_URI}scenarioName> "{scenario.scenarioName}" .
        
        <{scenario_uri}_desc> a <{BASE_URI}ScenarioDescription> ;
            rdfs:label "{scenario.description}" .
        
        <{scenario_uri}> <{BASE_URI}hasScenarioDescription> <{scenario_uri}_desc> .
    """
    for param_name, param_value in scenario.parameters.items():
        query += f"""
        <{scenario_uri}_param_{param_name}> a <{BASE_URI}ScenarioParameter> ;
            rdfs:label "{param_name}" ;
            rdf:value "{param_value}" .
        <{scenario_uri}> <{BASE_URI}hasScenarioParameter> <{scenario_uri}_param_{param_name}> .
        """
    for user in scenario.users:
        user_uri = f"{BASE_URI}User_{user}"
        query += f"""
        <{user_uri}> <{BASE_URI}hasAccessTo> <{scenario_uri}> .
        """
    query += "}"
    
    execute_sparql_query_post(query)
    return {"status": "success", "scenario_uri": scenario_uri}

@app.get("/lifecycle/{project_id}", tags=["Lifecycle"])
async def get_project_lifecycle(
    project_id: str = Path(..., description="The project identifier")
):
    """Get all lifecycle information for a specific project"""
    query = f"""
    SELECT ?phase ?type ?data
    WHERE {{
        <{BASE_URI}{project_id}> ?phase ?data .
        ?phase rdfs:subClassOf <{BASE_URI}DigitalTwinLifecycle> .
        BIND(STRAFTER(STR(?phase), "{BASE_URI}") AS ?type)
    }}
    """
    results = execute_sparql_query(query)
    return results["results"]["bindings"]

@app.get("/provenance/activities", tags=["Provenance"])
async def get_activities(
    scenario_name: Optional[str] = Query(None, description="Filter by scenario name")
):
    """Get provenance activities, optionally filtered by scenario"""
    query = f"""
    SELECT ?activity ?type ?timestamp ?scenario
    WHERE {{
        ?activity a <{BASE_URI}Activity> ;
                 rdf:type ?type ;
                 <{BASE_URI}timestamp> ?timestamp .
        OPTIONAL {{ ?activity <{BASE_URI}relatedToScenario> ?scenario }}
    """
    if scenario_name:
        query += f"""
        FILTER(CONTAINS(STR(?scenario), "{scenario_name}"))
        """
    query += "}"
    
    results = execute_sparql_query(query)
    return results["results"]["bindings"]

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)