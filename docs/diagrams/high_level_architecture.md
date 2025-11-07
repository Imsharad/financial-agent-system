
```mermaid
graph TD
    subgraph User Interface
        A[User Query]
    end

    subgraph Financial Agent System
        B[Agent Coordinator]
        C[Document Tools]
        D[Function Tools]
    end

    subgraph Data Sources
        E[SEC 10-K Filings]
        F[Financial Database]
        G[Yahoo Finance API]
    end

    A --> B
    B --> C
    B --> D
    C --> E
    D --> F
    D --> G
```
