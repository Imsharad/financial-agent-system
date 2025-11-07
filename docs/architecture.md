Architecture Overview:

User Query enters through the AgentCoordinator
AgentCoordinator intelligently routes to appropriate tool managers
DocumentToolsManager handles SEC filing analysis
FunctionToolsManager provides database, market, and PII capabilities
Result Synthesis combines multi-source information into coherent answers
Interaction Flow Details:

Query Analysis: LLM analyzes query to determine which tools are needed
Tool Execution: Selected tools execute in appropriate order
PII Detection: Database results automatically checked for sensitive fields
Result Synthesis: Multiple tool results combined using LLM when needed
Response Delivery: Final answer returned to user
Component Responsibilities:

DocumentToolsManager:

Configures LlamaIndex with OpenAI models
Loads and processes PDF documents
Creates vector indices for semantic search
Wraps indices in QueryEngineTool objects
FunctionToolsManager:

Implements SQL generation from natural language
Fetches real-time market data from APIs
Detects and masks PII fields automatically
Wraps functions in FunctionTool objects
AgentCoordinator:

Orchestrates all tools through intelligent routing
Uses LLM to select appropriate tools for queries
Coordinates PII protection with database queries
Synthesizes multi-tool results into coherent answers