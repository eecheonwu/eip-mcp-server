import logging
from fastapi import FastAPI, BackgroundTasks
import uvicorn
from pydantic import BaseModel

# Import our MCP server functions directly
from eip_mcp_server.server import (
    generate_implementation_plan,
    generate_task_plan,
    generate_test_plan,
    generate_security_plan,
    KNOWLEDGE_DIR
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("trigger_listener")

app = FastAPI()

from typing import List, Dict

class TriggerPayload(BaseModel):
    project_id: str
    plan_type: str
    artifacts: List[Dict] = []
    graph_context: str = ""

def process_plan(payload: TriggerPayload):
    logger.info(f"Received trigger to generate {payload.plan_type} in {KNOWLEDGE_DIR}")
    
    # Scaffold SSOT directories
    dirs = ["requirements", "architecture", "system", "testing", "agents"]
    for d in dirs:
        dir_path = KNOWLEDGE_DIR / d
        dir_path.mkdir(parents=True, exist_ok=True)
        (dir_path / ".gitkeep").touch(exist_ok=True)
        
    ssot_yaml_path = KNOWLEDGE_DIR / "ssot.yaml"
    if not ssot_yaml_path.exists():
        ssot_yaml_content = f"""project_id: {payload.project_id}
version: 1.0.0
last_synced: ""
description: "Local Engineering SSOT synchronized from EIP Web App"
directories:
  requirements: "SRDs and business requirements"
  architecture: "ADRs, C4, and UML diagrams"
  system: "Knowledge Graph and technical specifications"
  testing: "Test specifications and coverage"
  agents: "AI Agent context packages"
"""
        ssot_yaml_path.write_text(ssot_yaml_content, encoding='utf-8')
    
    # Map artifacts to appropriate directories
    for artifact in payload.artifacts:
        name = artifact.get("name", "artifact")
        if not name.endswith(".md"):
            name += ".md"
            
        atype = artifact.get("type", "")
        if atype == "SRD":
            target_path = KNOWLEDGE_DIR / "requirements" / name
        elif atype == "ADR" or atype == "UML" or atype == "C4":
            target_path = KNOWLEDGE_DIR / "architecture" / name
        elif atype == "Test Spec":
            target_path = KNOWLEDGE_DIR / "testing" / name
        else:
            target_path = KNOWLEDGE_DIR / "system" / name
            
        content = artifact.get("content")
        if content is None:
            content = ""
            
        target_path.write_text(content, encoding='utf-8')
        
    if payload.graph_context:
        (KNOWLEDGE_DIR / "system" / "WEB_GRAPH_CONTEXT.md").write_text(payload.graph_context, encoding='utf-8')
    
    if payload.plan_type == "Implementation Plan":
        generate_implementation_plan()
    elif payload.plan_type == "Task Plan":
        generate_task_plan()
    elif payload.plan_type == "Test Plan":
        generate_test_plan()
    elif payload.plan_type == "Security Plan":
        generate_security_plan()
    else:
        logger.warning(f"Unknown plan type: {payload.plan_type}")
        # Default to implementation plan
        generate_implementation_plan()

@app.post("/trigger")
async def trigger_webhook(payload: TriggerPayload, background_tasks: BackgroundTasks):
    """Webhook listener that kicks off the background MCP generation."""
    logger.info(f"Webhook hit for project {payload.project_id}")
    background_tasks.add_task(process_plan, payload)
    return {"status": "accepted", "message": f"Delegated generation for {payload.plan_type}"}

if __name__ == "__main__":
    logger.info("Starting local EIP MCP Webhook Listener on port 8123...")
    uvicorn.run(app, host="0.0.0.0", port=8123)
