
```mermaid
sequenceDiagram
    participant User
    participant AgentCoordinator
    participant LLM
    participant DocumentTools
    participant FunctionTools

    User->>AgentCoordinator: Submits Query
    AgentCoordinator->>LLM: Route Query to Tools
    LLM-->>AgentCoordinator: Returns Selected Tools
    alt Document Query
        AgentCoordinator->>DocumentTools: Execute Query
        DocumentTools-->>AgentCoordinator: Returns Document Insights
    end
    alt Function Query
        AgentCoordinator->>FunctionTools: Execute Query
        FunctionTools-->>AgentCoordinator: Returns Data (e.g., SQL results, Market Data)
    end
    AgentCoordinator->>LLM: Synthesize Results
    LLM-->>AgentCoordinator: Returns Comprehensive Answer
    AgentCoordinator-->>User: Displays Final Answer
```
