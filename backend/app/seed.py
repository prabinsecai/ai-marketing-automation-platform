from sqlalchemy.orm import Session
from .models import Workspace, Product, Audience, Campaign

def seed_demo(db: Session) -> Workspace:
    workspace = db.query(Workspace).filter_by(name="Demo Workspace").first()
    if workspace:
        return workspace
    workspace = Workspace(name="Demo Workspace", description="Sample marketing workspace")
    db.add(workspace); db.flush()
    db.add_all([
        Product(workspace_id=workspace.id, name="Growth Platform", description="AI-powered marketing automation"),
        Audience(workspace_id=workspace.id, name="Growth Marketers", description="Teams seeking scalable campaigns", criteria={"role": "marketer"}),
        Campaign(workspace_id=workspace.id, name="Launch Campaign", objective="Drive product awareness")
    ])
    db.commit(); db.refresh(workspace)
    return workspace
