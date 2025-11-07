# Financial Agent System: Multi-Tool Coordination for Financial Analysis

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![LlamaIndex](https://img.shields.io/badge/LlamaIndex-0.10+-green.svg)](https://www.llamaindex.ai/)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--3.5--Turbo-orange.svg)](https://openai.com/)

A sophisticated **agentic AI system** that intelligently coordinates between document analysis, database queries, and real-time market data to provide comprehensive financial insights. This project demonstrates enterprise-grade agentic AI architecture suitable for production financial services applications.

## Project Overview

### What Is This Project?

This is a **multi-tool agentic financial analyst system** that combines the power of:
- **Document RAG (Retrieval-Augmented Generation)**: Analyzes SEC 10-K filings using vector search
- **Database Intelligence**: Converts natural language to SQL queries for customer portfolio analysis
- **Real-Time Market Data**: Fetches live stock prices and market information
- **Privacy Protection**: Automatically detects and masks personally identifiable information (PII)

The system intelligently routes user queries to the appropriate tools, coordinates multiple data sources, and synthesizes comprehensive answers—all while maintaining privacy and security standards required for financial services.

### The Challenge

Financial analysts need to answer complex questions that require information from multiple sources simultaneously. For example:

> *"How does Tesla's business strategy from their 10-K filing align with our customers' investment positions and current market performance?"*

This single query requires:
1. **Document analysis** of Tesla's SEC 10-K filing
2. **Database queries** to find customers holding Tesla stock
3. **Real-time market data** for current TSLA price and performance
4. **Intelligent synthesis** of all information into a coherent answer
5. **Automatic PII protection** for customer data

Traditional systems require manual coordination across multiple tools and databases. This project demonstrates how **agentic AI** can automate this entire workflow.

## Architecture & Design

### System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    User Query Interface                      │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│              AgentCoordinator (Orchestration Layer)         │
│  • LLM-based intelligent routing                             │
│  • Multi-tool coordination                                   │
│  • Result synthesis                                          │
│  • Automatic PII detection & protection                     │
└───────────────┬───────────────────────────┬─────────────────┘
                │                           │
        ┌───────┴────────┐         ┌────────┴────────┐
        │                │         │                 │
        ▼                ▼         ▼                 ▼
┌───────────────┐  ┌──────────────┐  ┌──────────────────────┐
│ Document Tools│  │ Function Tools│  │   PII Protection     │
│ Manager       │  │ Manager       │  │   System             │
├───────────────┤  ├──────────────┤  └──────────────────────┘
│ • AAPL 10-K  │  │ • SQL Gen    │
│ • GOOGL 10-K │  │ • Market Data│
│ • TSLA 10-K  │  │ • PII Mask   │
└───────────────┘  └──────────────┘
```

### Core Components

#### 1. **DocumentToolsManager** (`helper_modules/document_tools.py`)
- **Purpose**: Creates individual RAG systems for each company's SEC 10-K filing
- **Technology**: LlamaIndex vector indexing with OpenAI embeddings
- **Capabilities**:
  - PDF document processing and chunking
  - Vector embedding generation (`text-embedding-ada-002`)
  - Semantic search query engines
  - Company-specific tool creation (AAPL, GOOGL, TSLA)

**Key Implementation Details**:
- Uses `SentenceSplitter` with 1024-character chunks and 20-character overlap
- Adds metadata (company, sector, document type) to each node
- Creates `QueryEngineTool` objects with descriptive names and descriptions
- Supports Vocareum API compatibility via `api_base` parameter

#### 2. **FunctionToolsManager** (`helper_modules/function_tools.py`)
- **Purpose**: Provides database querying, market data, and PII protection capabilities
- **Technology**: SQLite, Yahoo Finance API, pattern-based PII detection
- **Capabilities**:
  - **Natural Language to SQL**: LLM-powered SQL generation from user queries
  - **Real-Time Market Data**: Yahoo Finance API integration for live stock prices
  - **PII Protection**: Automatic detection and masking of sensitive information

**Key Implementation Details**:
- **SQL Generation**: Uses GPT-3.5-turbo to convert natural language to SQL queries
  - Includes comprehensive database schema with relationships
  - Error handling with retry logic and context-aware regeneration
  - Supports complex JOINs across customers, portfolios, companies, and market data
- **Market Data**: Fetches real-time prices, volumes, market cap from Yahoo Finance
  - Handles multiple companies in a single query
  - Graceful fallback on API failures
- **PII Protection**: Pattern-based detection with intelligent masking
  - Email: `abc@gmail.com` → `***@gmail.com`
  - Phone: `123-456-7890` → `***-***-7890`
  - Names: `John Doe` → `****`
  - Addresses: Partial masking preserving format

#### 3. **AgentCoordinator** (`helper_modules/agent_coordinator.py`)
- **Purpose**: Orchestrates all tools with intelligent routing and result synthesis
- **Technology**: LLM-based decision making, multi-tool coordination
- **Capabilities**:
  - **Intelligent Routing**: Analyzes queries to select appropriate tools
  - **Multi-Tool Coordination**: Executes multiple tools and combines results
  - **Result Synthesis**: Uses LLM to create coherent answers from multiple sources
  - **Automatic PII Protection**: Detects database results and applies masking

**Key Implementation Details**:
- **Query Routing**: Uses LLM prompt engineering to analyze queries and select tools
  - Provides tool descriptions and routing guidelines
  - Falls back to keyword matching if LLM routing fails
  - Supports single and multi-tool queries
- **Result Synthesis**: Combines multiple tool outputs into comprehensive answers
  - Uses LLM to integrate information from documents, databases, and market data
  - Maintains context and coherence across sources
- **PII Workflow**: Automatic detection and protection
  - Scans database query results for PII column names
  - Applies appropriate masking based on field type
  - Adds notices about masked fields

## Technology Stack

### Core Technologies

| Technology | Version | Purpose |
|------------|---------|---------|
| **Python** | 3.9+ | Core programming language |
| **LlamaIndex** | 0.10+ | RAG framework for document processing |
| **OpenAI GPT-3.5-turbo** | Latest | LLM for routing, SQL generation, synthesis |
| **OpenAI Embeddings** | text-embedding-ada-002 | Vector embeddings for semantic search |
| **SQLite** | Built-in | Customer portfolio database |
| **Yahoo Finance API** | REST | Real-time market data |
| **python-dotenv** | Latest | Environment variable management |

### Key Libraries

- **llama-index-core**: Core LlamaIndex functionality for document processing
- **llama-index-llms-openai**: OpenAI LLM integration
- **llama-index-embeddings-openai**: OpenAI embedding integration
- **requests**: HTTP client for Yahoo Finance API
- **pandas/numpy**: Data manipulation (for future enhancements)

### Architecture Patterns

1. **Modular Design**: Clean separation of concerns with independently testable components
2. **Tool-Based Architecture**: Each capability wrapped as a LlamaIndex tool
3. **LLM-Based Routing**: Intelligent tool selection using language model reasoning
4. **Lazy Initialization**: Tools created on-demand to optimize resource usage
5. **Error Handling**: Comprehensive error handling with graceful fallbacks

## How We Built It

### Implementation Approach

The system was built using a **modular, incremental approach**:

#### Phase 1: Document Processing Foundation
1. **PDF Loading**: Used LlamaIndex's `SimpleDirectoryReader` to load SEC 10-K filings
2. **Chunking Strategy**: Implemented `SentenceSplitter` with optimal chunk size (1024 chars) and overlap (20 chars)
3. **Vector Indexing**: Created `VectorStoreIndex` for semantic search capabilities
4. **Tool Creation**: Wrapped query engines in `QueryEngineTool` objects with descriptive metadata

**Key Decisions**:
- Chunk size of 1024 balances context preservation with search precision
- 20-character overlap ensures continuity across chunk boundaries
- Metadata enrichment enables company-specific filtering

#### Phase 2: Function Tool Development
1. **SQL Generation**: Implemented LLM-powered natural language to SQL conversion
   - Created comprehensive schema descriptions with relationships
   - Added error handling with retry logic
   - Implemented query validation and sanitization
2. **Market Data Integration**: Built Yahoo Finance API client
   - Implemented symbol detection from natural language
   - Added error handling and fallback mechanisms
   - Formatted results for readability
3. **PII Protection**: Developed pattern-based detection and masking system
   - Created field name pattern matching
   - Implemented type-specific masking strategies
   - Added automatic detection workflow

**Key Decisions**:
- SQL generation uses schema context to improve accuracy
- Market data tool supports multiple companies in single query
- PII protection applies automatically without manual intervention

#### Phase 3: Agent Coordination
1. **Tool Routing**: Implemented LLM-based intelligent routing
   - Created comprehensive tool descriptions
   - Developed routing guidelines and examples
   - Added fallback keyword matching
2. **Result Synthesis**: Built multi-source answer generation
   - Used LLM to integrate information from multiple tools
   - Maintained query context throughout synthesis
   - Formatted responses for clarity
3. **PII Workflow**: Integrated automatic protection into query pipeline
   - Detected PII fields in database results
   - Applied masking before result synthesis
   - Added transparency notices

**Key Decisions**:
- LLM routing provides flexibility for complex queries
- Synthesis ensures coherent answers from multiple sources
- PII protection is automatic and transparent

### Design Patterns Used

1. **Manager Pattern**: Each component has a manager class (DocumentToolsManager, FunctionToolsManager)
2. **Factory Pattern**: Tools are created through factory methods (`build_document_tools`, `create_function_tools`)
3. **Strategy Pattern**: Different masking strategies for different PII types
4. **Template Method**: Common patterns in tool creation with customizable steps
5. **Observer Pattern**: Verbose mode for debugging and monitoring

## Trade-offs & Design Decisions

### 1. **Chunk Size vs. Context Preservation**

**Decision**: 1024-character chunks with 20-character overlap

**Trade-offs**:
- **Pros**: Good balance between search precision and context preservation
- **Pros**: Efficient embedding generation and storage
- **Cons**: Very long answers may span multiple chunks (mitigated by overlap)
- **Cons**: May miss context that spans chunk boundaries

**Alternative Considered**: Larger chunks (2048) would preserve more context but reduce search precision.

### 2. **LLM Routing vs. Rule-Based Routing**

**Decision**: LLM-based routing with keyword fallback

**Trade-offs**:
- **Pros**: Handles complex, ambiguous queries intelligently
- **Pros**: Adapts to new query patterns without code changes
- **Pros**: Can understand intent beyond keywords
- **Cons**: Higher latency (API call required)
- **Cons**: Less predictable than rule-based systems
- **Cons**: Higher cost per query

**Alternative Considered**: Pure rule-based routing would be faster and cheaper but less flexible.

### 3. **Automatic PII Protection vs. Manual**

**Decision**: Automatic PII detection and masking

**Trade-offs**:
- **Pros**: No manual intervention required
- **Pros**: Consistent privacy protection
- **Pros**: Reduces risk of data leaks
- **Cons**: May mask non-sensitive fields with similar names
- **Cons**: Pattern-based detection may have false positives

**Alternative Considered**: Manual PII marking would be more precise but error-prone and labor-intensive.

### 4. **Single vs. Multi-Tool Queries**

**Decision**: Support both single and multi-tool queries with synthesis

**Trade-offs**:
- **Pros**: Handles simple and complex queries seamlessly
- **Pros**: Single-tool queries are fast (no synthesis overhead)
- **Pros**: Multi-tool queries provide comprehensive answers
- **Cons**: Synthesis adds latency and cost
- **Cons**: More complex error handling

**Alternative Considered**: Always synthesizing would simplify code but add unnecessary overhead for simple queries.

### 5. **Lazy vs. Eager Tool Initialization**

**Decision**: Lazy initialization (tools created on first query)

**Trade-offs**:
- **Pros**: Faster startup time
- **Pros**: Lower memory usage if tools aren't used
- **Pros**: Better for interactive development
- **Cons**: First query has higher latency
- **Cons**: Errors discovered later in workflow

**Alternative Considered**: Eager initialization would catch errors earlier but slow startup.

### 6. **SQL Generation: Single vs. Multiple Attempts**

**Decision**: Two-attempt SQL generation with error context

**Trade-offs**:
- **Pros**: Handles common SQL errors automatically
- **Pros**: Improves success rate without manual intervention
- **Cons**: Adds latency on failures
- **Cons**: May still fail on complex queries

**Alternative Considered**: Single attempt would be faster but less robust.

### 7. **Market Data: Real-Time vs. Cached**

**Decision**: Real-time API calls (no caching)

**Trade-offs**:
- **Pros**: Always current data
- **Pros**: No stale data issues
- **Cons**: Higher latency
- **Cons**: API rate limits and failures
- **Cons**: Higher cost

**Alternative Considered**: Caching would improve performance but risk stale data in financial context.

## Key Features & Capabilities

### 1. **Intelligent Multi-Tool Coordination**

The system can handle queries that require multiple data sources:

```python
# Example: Complex multi-tool query
query = "How does Tesla's supply chain strategy from their 10-K align with our customers' TSLA holdings and current stock performance?"

# System automatically:
# 1. Routes to TSLA_10k_filing_tool for document analysis
# 2. Routes to database_query_tool to find TSLA holders
# 3. Routes to finance_market_search_tool for current price
# 4. Synthesizes all information into coherent answer
# 5. Applies PII protection to customer data
```

### 2. **Natural Language to SQL Conversion**

Users can query the database in plain English:

```python
# Natural language query
query = "Show me all customers who own Tesla stock"

# System generates SQL:
# SELECT c.first_name, c.last_name, ph.symbol, ph.shares
# FROM customers c
# JOIN portfolio_holdings ph ON c.id = ph.customer_id
# WHERE ph.symbol = 'TSLA'

# Returns formatted results with automatic PII masking
```

### 3. **Real-Time Market Data Integration**

Live stock prices and market information:

```python
query = "What's the current price of Apple and Tesla stock?"

# Fetches real-time data from Yahoo Finance:
# AAPL: $175.43 (+2.3%)
# TSLA: $248.50 (-1.2%)
```

### 4. **Automatic PII Protection**

Sensitive information is automatically detected and masked:

```python
# Database query returns customer email: "john.doe@example.com"
# System automatically masks to: "***@example.com"

# Phone number: "555-123-4567" → "***-***-4567"
# Customer name: "John Doe" → "****"
```

### 5. **Document RAG for SEC Filings**

Semantic search across company 10-K filings:

```python
query = "What are Apple's main business risks according to their 10-K?"

# System searches vector index of AAPL_10K_2024.pdf
# Returns relevant sections about risk factors
# Provides citations and context
```

## System Capabilities

### Supported Query Types

1. **Document Analysis Queries**
   - Company business strategies
   - Financial performance analysis
   - Risk factor identification
   - Competitive positioning

2. **Database Queries**
   - Customer portfolio analysis
   - Holdings by company
   - Investment profile matching
   - Portfolio value calculations

3. **Market Data Queries**
   - Current stock prices
   - Price changes and trends
   - Trading volumes
   - Market capitalization

4. **Multi-Source Queries**
   - Compare company strategy with customer holdings
   - Analyze market performance with portfolio data
   - Cross-reference documents with database

### Example Use Cases

1. **Portfolio Analysis**: "Which customers own Tesla stock and what does Tesla's 10-K say about their growth strategy?"
2. **Risk Assessment**: "What are Apple's main risks and how many of our customers are exposed?"
3. **Market Intelligence**: "Compare current GOOGL price with what our Google customers paid"
4. **Strategic Planning**: "Analyze Tesla's supply chain risks and show customer TSLA holdings"

## Getting Started

### Prerequisites

- Python 3.9 or higher
- OpenAI API key (or Vocareum API access)
- Internet connection (for Yahoo Finance API)

### Installation

```bash
# Clone the repository
git clone https://github.com/Imsharad/finance-agent-01.git
cd finance-agent-01

# Navigate to starter code
cd project/starter_code

# Create virtual environment
uv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
uv sync

# Set up environment variables
cp .env.example .env
# Edit .env and add your OpenAI API key:
# OPENAI_API_KEY=your_key_here
# OPENAI_API_BASE=https://api.openai.com/v1  # or Vocareum endpoint
```

### Database Setup

```bash
# Initialize the sample database
python data/build_database.py
```

This creates a SQLite database with:
- Sample customer data
- Portfolio holdings
- Company information
- Financial metrics
- Market data

### Running the System

```python
from helper_modules.agent_coordinator import AgentCoordinator

# Initialize the agent
agent = AgentCoordinator(verbose=True)

# Ask a question
response = agent.query("What are Apple's main business risks?")
print(response)
```

### Testing

```bash
# Test individual components
python tests/test_document_tools.py
python tests/test_function_tools.py
python tests/test_agent_coordinator.py

# Run comprehensive walkthrough
jupyter notebook financial_agent_walkthrough.ipynb
```

## Project Structure

```
finance-agent-01/
├── README.md                          # This file
├── .gitignore                         # Git ignore rules
├── docs/                              # Documentation
│   ├── architecture.md                # System architecture details
│   ├── overview.md                    # Project overview
│   ├── instructions.md                # Implementation guide
│   └── diagrams/                      # Architecture diagrams
├── memory/                            # Project planning notes
├── project/
│   ├── README.md                      # Project structure summary
│   └── starter_code/                  # Main implementation
│       ├── README.md                  # Detailed instructions
│       ├── pyproject.toml             # Dependencies
│       ├── helper_modules/            # Core implementation
│       │   ├── document_tools.py      # Document RAG tools
│       │   ├── function_tools.py     # Database, market, PII tools
│       │   └── agent_coordinator.py  # Multi-tool coordination
│       ├── data/
│       │   ├── financial.db           # SQLite database
│       │   ├── build_database.py     # Database setup script
│       │   └── 10k_documents/        # SEC filing PDFs
│       │       ├── AAPL_10K_2024.pdf
│       │       ├── GOOGL_10K_2024.pdf
│       │       └── TSLA_10K_2024.pdf
│       ├── tests/                     # Test suite
│       └── financial_agent_walkthrough.ipynb  # Testing notebook
```

## Learning Objectives

This project demonstrates:

1. **Agentic AI Architecture**: Building systems that can reason about tool selection
2. **Multi-Tool Coordination**: Orchestrating multiple specialized tools
3. **RAG Implementation**: Document processing with vector search
4. **Natural Language Interfaces**: Converting user queries to structured operations
5. **Privacy Engineering**: Automatic PII detection and protection
6. **API Integration**: Real-time data fetching from external sources
7. **Error Handling**: Robust error handling with fallbacks
8. **Modular Design**: Clean, maintainable, testable architecture

## Security & Privacy

- **Automatic PII Detection**: Pattern-based identification of sensitive fields
- **Intelligent Masking**: Type-specific masking strategies
- **Transparent Protection**: Users notified when PII is masked
- **No Data Storage**: Queries processed without storing user data
- **API Key Security**: Environment variables for sensitive credentials

## Limitations & Future Enhancements

### Current Limitations

1. **Fixed Company Set**: Only supports AAPL, GOOGL, TSLA (can be extended)
2. **Single Database**: SQLite database (can be migrated to PostgreSQL)
3. **No Caching**: Market data fetched fresh each time (could add caching)
4. **Limited Error Recovery**: Some edge cases may require manual intervention
5. **Synchronous Processing**: All tools execute sequentially (could parallelize)

### Potential Enhancements

1. **Additional Data Sources**: News articles, earnings reports, analyst ratings
2. **Advanced Analytics**: Portfolio optimization, risk scoring, trend analysis
3. **User Authentication**: Multi-user support with role-based access
4. **Caching Layer**: Redis for market data and query results
5. **Streaming Responses**: Real-time updates for market data
6. **Multi-Language Support**: Internationalization for global users
7. **Advanced PII Detection**: ML-based detection beyond pattern matching
8. **Query History**: Learning from past queries to improve routing

## Additional Resources

- [LlamaIndex Documentation](https://docs.llamaindex.ai/)
- [OpenAI API Reference](https://platform.openai.com/docs)
- [Yahoo Finance API](https://pypi.org/project/yfinance/)
- [SQLite Documentation](https://www.sqlite.org/docs.html)

## Contributing

This is an educational project demonstrating agentic AI principles. Contributions, suggestions, and improvements are welcome!

## License

This project is for educational purposes as part of the Udacity Building Agents course.

## Author

Built as part of the Udacity Building Agents specialization, demonstrating advanced agentic AI capabilities for financial services applications.

---

**Key Achievement**: This project successfully demonstrates how to build a production-ready agentic AI system that intelligently coordinates multiple tools, handles complex multi-source queries, and maintains privacy standards—all essential skills for building real-world AI agents in financial services.
