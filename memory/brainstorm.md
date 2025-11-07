# Finance Agent Project - Implementation Brainstorm

## Architecture Overview

The system follows a modular 3-layer architecture:

```
┌─────────────────────────────────────┐
│     AgentCoordinator                 │
│  (Intelligent Routing & Synthesis)   │
└──────────────┬───────────────────────┘
               │
       ┌───────┴────────┐
       │                │
┌──────▼──────┐  ┌──────▼──────────┐
│ Document    │  │ Function       │
│ Tools       │  │ Tools          │
│ Manager     │  │ Manager        │
└─────────────┘  └────────────────┘
```

## Key Design Decisions

### 1. Vocareum API Compatibility
**Challenge**: Must work with Vocareum's OpenAI endpoint, not standard OpenAI API
**Solution**: 
- Use `api_base` parameter for all OpenAI/OpenAIEmbedding instances
- Get from environment: `os.getenv("OPENAI_API_BASE", "https://openai.vocareum.com/v1")`
- Apply consistently across all three modules

### 2. Tool Routing Strategy
**Challenge**: Need intelligent tool selection based on query content
**Solution**:
- Use LLM to analyze query and select appropriate tools
- Build prompt with:
  - Query text
  - Available tools with descriptions
  - Routing guidelines (database → customers, market → prices, documents → company info)
- Parse LLM response to get tool indices/names
- Execute selected tools and collect results

### 3. PII Protection Coordination
**Challenge**: Automatically detect and protect sensitive data without manual intervention
**Solution**:
- Database results include "COLUMNS:" prefix for detection
- Coordinator detects PII fields using pattern matching
- Automatically invokes PII protection tool when sensitive fields detected
- Non-database results bypass PII processing for performance

### 4. Result Synthesis
**Challenge**: Combine results from multiple tools into coherent answer
**Solution**:
- Single tool results: return directly
- Multiple tool results: use LLM to synthesize
- Build synthesis prompt with:
  - Original query
  - All tool results
  - Instructions to integrate information coherently

## Implementation Strategy

### Phase 1: Document Tools (Foundation)
**Why First**: Simplest component, establishes patterns for LlamaIndex usage

**Key Steps**:
1. Configure Settings with Vocareum compatibility
2. Load PDFs, split into chunks, create vector indices
3. Wrap in QueryEngineTool objects

**Pattern to Follow**:
```python
# Configure
Settings.llm = OpenAI(model="gpt-3.5-turbo", temperature=0, api_base=api_base)
Settings.embed_model = OpenAIEmbedding(model="text-embedding-ada-002", api_base=api_base)

# Load & Process
documents = SimpleDirectoryReader(input_files=[pdf_path]).load_data()
nodes = SentenceSplitter().get_nodes_from_documents(documents)
index = VectorStoreIndex(nodes)
query_engine = index.as_query_engine()

# Wrap Tool
tool = QueryEngineTool.from_defaults(
    query_engine=query_engine,
    name=f"{SYMBOL}_10k_filing_tool",
    description="..."
)
```

### Phase 2: Function Tools (Most Complex)
**Why Second**: Builds on LlamaIndex patterns, adds custom logic

**Key Challenges**:
1. **SQL Generation**: Natural language → SQL using LLM
   - Provide database schema in prompt
   - Handle SQL syntax errors with retry logic
   - Format results with column names

2. **Market Data**: Yahoo Finance API integration
   - Parse query to identify companies
   - Make API calls with error handling
   - Format financial data clearly

3. **PII Protection**: Pattern-based detection and masking
   - Field name patterns (email, phone, name, etc.)
   - Field-specific masking strategies
   - Preserve non-PII data readability

**Pattern to Follow**:
```python
# Function Tool Creation
def my_function(param: str) -> str:
    """Tool description"""
    # Implementation
    return result

tool = FunctionTool.from_defaults(
    fn=my_function,
    name="tool_name",
    description="Tool description for routing"
)
```

### Phase 3: Agent Coordinator (Orchestration)
**Why Last**: Depends on both previous modules

**Key Challenges**:
1. **Tool Routing**: LLM-based selection
   - Build tool descriptions
   - Create routing prompt
   - Parse LLM response
   - Execute selected tools

2. **Result Synthesis**: Multi-source integration
   - Detect when synthesis needed
   - Build synthesis prompt
   - Generate coherent answer

**Pattern to Follow**:
```python
# Routing Prompt Structure
prompt = f"""
Query: {query}

Available Tools:
{tool_descriptions}

Guidelines:
- Database queries → database_query_tool
- Market prices → finance_market_search_tool
- Company info → document tools
- Select appropriate tools (can be multiple)

Selected tools: [tool indices or names]
"""

# Execute Tools
results = []
for tool_info in selected_tools:
    if is_document_tool:
        result = tool.query_engine.query(query)
    else:
        result = tool.call(query)
    results.append((tool_name, tool_desc, result))
```

## Error Handling Strategy

### Database Errors
- SQL syntax errors → retry with error context
- Connection errors → graceful failure message
- Empty results → informative message

### API Errors
- Network failures → fallback message
- Invalid responses → error handling
- Rate limits → retry logic

### LLM Errors
- API failures → graceful degradation
- Invalid responses → fallback to simple routing
- Timeout → retry once

## Testing Strategy

1. **Unit Tests**: Each module independently
   - Test configuration
   - Test tool creation
   - Test individual functions

2. **Integration Tests**: Modules together
   - Test coordinator with all tools
   - Test routing decisions
   - Test result synthesis

3. **End-to-End**: Walkthrough notebook
   - All query types
   - PII protection
   - Multi-tool coordination

## Common Pitfalls to Avoid

1. **Forgetting Vocareum API Base**: Always use `api_base` parameter
2. **Missing Column Information**: Database results must include "COLUMNS:" prefix
3. **Tool Naming**: Must match exact patterns for tests
4. **Error Handling**: Don't leave placeholder error messages
5. **Result Formatting**: Ensure consistent format for synthesis

## Success Metrics

✅ All 6 tools created successfully
✅ Tests pass for all modules
✅ Walkthrough notebook runs end-to-end
✅ PII protection activates automatically
✅ Multi-tool queries produce coherent results
✅ No placeholder code remains

## Next Steps

1. Start with `document_tools.py` - simplest component
2. Move to `function_tools.py` - most complex, take time
3. Finish with `agent_coordinator.py` - orchestration layer
4. Test incrementally after each component
5. Polish and document

---

**Ready to begin implementation!**
