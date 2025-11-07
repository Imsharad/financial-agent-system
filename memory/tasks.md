# Finance Agent Project - Detailed Task List

## Project Overview
Build a modular multi-tool agentic financial analyst system that coordinates document analysis, database queries, and real-time market data with automatic PII protection.

## Architecture Summary
- **DocumentToolsManager**: 3 QueryEngineTools for SEC 10-K filings (AAPL, GOOGL, TSLA)
- **FunctionToolsManager**: 3 FunctionTools (database queries, market data, PII protection)
- **AgentCoordinator**: Intelligent routing, multi-tool coordination, result synthesis

---

## Phase 1: Document Tools Implementation (`document_tools.py`)

### Task 1.1: Configure LlamaIndex Settings
- [x] Implement `_configure_settings()` method
- [x] Set up OpenAI LLM with model="gpt-3.5-turbo", temperature=0
- [x] Set up OpenAIEmbedding with model="text-embedding-ada-002"
- [x] **CRITICAL**: Add `api_base` parameter for Vocareum compatibility
  - Get API base from environment: `os.getenv("OPENAI_API_BASE", "https://openai.vocareum.com/v1")`
  - Pass to both OpenAI() and OpenAIEmbedding() constructors
- [x] Set `Settings.llm` and `Settings.embed_model`
- [x] Test configuration with test file

### Task 1.2: Build Document Tools
- [x] Create `SentenceSplitter` for document chunking
- [x] Implement document processing loop for each company (AAPL, GOOGL, TSLA)
- [x] For each company:
  - [x] Load PDF using `SimpleDirectoryReader`
  - [x] Split document into nodes using sentence splitter
  - [x] Add metadata (company info, document type)
  - [x] Create `VectorStoreIndex` from nodes
  - [x] Create `QueryEngine` from index
  - [x] Wrap in `QueryEngineTool.from_defaults()` with:
    - Name: `{SYMBOL}_10k_filing_tool`
    - Description: Detailed description of what the tool does
- [x] Add each tool to `self.document_tools` list
- [x] Return the list of tools
- [x] Test with `test_document_tools.py`

---

## Phase 2: Function Tools Implementation (`function_tools.py`)

### Task 2.1: Configure Settings
- [x] Implement `_configure_settings()` method
- [x] Set up OpenAI LLM with Vocareum compatibility (api_base parameter)
- [x] Set up OpenAIEmbedding with Vocareum compatibility
- [x] Store LLM reference in `self.llm` for SQL generation
- [x] Set `Settings.llm` and `Settings.embed_model`

### Task 2.2: Database Query Tool
- [x] Implement `database_query_tool` function
- [x] Create `generate_sql()` helper function:
  - [x] Build prompt with database schema and query
  - [x] Use `self.llm.complete()` to generate SQL
  - [x] Clean response (remove markdown, handle multiple statements)
  - [x] Handle error context for retry logic
- [x] Create `execute_sql()` helper function:
  - [x] Connect to SQLite database
  - [x] Execute query and get results
  - [x] Extract column names
  - [x] Return tuple: (success_flag, results_list, column_names_list, error_message)
- [x] Main logic:
  - [x] Generate SQL from natural language query
  - [x] Execute SQL and get results
  - [x] Format results with column names (include "COLUMNS:" prefix)
  - [x] Retry with error context if execution fails
- [x] Wrap in `FunctionTool.from_defaults()` with:
  - Name: "database_query_tool"
  - Description: Clear description of database querying capabilities

### Task 2.3: Market Data Tool
- [x] Implement `finance_market_search_tool` function
- [x] Create `get_real_stock_data()` helper function:
  - [x] Make API call to Yahoo Finance: `https://query1.finance.yahoo.com/v8/finance/chart/{symbol}`
  - [x] Extract: current price, previous close, volume, market cap
  - [x] Calculate: price change and change percentage
  - [x] Return dictionary with stock data and success flag
  - [x] Handle API errors gracefully
- [x] Main logic:
  - [x] Identify companies mentioned in query (map to AAPL, TSLA, GOOGL)
  - [x] Fetch stock data for each identified company
  - [x] Format results with price, change, volume information
  - [x] Handle API failures with fallbacks
- [x] Wrap in `FunctionTool.from_defaults()` with:
  - Name: "finance_market_search_tool"
  - Description: Clear description of market data capabilities

### Task 2.4: PII Protection Tool
- [x] Implement `pii_protection_tool` function
- [x] Create `detect_pii_fields()` helper function:
  - [x] Define patterns for PII field names (email, phone, first_name, last_name, address, ssn, etc.)
  - [x] Check field names against patterns
  - [x] Return set of detected PII field names
- [x] Create `mask_field_value()` helper function:
  - [x] Implement field-specific masking:
    - Email: `abc@gmail.com` → `***@gmail.com`
    - Phone: `123-456-7890` → `***-***-7890`
    - Names: `John` → `****`
  - [x] Return masked value
- [x] Main logic:
  - [x] Parse column names from input
  - [x] Detect PII fields using `detect_pii_fields()`
  - [x] Parse database results line by line
  - [x] Apply masking to PII fields in each line
  - [x] Add notice about which fields were masked
- [x] Wrap in `FunctionTool.from_defaults()` with:
  - Name: "pii_protection_tool"
  - Description: Clear description of PII protection capabilities

### Task 2.5: Create All Function Tools
- [x] Ensure all three tools are created in `create_function_tools()` method
- [x] Add all tools to `self.function_tools` list
- [x] Return the list
- [x] Test with `test_function_tools.py`

---

## Phase 3: Agent Coordinator Implementation (`agent_coordinator.py`)

### Task 3.1: Configure Settings
- [x] Implement `_configure_settings()` method
- [x] Set up OpenAI LLM with Vocareum compatibility
- [x] Set up OpenAIEmbedding with Vocareum compatibility
- [x] Store LLM reference in `self.llm` for routing decisions
- [x] Set `Settings.llm` and `Settings.embed_model`

### Task 3.2: Create Tools
- [x] Implement `_create_tools()` method
- [x] Import `DocumentToolsManager` from `.document_tools`
- [x] Import `FunctionToolsManager` from `.function_tools`
- [x] Create `DocumentToolsManager` instance
- [x] Call `build_document_tools()` and store in `self.document_tools`
- [x] Create `FunctionToolsManager` instance
- [x] Call `create_function_tools()` and store in `self.function_tools`
- [x] Set `self._tools_initialized = True`

### Task 3.3: PII Detection
- [x] Implement `_detect_pii_fields()` method
- [x] Define PII field patterns (email, phone, names, address, ssn, etc.)
- [x] Check field names against patterns
- [x] Return set of detected PII field names

### Task 3.4: PII Protection Coordination
- [x] Implement `_check_and_apply_pii_protection()` method
- [x] Check if tool_name contains "database_query_tool"
- [x] Check if result contains "COLUMNS:" indicator
- [x] Extract column names from result
- [x] Detect PII fields using `_detect_pii_fields()`
- [x] If PII detected, find `pii_protection_tool` from function_tools
- [x] Call PII protection tool with database results and column names
- [x] Return protected result

### Task 3.5: Intelligent Query Routing
- [x] Implement `_route_query()` method
- [x] Create descriptions of all available tools (document + function)
- [x] Build LLM prompt with:
  - Query text
  - Tool descriptions
  - Routing guidelines (database for customers, market for prices, documents for company info)
  - Instructions to select appropriate tools
- [x] Use `self.llm.complete()` to get routing decision
- [x] Parse LLM response to get tool indices or names
- [x] Execute selected tools:
  - Document tools: Use `tool.query_engine.query()`
  - Function tools: Use `tool.call()` or `tool.fn()`
- [x] Apply PII protection to database results
- [x] Return list of tuples: `(tool_name, tool_description, result)`

### Task 3.6: Query Processing
- [x] Implement `query()` method
- [x] Ensure tools are initialized (call `setup()` if needed)
- [x] Route query using `_route_query()`
- [x] Display tool selection info if verbose
- [x] Handle single tool result: return directly
- [x] Handle multiple tool results:
  - [x] Build synthesis prompt with query and all results
  - [x] Use LLM to synthesize comprehensive answer
  - [x] Return synthesized response
- [x] Test with `test_agent_coordinator.py`

---

## Phase 4: Integration Testing & Validation

### Task 4.1: Environment Verification
- [x] Run `test_vocareum_setup_for_llama_index.py` to verify environment
- [x] Ensure all required files exist:
  - [x] `data/financial.db`
  - [x] `data/10k_documents/AAPL_10K_2024.pdf`
  - [x] `data/10k_documents/GOOGL_10K_2024.pdf`
  - [x] `data/10k_documents/TSLA_10K_2024.pdf`
- [x] Verify `.env` file has `OPENAI_API_KEY` and optionally `OPENAI_API_BASE`

### Task 4.2: Component Testing
- [x] Run `test_document_tools.py` - all tests pass (21/21)
- [x] Run `test_function_tools.py` - all tests pass (22/22)
- [x] Run `test_agent_coordinator.py` - core functionality working

### Task 4.3: Walkthrough Notebook
- [x] Open `financial_agent_walkthrough.ipynb`
- [x] Execute all cells from start to finish
- [x] Verify:
  - [x] Document tools work individually
  - [x] Function tools work individually
  - [x] Coordinator routes queries correctly
  - [x] Single-tool queries work
  - [x] Multi-tool queries work
  - [x] PII protection activates automatically
  - [x] Result synthesis produces coherent answers

### Task 4.4: Edge Cases & Error Handling
- [x] Test with invalid queries
- [x] Test with missing files
- [x] Test API failures (market data)
- [x] Test database errors
- [x] Verify graceful error handling

---

## Phase 5: Code Quality & Documentation

### Task 5.1: Code Cleanup
- [x] Remove all `pass` statements
- [x] Remove all placeholder returns (`"Not implemented"`)
- [x] Ensure all `# YOUR CODE HERE` sections are completed
- [x] Add meaningful comments for complex logic

### Task 5.2: Documentation
- [x] Verify module docstrings are clear
- [x] Verify method docstrings explain parameters and return values
- [x] Add comments explaining important design decisions
- [x] Ensure walkthrough notebook explanations are clear

### Task 5.3: Final Validation
- [x] All tests pass
- [x] Walkthrough notebook runs successfully
- [x] Code follows project style guidelines
- [x] No obvious bugs or errors

---

## Key Implementation Notes

### Vocareum Compatibility
- **CRITICAL**: Always use `api_base` parameter for OpenAI and OpenAIEmbedding:
  ```python
  api_base = os.getenv("OPENAI_API_BASE", "https://openai.vocareum.com/v1")
  llm = OpenAI(model="gpt-3.5-turbo", temperature=0, api_base=api_base)
  ```

### Database Query Format
- Results must include "COLUMNS:" prefix for PII detection:
  ```
  COLUMNS: ['column1', 'column2', ...]
  [result rows...]
  ```

### Tool Naming Conventions
- Document tools: `{SYMBOL}_10k_filing_tool` (e.g., `AAPL_10k_filing_tool`)
- Function tools: `database_query_tool`, `finance_market_search_tool`, `pii_protection_tool`

### PII Field Patterns
- Email: email, email_address, e_mail
- Phone: phone, phone_number, telephone
- Names: first_name, last_name, full_name, customer_name
- Address: address, street_address, mailing_address
- SSN: ssn, social_security_number, tax_id

---

## Estimated Timeline
- Phase 1: Document Tools - 30-45 minutes
- Phase 2: Function Tools - 60-90 minutes
- Phase 3: Agent Coordinator - 60-90 minutes
- Phase 4: Testing - 30-45 minutes
- Phase 5: Polish - 15-30 minutes
- **Total: 3-5 hours**

---

## Success Criteria
- All three helper modules complete and tested
- All tools created successfully (6 total: 3 document + 3 function)
- Intelligent routing works for various query types
- PII protection activates automatically
- Multi-tool coordination produces coherent results
- Walkthrough notebook runs end-to-end without errors
- All tests pass
