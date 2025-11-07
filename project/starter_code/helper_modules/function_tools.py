"""
Function Tools Module - Database queries, market data, and PII protection

This module provides function-based tools for SQL generation, market data retrieval,
and PII protection. These are the core business logic tools that enable the agent
to access database information and current market data.

Learning Objectives:
- Understand function tool creation with LlamaIndex
- Implement database querying with SQL generation
- Create market data retrieval tools
- Build PII protection mechanisms
- Learn about real-time API integration

Your Task: Complete the missing implementations marked with YOUR CODE HERE

Key Concepts:
1. FunctionTool Creation: Wrap Python functions as LlamaIndex tools
2. SQL Generation: Use LLM to generate SQL from natural language
3. Database Operations: Execute SQL queries and format results  
4. API Integration: Fetch real-time market data from external APIs
5. PII Protection: Automatically mask sensitive information
"""

import os
import logging
import sqlite3
import random
import re
import json
import requests
from pathlib import Path
from typing import List, Tuple

# LlamaIndex imports
from llama_index.core import Settings
from llama_index.core.tools import FunctionTool
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding

# Environment setup
from dotenv import load_dotenv
load_dotenv()

# Configure logging
logger = logging.getLogger(__name__)

class FunctionToolsManager:
    """Manager for all function tools - Database, market data, and PII protection"""
    
    def __init__(self, verbose: bool = False):
        """Initialize function tools manager
        
        Args:
            verbose: Whether to print detailed progress information
        """
        self.verbose = verbose
        self.project_root = Path.cwd()
        self.db_path = self.project_root / "data" / "financial.db"
        
        # Database schema for SQL generation
        self.db_schema = self._get_database_schema()
        
        # Storage for tools
        self.function_tools = []
        
        self._configure_settings()
        
        if self.verbose:
            print("✅ Function Tools Manager Initialized")
    
    def _configure_settings(self):
        """Configure LlamaIndex settings
        
        Requirements:
        - Create OpenAI LLM with "gpt-3.5-turbo" model and temperature=0
        - Set Settings.llm and Settings.embed_model
        - Store LLM reference in self.llm for use in tools
        
        IMPORTANT NOTE FOR VOCAREUM:
        LlamaIndex requires the api_base parameter to work with Vocareum's OpenAI endpoint.
        Get the base URL from environment: os.getenv("OPENAI_API_BASE", "https://openai.vocareum.com/v1")
        Pass it as api_base parameter to both OpenAI() and OpenAIEmbedding() constructors.
        
        Hint: This is similar to document_tools configuration
        """
        # Get API base URL for Vocareum compatibility
        api_base = os.getenv("OPENAI_API_BASE", "https://openai.vocareum.com/v1")
        
        # Create OpenAI LLM with Vocareum compatibility
        self.llm = OpenAI(
            model="gpt-3.5-turbo",
            temperature=0,
            api_base=api_base
        )
        
        # Create OpenAI embeddings with Vocareum compatibility
        embed_model = OpenAIEmbedding(
            model="text-embedding-ada-002",
            api_base=api_base
        )
        
        # Set global LlamaIndex settings
        Settings.llm = self.llm
        Settings.embed_model = embed_model
    
    def _get_database_schema(self) -> str:
        """Get enhanced database schema with relationships for SQL generation
        
        This method reads the database structure and returns a comprehensive
        schema description that helps the LLM generate better SQL queries.
        
        Returns:
            String containing detailed database schema with table relationships
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Get table names to verify database connection
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            
            # Return comprehensive schema for SQL generation
            schema_info = """Enhanced Database Schema with Relationships:

TABLE: customers (Customer Information)
- id (PRIMARY KEY, INTEGER) - Unique customer identifier
- first_name (TEXT) - Customer first name
- last_name (TEXT) - Customer last name  
- email (TEXT) - Customer email address
- phone (TEXT) - Customer phone number
- investment_profile (TEXT) - conservative/moderate/aggressive
- risk_tolerance (TEXT) - low/medium/high

TABLE: portfolio_holdings (Customer Stock Holdings)
- id (PRIMARY KEY, INTEGER) - Unique holding record
- customer_id (FOREIGN KEY → customers.id) - Links to customer
- symbol (TEXT) - Stock symbol like 'AAPL', 'TSLA', 'MSFT', 'GOOGL'
- shares (REAL) - Number of shares owned
- purchase_price (REAL) - Price when purchased
- current_value (REAL) - Current total value of holding

TABLE: companies (Company Master Data)
- id (PRIMARY KEY, INTEGER) - Unique company identifier
- symbol (TEXT) - Stock symbol like 'AAPL', 'TSLA', 'MSFT', 'GOOGL'
- name (TEXT) - Company name like 'Apple Inc', 'Tesla Inc'
- sector (TEXT) - Business sector (technology, automotive, etc.)
- market_cap (REAL) - Market capitalization

TABLE: financial_metrics (Company Financial Data)
- id (PRIMARY KEY, INTEGER) - Unique metrics record
- symbol (FOREIGN KEY → companies.symbol) - Stock symbol
- revenue (REAL) - Company revenue
- net_income (REAL) - Net income
- eps (REAL) - Earnings per share
- pe_ratio (REAL) - Price to earnings ratio
- debt_to_equity (REAL) - Debt to equity ratio
- roe (REAL) - Return on equity

TABLE: market_data (Current Market Information)
- id (PRIMARY KEY, INTEGER) - Unique market record
- symbol (FOREIGN KEY → companies.symbol) - Stock symbol
- close_price (REAL) - Latest closing price
- volume (INTEGER) - Trading volume
- market_cap (REAL) - Current market cap
- date (TEXT) - Date of data

COMMON QUERY PATTERNS & JOINS:

1. Customer holdings with names:
   SELECT c.first_name, c.last_name, ph.symbol, ph.shares, ph.current_value
   FROM customers c 
   JOIN portfolio_holdings ph ON c.id = ph.customer_id

2. Holdings with company information:
   SELECT ph.symbol, co.name, ph.shares, ph.current_value, co.sector
   FROM portfolio_holdings ph
   JOIN companies co ON ph.symbol = co.symbol

3. Holdings with current market prices:
   SELECT ph.symbol, ph.shares, ph.current_value, md.close_price
   FROM portfolio_holdings ph
   JOIN market_data md ON ph.symbol = md.symbol

4. Complete customer portfolio view:
   SELECT c.first_name, c.last_name, co.name, ph.shares, 
          ph.current_value, md.close_price, co.sector
   FROM customers c
   JOIN portfolio_holdings ph ON c.id = ph.customer_id
   JOIN companies co ON ph.symbol = co.symbol
   JOIN market_data md ON ph.symbol = md.symbol

KEY TIPS:
- Use LIKE '%Tesla%' or LIKE '%Apple%' for company name searches
- Use symbol = 'TSLA', 'AAPL', 'MSFT', 'GOOGL' for exact stock matches
- JOIN portfolio_holdings with customers to get customer names
- JOIN with companies to get full company names and sectors
- JOIN with market_data to get current prices and volumes
"""
            
            conn.close()
            return schema_info
            
        except Exception as e:
            return f"Schema error: {e}\n\nFallback basic schema available."
    
    def create_function_tools(self):
        """Create function tools for database, market data, and PII protection
        
        This method creates three main function tools:
        1. Database Query Tool - Generates and executes SQL queries
        2. Market Search Tool - Fetches real-time stock data
        3. PII Protection Tool - Masks sensitive information
        
        Returns:
            List of FunctionTool objects
        """
        if self.verbose:
            print("🛠️ Creating function tools...")
        
        # Clear existing tools
        self.function_tools = []
        
        # Create the three main function tools
        # Implement these three nested functions and wrap them with FunctionTool:
        # 1. database_query_tool - Natural language to SQL conversion and execution
        # 2. finance_market_search_tool - Real-time Yahoo Finance API integration
        # 3. pii_protection_tool - Automatic PII detection and masking
        
        # 1. DATABASE QUERY TOOL
        def database_query_tool(query: str) -> str:
            """Generate and execute SQL queries for customer/portfolio database
            
            This tool takes a natural language query, converts it to SQL using
            the LLM, executes it against the database, and returns formatted results.
            
            Args:
                query: Natural language question about the database
                
            Returns:
                String containing SQL query and formatted results
            """
            
            def generate_sql(query_text: str, error_context: str = None) -> str:
                """Generate SQL query from natural language using LLM"""
                # Build prompt with database schema and query
                prompt = f"""You are a SQL expert. Convert the following natural language query into a valid SQLite SQL query.

Database Schema:
{self.db_schema}

Natural Language Query: {query_text}
"""
                
                # Add error context if retrying after a failed query
                if error_context:
                    prompt += f"\nPrevious SQL query failed with error: {error_context}\nPlease fix the SQL query."
                
                prompt += "\n\nGenerate ONLY the SQL query, no explanations, no markdown formatting. Return only the SQL statement."
                
                try:
                    # Use LLM to generate SQL
                    response = self.llm.complete(prompt)
                    sql_query = str(response.text).strip()
                    
                    # Clean up response - remove markdown code blocks if present
                    sql_query = re.sub(r'```sql\s*', '', sql_query)
                    sql_query = re.sub(r'```\s*', '', sql_query)
                    sql_query = sql_query.strip()
                    
                    # Handle multiple statements - take only the first one
                    if ';' in sql_query:
                        sql_query = sql_query.split(';')[0].strip()
                    
                    return sql_query
                except Exception as e:
                    logger.error(f"Error generating SQL: {e}")
                    return "SELECT 1"
            
            def execute_sql(sql_query: str) -> Tuple[bool, list, list, str]:
                """Execute SQL and return (success, results, column_names, error)"""
                try:
                    # Connect to database
                    conn = sqlite3.connect(self.db_path)
                    cursor = conn.cursor()
                    
                    # Execute query
                    cursor.execute(sql_query)
                    
                    # Get column names
                    column_names = [description[0] for description in cursor.description]
                    
                    # Fetch all results
                    rows = cursor.fetchall()
                    
                    # Convert rows to list of dictionaries for easier formatting
                    results = []
                    for row in rows:
                        row_dict = {}
                        for i, col_name in enumerate(column_names):
                            row_dict[col_name] = row[i]
                        results.append(row_dict)
                    
                    # Close connection
                    conn.close()
                    
                    return True, results, column_names, ""
                    
                except Exception as e:
                    error_msg = str(e)
                    logger.error(f"SQL execution error: {error_msg}")
                    return False, None, None, error_msg
            
            try:
                # Generate SQL from natural language query
                sql_query = generate_sql(query)
                
                # Execute the SQL and get results
                success, results, column_names, error = execute_sql(sql_query)
                
                # If execution fails, retry with error context
                if not success:
                    # Retry with error context
                    sql_query = generate_sql(query, error_context=error)
                    success, results, column_names, error = execute_sql(sql_query)
                
                if not success:
                    return f"Database query failed: {error}\nSQL attempted: {sql_query}"
                
                # Format results with column names
                # IMPORTANT: Include "COLUMNS:" prefix for PII detection
                formatted_result = f"SQL Query: {sql_query}\n\n"
                formatted_result += f"COLUMNS: {column_names}\n\n"
                formatted_result += "Database Results:\n"
                
                if not results:
                    formatted_result += "No results found."
                else:
                    # Format each row
                    for i, row in enumerate(results, 1):
                        formatted_result += f"Row {i}:\n"
                        for col_name, value in row.items():
                            formatted_result += f"  {col_name}: {value}\n"
                        formatted_result += "\n"
                
                return formatted_result
                        
            except Exception as e:
                logger.error(f"Database query tool error: {e}")
                return f"Database system error: {e}"
        
        # 2. MARKET DATA TOOL
        def finance_market_search_tool(query: str) -> str:
            """Get real current stock prices and market information
            
            This tool fetches real-time stock data from Yahoo Finance API
            for Apple (AAPL), Tesla (TSLA), and Google (GOOGL).
            
            Args:
                query: Natural language query mentioning companies
                
            Returns:
                String containing current market data
            """
            
            def get_real_stock_data(symbol: str) -> dict:
                """Fetch real stock data from Yahoo Finance API"""
                try:
                    # Make API call to Yahoo Finance
                    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}"
                    headers = {
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                    }
                    
                    response = requests.get(url, headers=headers, timeout=10)
                    response.raise_for_status()
                    
                    data = response.json()
                    
                    # Extract data from Yahoo Finance response
                    if 'chart' in data and 'result' in data['chart'] and len(data['chart']['result']) > 0:
                        result = data['chart']['result'][0]
                        
                        # Get current price
                        if 'meta' in result and 'regularMarketPrice' in result['meta']:
                            current_price = result['meta']['regularMarketPrice']
                        elif 'meta' in result and 'previousClose' in result['meta']:
                            current_price = result['meta']['previousClose']
                        else:
                            return {'success': False, 'error': 'Price data not available'}
                        
                        # Get previous close
                        previous_close = result['meta'].get('previousClose', current_price)
                        
                        # Get volume
                        volume = result['meta'].get('regularMarketVolume', 0)
                        
                        # Get market cap
                        market_cap = result['meta'].get('marketCap', 0)
                        
                        # Calculate price change and change percentage
                        price_change = current_price - previous_close
                        change_percentage = (price_change / previous_close * 100) if previous_close > 0 else 0
                        
                        return {
                            'success': True,
                            'symbol': symbol,
                            'current_price': current_price,
                            'previous_close': previous_close,
                            'price_change': price_change,
                            'change_percentage': change_percentage,
                            'volume': volume,
                            'market_cap': market_cap
                        }
                    else:
                        return {'success': False, 'error': 'Invalid response format'}
                        
                except requests.exceptions.RequestException as e:
                    logger.error(f"Yahoo Finance API error for {symbol}: {e}")
                    return {'success': False, 'error': f'API request failed: {str(e)}'}
                except Exception as e:
                    logger.error(f"Error fetching stock data for {symbol}: {e}")
                    return {'success': False, 'error': f'Unexpected error: {str(e)}'}
            
            try:
                # Identify companies mentioned in the query
                # Map company names/symbols to ticker symbols (AAPL, TSLA, GOOGL)
                query_lower = query.lower()
                symbols_to_fetch = []
                
                # Company name mappings
                company_mappings = {
                    'apple': 'AAPL',
                    'aapl': 'AAPL',
                    'tesla': 'TSLA',
                    'tsla': 'TSLA',
                    'google': 'GOOGL',
                    'googl': 'GOOGL',
                    'alphabet': 'GOOGL'
                }
                
                # Check for each company in the query
                for keyword, symbol in company_mappings.items():
                    if keyword in query_lower:
                        if symbol not in symbols_to_fetch:
                            symbols_to_fetch.append(symbol)
                
                # If no companies found, try to fetch all three
                if not symbols_to_fetch:
                    symbols_to_fetch = ['AAPL', 'TSLA', 'GOOGL']
                
                # Fetch stock data for each identified company
                results = []
                for symbol in symbols_to_fetch:
                    stock_data = get_real_stock_data(symbol)
                    
                    if stock_data['success']:
                        # Format results with price, change, volume
                        result_text = f"{symbol} ({stock_data.get('symbol', symbol)}):\n"
                        result_text += f"  Current Price: ${stock_data['current_price']:.2f}\n"
                        result_text += f"  Previous Close: ${stock_data['previous_close']:.2f}\n"
                        result_text += f"  Change: ${stock_data['price_change']:.2f} ({stock_data['change_percentage']:.2f}%)\n"
                        result_text += f"  Volume: {stock_data['volume']:,}\n"
                        if stock_data.get('market_cap', 0) > 0:
                            result_text += f"  Market Cap: ${stock_data['market_cap']:,.0f}\n"
                        results.append(result_text)
                    else:
                        # Handle API failures with appropriate fallbacks
                        results.append(f"{symbol}: Error - {stock_data.get('error', 'Unknown error')}")
                
                if results:
                    return "\n".join(results)
                else:
                    return "No market data available. Please check your query mentions Apple (AAPL), Tesla (TSLA), or Google (GOOGL), or verify API connectivity."
                    
            except Exception as e:
                logger.error(f"Market data tool error: {e}")
                return f"Market data error: {e}"
        
        # 3. PII PROTECTION TOOL
        def pii_protection_tool(database_results: str, column_names: str) -> str:
            """Automatically mask PII fields in database results
            
            This tool identifies and masks personally identifiable information
            in database query results based on column names and content patterns.
            
            Args:
                database_results: Raw database results as string
                column_names: List of column names (as string)
                
            Returns:
                String with PII fields masked for privacy protection
            """
            
            def detect_pii_fields(field_names: list) -> set:
                """Detect which fields contain PII based on field names"""
                # Create patterns for common PII field names
                pii_patterns = {
                    # Email patterns
                    'email', 'email_address', 'e_mail', 'e-mail', 'email_addr',
                    # Phone patterns
                    'phone', 'phone_number', 'telephone', 'mobile', 'cell', 'contact_number',
                    # Name patterns
                    'first_name', 'last_name', 'full_name', 'customer_name', 'name', 'given_name', 'surname',
                    # Address patterns
                    'address', 'street_address', 'mailing_address', 'home_address', 'physical_address',
                    # SSN patterns
                    'ssn', 'social_security_number', 'tax_id', 'tax_id_number', 'ssn_number'
                }
                
                detected_pii = set()
                
                # Check each field name against patterns (case-insensitive)
                for field_name in field_names:
                    field_lower = str(field_name).lower().strip()
                    
                    # Direct match
                    if field_lower in pii_patterns:
                        detected_pii.add(field_name)
                        continue
                    
                    # Pattern matching - check if any PII pattern is in the field name
                    for pattern in pii_patterns:
                        if pattern in field_lower:
                            detected_pii.add(field_name)
                            break
                
                return detected_pii
            
            def mask_field_value(field_name: str, value: str) -> str:
                """Apply appropriate masking based on field type"""
                if not value:
                    return str(value)
                
                field_lower = str(field_name).lower()
                value_str = str(value)
                
                # Email masking: abc@gmail.com -> ***@gmail.com
                if 'email' in field_lower:
                    if '@' in value_str:
                        parts = value_str.split('@')
                        if len(parts) == 2:
                            return f"***@{parts[1]}"
                    return "***"
                
                # Phone masking: 123-456-7890 -> ***-***-7890
                elif 'phone' in field_lower or 'telephone' in field_lower:
                    # Remove common phone formatting
                    digits = re.sub(r'[^\d]', '', value_str)
                    if len(digits) >= 4:
                        # Keep last 4 digits
                        return f"***-***-{digits[-4:]}"
                    return "***-***-****"
                
                # Name masking: John -> ****
                elif 'name' in field_lower:
                    # Simple masking - replace with asterisks
                    if len(value_str) > 0:
                        return '*' * min(len(value_str), 4)
                    return "****"
                
                # Address masking: Show partial address
                elif 'address' in field_lower:
                    # Keep first few characters, mask the rest
                    if len(value_str) > 5:
                        return value_str[:2] + '*' * (len(value_str) - 2)
                    return "***"
                
                # SSN masking: 123-45-6789 -> ***-**-6789
                elif 'ssn' in field_lower or 'social' in field_lower:
                    digits = re.sub(r'[^\d]', '', value_str)
                    if len(digits) >= 4:
                        return f"***-**-{digits[-4:]}"
                    return "***-**-****"
                
                # Default masking for other PII fields
                else:
                    if len(value_str) > 0:
                        return '*' * min(len(value_str), 4)
                    return "****"
            
            # Parse column names
            try:
                # Column names might be a string representation of a list
                if isinstance(column_names, str):
                    # Try to parse as JSON or Python list
                    try:
                        import ast
                        cols = ast.literal_eval(column_names)
                    except:
                        # Try regex extraction
                        cols = re.findall(r"'([^']+)'", column_names)
                        if not cols:
                            cols = re.findall(r'"([^"]+)"', column_names)
                        if not cols:
                            # Fallback: split by comma
                            cols = [c.strip() for c in column_names.split(',')]
                else:
                    cols = list(column_names)
                
                # Detect PII fields
                pii_fields = detect_pii_fields(cols)
                
                if not pii_fields:
                    # No PII detected, return original
                    return database_results
                
                # Parse database results line by line
                lines = database_results.split('\n')
                protected_lines = []
                masked_fields_notice = []
                
                for line in lines:
                    # Check if this line contains data (not headers or formatting)
                    if ':' in line and any(col in line for col in cols):
                        # Extract field-value pairs
                        for col in cols:
                            if col in line:
                                # Find the value after the colon
                                parts = line.split(':', 1)
                                if len(parts) == 2:
                                    field_name = parts[0].strip()
                                    value = parts[1].strip()
                                    
                                    # Mask if it's a PII field
                                    if field_name in pii_fields:
                                        masked_value = mask_field_value(field_name, value)
                                        line = line.replace(value, masked_value)
                                        if field_name not in masked_fields_notice:
                                            masked_fields_notice.append(field_name)
                    
                    protected_lines.append(line)
                
                # Add notice about which fields were masked
                protected_result = '\n'.join(protected_lines)
                
                if masked_fields_notice:
                    notice = f"\n\n[PII Protection Applied] The following fields have been masked for privacy: {', '.join(masked_fields_notice)}"
                    protected_result += notice
                
                return protected_result
                
            except Exception as e:
                logger.error(f"PII protection error: {e}")
                # On error, return original with a notice
                return f"{database_results}\n\n[PII Protection Error] Could not apply masking: {e}"
        
        # Create FunctionTool objects for each function
        # Wrap each function with FunctionTool.from_defaults()
        # Provide descriptive names and descriptions for agent routing
        # Add all tools to self.function_tools list
        
        # 1. Database Query Tool
        db_tool = FunctionTool.from_defaults(
            fn=database_query_tool,
            name="database_query_tool",
            description=(
                "Query the customer and portfolio database using natural language. "
                "This tool converts natural language queries into SQL and executes them "
                "against the financial database. Use this for questions about customers, "
                "portfolio holdings, company information, and financial metrics. "
                "Returns formatted results with column information."
            )
        )
        self.function_tools.append(db_tool)
        
        # 2. Market Data Tool
        market_tool = FunctionTool.from_defaults(
            fn=finance_market_search_tool,
            name="finance_market_search_tool",
            description=(
                "Get real-time stock market data from Yahoo Finance API. "
                "Use this tool to fetch current stock prices, trading volumes, "
                "price changes, and market capitalization for Apple (AAPL), "
                "Tesla (TSLA), and Google (GOOGL). Query should mention company "
                "names or stock symbols."
            )
        )
        self.function_tools.append(market_tool)
        
        # 3. PII Protection Tool
        pii_tool = FunctionTool.from_defaults(
            fn=pii_protection_tool,
            name="pii_protection_tool",
            description=(
                "Automatically mask personally identifiable information (PII) in database results. "
                "This tool detects sensitive fields like email addresses, phone numbers, "
                "customer names, and applies appropriate masking to protect privacy. "
                "Takes database results and column names as input, returns masked results."
            )
        )
        self.function_tools.append(pii_tool)
        
        if self.verbose:
            print("   ✅ Function tools created")
        
        return self.function_tools
    
    def get_tools(self):
        """Get all function tools
        
        Returns:
            List of FunctionTool objects
        """
        return self.function_tools

