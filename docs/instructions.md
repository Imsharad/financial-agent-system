Your implementation follows a  **4-step approach** , building from individual components to complete system integration. The three core scripts in the **helper_modules/** directory form the foundation of your agentic system. Each script contains strategic `# YOUR CODE HERE` placeholders where you'll implement key functionality.

### Step 1: Document Tools (`helper_modules/document_tools.py`)

 **Your Task** : Complete the DocumentToolsManager class for individual RAG systems

 **Implementation Areas** :

* Complete `_configure_settings()`: Set up LlamaIndex configurations with OpenAI LLM and embeddings
* Complete `build_document_tools()`: Create QueryEngineTools for each company's 10-K filing (AAPL, GOOGL, TSLA)

 **Key Learning Goals** :

* PDF document processing with LlamaIndex
* Vector embedding and indexing strategies
* Query engine creation for document retrieval
* Tool naming and metadata configuration
* Vocareum API compatibility with `api_base` parameter

 **What's Provided** :

* Class structure and method signatures
* Document loading utilities and chunking guidance
* Index creation templates with helpful comments
* Vocareum-specific configuration notes

 **Test Your Work** :

<pre class="css-0"><div data-defines-codeblock="true" tabindex="0" class="css-ift61f"><div class="css-1wj0762"></div><div><code class="language-bash"><span>python tests/test_document_tools.py</span></code></div></div></pre>

### Step 2: Function Tools (`helper_modules/function_tools.py`)

 **Your Task** : Complete the FunctionToolsManager class for database and market data functionality

 **Implementation Areas** :

* Complete `create_function_tools()`: Build three core function tools:
  * **Database query tool** : Natural language to SQL converter with error handling
  * **Market search tool** : Real-time market data fetcher via Yahoo Finance API
  * **PII protection tool** : Automatic sensitive data masking system

 **Key Learning Goals** :

* Natural language to SQL conversion using LLM
* Real-time API integration (Yahoo Finance)
* Privacy protection and data masking techniques
* FunctionTool creation and parameter validation

 **What's Provided** :

* Database schema reference with example queries and relationships
* API integration templates with error handling patterns
* PII detection patterns and masking examples
* Function structure with TODO markers for implementation

 **Test Your Work** :

<pre class="css-0"><div data-defines-codeblock="true" tabindex="0" class="css-ift61f"><div class="css-1wj0762"></div><div><code class="language-bash"><span>python tests/test_function_tools.py</span></code></div></div></pre>

### Step 3: Agent Coordination (`helper_modules/agent_coordinator.py`)

 **Your Task** : Complete the AgentCoordinator class for intelligent multi-tool orchestration

 **Implementation Areas** :

* Complete `_configure_settings()`: Set up LLM and embedding models with Vocareum compatibility
* Complete `_create_tools()`: Initialize document and function tools using helper modules
* Complete `_route_query()`: Implement intelligent LLM-based tool routing logic
* Complete `query()`: Main query processing with multi-tool coordination and result synthesis

 **Key Learning Goals** :

* LLM-based intelligent tool routing and selection
* Multi-tool coordination and result synthesis
* Automatic PII detection and protection workflow
* Response formatting from multiple data sources

 **What's Provided** :

* Complete class structure with helper methods
* Tool management and status tracking
* Error handling framework
* PII field detection patterns

 **Test Your Work** :

<pre class="css-0"><div data-defines-codeblock="true" tabindex="0" class="css-ift61f"><div class="css-1wj0762"></div><div><code class="language-bash"><span>python tests/test_agent_coordinator.py</span></code></div></div></pre>

### Step 4: Validation & Testing (`financial_agent_walkthrough.ipynb`)

 **Your Task** : Once you complete the helper modules, run this comprehensive walkthrough

 **Testing Scenarios** :

* Individual tool functionality verification
* Multi-tool coordination examples
* PII protection validation
* Complex financial analysis workflows

 **What It Provides** :

* Complete testing framework for validating your implementations
* Example queries demonstrating system capabilities
* Performance validation and debugging guidance

---

## ✅ Testing & Validation

### Vocareum Setup Verification

 **Before implementing any code** , verify your environment is configured correctly:

<pre class="css-0"><div data-defines-codeblock="true" tabindex="0" class="css-ift61f"><div class="css-1wj0762"></div><div><code class="language-bash"><span>python tests/test_vocareum_setup_for_llama_index.py</span></code></div></div></pre>

This validates:

* Environment variables are set correctly
* LlamaIndex components import successfully
* OpenAI models initialize with `api_base` parameter
* All helper modules have correct Vocareum configuration

### Component Testing

Run individual tests as you complete each module:

**Test Document Tools:**

<pre class="css-0"><div data-defines-codeblock="true" tabindex="0" class="css-ift61f"><div class="css-1wj0762"></div><div><code class="language-bash"><span>python tests/test_document_tools.py</span></code></div></div></pre>

Validates: PDF loading, vector indexing, query engine creation, tool metadata

**Test Function Tools:**

<pre class="css-0"><div data-defines-codeblock="true" tabindex="0" class="css-ift61f"><div class="css-1wj0762"></div><div><code class="language-bash"><span>python tests/test_function_tools.py</span></code></div></div></pre>

Validates: SQL generation, database queries, market data API, PII masking

**Test Agent Coordinator:**

<pre class="css-0"><div data-defines-codeblock="true" tabindex="0" class="css-ift61f"><div class="css-1wj0762"></div><div><code class="language-bash"><span>python tests/test_agent_coordinator.py</span></code></div></div></pre>

Validates: Tool routing, multi-tool coordination, PII protection, result synthesis

### Integration Testing

Once all components pass individual tests, run the complete walkthrough:

<pre class="css-0"><div data-defines-codeblock="true" tabindex="0" class="css-ift61f"><div class="css-1wj0762"></div><div><code class="language-bash"><span>jupyter notebook financial_agent_walkthrough.ipynb</span></code></div></div></pre>

Execute all cells from start to finish to verify:

* End-to-end query processing works correctly
* Multi-tool coordination produces coherent results
* PII protection activates automatically when needed
* System handles diverse query types successfully

---

Your project will be evaluated based on the comprehensive Project Rubric.

## 💡 Tips for Success

1. **Start with Vocareum Validation** : Run the setup test first to ensure your configuration is correct before writing any code.
2. **Build Incrementally** : Complete one module at a time and test thoroughly before moving to the next. Don't try to implement everything at once.
3. **Use the Provided Schema** : The database schema in FunctionToolsManager is comprehensive. Study it to understand how to generate effective SQL queries.
4. **Test Individual Tools First** : Before testing the full coordinator, make sure each tool works independently. This makes debugging much easier.
5. **Pay Attention to PII** : The automatic PII protection is a key feature. Make sure you understand how column names trigger protection and how the coordination works.
6. **Study the Solution Notebook** : The walkthrough notebook shows exactly how the system should behave. Use it as a reference for expected behavior.
7. **Read Error Messages Carefully** : LLM responses, API errors, and database errors provide valuable debugging information. Don't ignore them.

---

## 📚 Additional Resources

* **LlamaIndex Documentation** : [https://docs.llamaindex.ai/(opens in a new tab)](https://docs.llamaindex.ai/)
* **OpenAI API Reference** : [https://platform.openai.com/docs(opens in a new tab)](https://platform.openai.com/docs)
* **Yahoo Finance API** : [https://pypi.org/project/yfinance/(opens in a new tab)](https://pypi.org/project/yfinance/)
* **Pydantic Documentation** : [https://docs.pydantic.dev/(opens in a new tab)](https://docs.pydantic.dev/)
* **SQLite Documentation** : [https://www.sqlite.org/docs.html(opens in a new tab)](https://www.sqlite.org/docs.html)

Good luck with your implementation! 🎓
