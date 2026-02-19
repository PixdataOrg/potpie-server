from pydantic import BaseModel, Field, ConfigDict
from typing import Literal

AllowedTag = Literal[
    "entrypoint","routing","controller","service","domain","data-access","model","migration",
    "auth","config","integration","queue","test","util","type","error-handling","build"
]

class Snippet(BaseModel):
    model_config = ConfigDict(extra="forbid")
    node_id: str
    file_path: str
    code: str | None
    tags: list[AllowedTag]
    description: str | None
    line_start: int
    line_end: int

class Metadata(BaseModel):
    model_config = ConfigDict(extra="forbid")
    parsed_at: str
    total_nodes_found: int
    processed_nodes: int
    repo: str
    branch: str

class RepoAnalysisOutput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    snippets: list[Snippet]
    snippets_count: int
    analysis_response: dict
    metadata: Metadata
