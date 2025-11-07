"""
Agent Coordinator Module - Complete Financial Agent with Modular Architecture

This module provides the complete financial agent functionality with intelligent routing,
tool coordination, and backward compatibility. It replaces both modern_financial_agent.py
and financial_agent.py by providing all functionality in a single coordinated system.

Learning Objectives:
- Understand multi-tool coordination and intelligent routing
- Implement LLM-based decision making for tool selection
- Learn result synthesis from multiple data sources
- Build modular agent architecture
- Master PII protection in agent workflows

Your Task: Complete the missing implementations marked with YOUR CODE HERE

Key Features:
- Multi-tool coordination with intelligent routing
- Document analysis (10-K filings) for Apple, Google, Tesla
- Database queries with SQL auto-generation and PII protection
- Real-time market data from Yahoo Finance
- Complete backward compatibility for existing notebooks
- Modular architecture using helper modules
"""

import os
import logging
from typing import Dict, List, Any, Tuple, Optional
from pathlib import Path

# LlamaIndex imports
from llama_index.core import Settings
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding

# Environment setup
from dotenv import load_dotenv
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.WARNING, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)


class AgentCoordinator:
    """
    Complete Financial Agent with Dynamic Multi-Tool Coordination
    
    This class combines the functionality of the original modern_financial_agent.py
    and financial_agent.py into a single coordinated system using modular architecture.
    
    Architecture:
    - Document Tools (3): Individual SEC 10-K filing analysis for Apple, Google, Tesla
    - Function Tools (3): Database SQL queries, real-time market data, PII protection
    - Intelligent Routing: LLM-based tool selection and result synthesis
    - Backward Compatibility: Works with existing notebooks and code
    """
    
    def __init__(self, companies: List[str] = None, verbose: bool = False):
        """
        Initialize the complete financial agent with modular architecture.
        
        Args:
            companies: List of company symbols (default: ["AAPL", "GOOGL", "TSLA"])
            verbose: Whether to show detailed operation information
        """
        self.companies = companies if companies is not None else ["AAPL", "GOOGL", "TSLA"]
        self.verbose = verbose
        self.project_root = Path.cwd()  # Use current working directory
        
        # Company metadata
        self.company_info = {
            "AAPL": {"name": "Apple Inc.", "sector": "Technology"},
            "GOOGL": {"name": "Alphabet Inc.", "sector": "Technology"},
            "TSLA": {"name": "Tesla Inc.", "sector": "Automotive"}
        }
        
        # Storage for tools and engines
        self.document_tools = []
        self.function_tools = []
        self.llm = None
    
        
        self._configure_settings()
        
        # Don't auto-initialize tools - create them lazily when first needed
        self._tools_initialized = False
        
        if self.verbose:
            print("✅ Financial Agent Coordinator Initialized")
            print(f"   Companies: {self.companies}")
            print(f"   Tools will be created automatically when first query is made")
    
  
    def _configure_settings(self):
        """Configure LlamaIndex settings with Vocareum API compatibility
        
        Requirements:
        - Create OpenAI LLM with "gpt-3.5-turbo" model and temperature=0
        - Create OpenAIEmbedding with "text-embedding-ada-002" model
        - Use api_base parameter for Vocareum API compatibility (both models)
        - Set Settings.llm and Settings.embed_model
        - Store LLM reference in self.llm for routing decisions
        
        IMPORTANT NOTE FOR VOCAREUM:
        LlamaIndex requires the api_base parameter to work with Vocareum's OpenAI endpoint.
        Get the base URL from environment: os.getenv("OPENAI_API_BASE", "https://openai.vocareum.com/v1")
        Pass it as api_base parameter to both OpenAI() and OpenAIEmbedding() constructors.
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
    
    
    def setup(self, document_tools: List = None, function_tools: List = None):
        """
        Setup all components using the modular architecture.
        
        Args:
            document_tools: Optional pre-created document tools
            function_tools: Optional pre-created function tools
            
        This method initializes all tools and sets up the routing system.
        If tools are not provided, they will be created automatically.
        """
        if self.verbose:
            print("🔧 Setting up Advanced Financial Agent (Modular Architecture)...")
        
        try:
            if document_tools is not None and function_tools is not None:
                # Use provided tools
                self.document_tools = document_tools
                self.function_tools = function_tools
            else:
                # Create tools automatically
                self._create_tools()
            
            if self.verbose:
                status = self.get_status()
                print(f"✅ Setup complete: {status['document_tools']} document tools, {status['function_tools']} function tools")
                print(f"🎯 System ready: {'✅' if status['ready'] else '❌'}")
                
        except Exception as e:
            logger.error(f"Setup failed: {e}")
            if self.verbose:
                print(f"❌ Setup failed: {e}")
    
    def _create_tools(self):
        """Create all tools automatically using helper modules
        
        Steps:
        1. Import DocumentToolsManager from .document_tools
        2. Import FunctionToolsManager from .function_tools
        3. Create instances and call their build methods
        4. Store results in self.document_tools and self.function_tools
        """
        # Import helper modules
        from helper_modules.document_tools import DocumentToolsManager
        from helper_modules.function_tools import FunctionToolsManager
        
        # Create DocumentToolsManager and build document tools
        doc_manager = DocumentToolsManager(companies=self.companies, verbose=self.verbose)
        self.document_tools = doc_manager.build_document_tools()
        
        # Create FunctionToolsManager and build function tools
        func_manager = FunctionToolsManager(verbose=self.verbose)
        self.function_tools = func_manager.create_function_tools()
        
        if self.verbose:
            print(f"   Created {len(self.document_tools)} document tools")
            print(f"   Created {len(self.function_tools)} function tools")
    
    def _check_and_apply_pii_protection(self, tool_name: str, result: str) -> str:
        """Check if database results need PII protection and apply it automatically
        
        This method automatically detects when database queries return sensitive information
        and applies appropriate PII protection using the PII protection tool from function_tools.
        
        Args:
            tool_name: Name of the tool that generated the result
            result: Raw result string from the tool
            
        Returns:
            Protected result string with PII masked if necessary
        """
        
        # Only apply to database query results
        if "database_query_tool" not in tool_name:
            return result
        
        # Check if result contains column information
        if "COLUMNS:" not in result:
            return result
        
        # Extract column names from result
        import re
        import ast
        
        # Find COLUMNS line
        columns_match = re.search(r'COLUMNS:\s*(.+)', result)
        if not columns_match:
            return result
        
        columns_str = columns_match.group(1).strip()
        
        # Parse column names
        try:
            cols = ast.literal_eval(columns_str)
        except:
            # Fallback: regex extraction
            cols = re.findall(r"'([^']+)'", columns_str)
            if not cols:
                cols = re.findall(r'"([^"]+)"', columns_str)
        
        if not cols:
            return result
        
        # Detect PII fields using _detect_pii_fields()
        pii_fields = self._detect_pii_fields(cols)
        
        # If PII detected, find and use the pii_protection_tool
        if pii_fields:
            # Find PII protection tool
            pii_tool = None
            for tool in self.function_tools:
                if hasattr(tool, 'metadata') and 'pii' in tool.metadata.name.lower():
                    pii_tool = tool
                    break
            
            if pii_tool:
                # Apply protection
                try:
                    protected_result = pii_tool.call(database_results=result, column_names=str(cols))
                    return protected_result
                except Exception as e:
                    logger.error(f"PII protection error: {e}")
                    return result
        
        return result
    
    def _detect_pii_fields(self, field_names: list) -> set:
        """Detect which fields contain PII based on field names
        
        This method identifies potentially sensitive database fields that need protection.
        
        Args:
            field_names: List of database column names
            
        Returns:
            Set of field names that contain PII
        """
        # Define PII field patterns (email, phone, names, address, ssn, etc.)
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
    
    def _route_query(self, query: str) -> List[Tuple[str, str, Any]]:
        """Use LLM to intelligently route query to appropriate tools
        
        This method analyzes the user's query and determines which tools are needed
        to provide a complete answer, then executes those tools and returns results.
        
        Args:
            query: User's natural language query
            
        Returns:
            List of tuples: (tool_name, tool_description, result)
        """
        # Create descriptions of all available tools
        all_tools = []
        tool_descriptions = []
        
        # Add document tools
        for i, tool in enumerate(self.document_tools):
            tool_name = tool.metadata.name
            tool_desc = tool.metadata.description
            all_tools.append((tool_name, tool_desc, tool, 'document'))
            tool_descriptions.append(f"{i}. {tool_name}: {tool_desc}")
        
        # Add function tools
        offset = len(self.document_tools)
        for i, tool in enumerate(self.function_tools):
            tool_name = tool.metadata.name
            tool_desc = tool.metadata.description
            all_tools.append((tool_name, tool_desc, tool, 'function'))
            tool_descriptions.append(f"{offset + i}. {tool_name}: {tool_desc}")
        
        # Build LLM prompt with query and tool options
        prompt = f"""You are a financial agent coordinator. Analyze the user query and select the appropriate tools to answer it.

User Query: {query}

Available Tools:
{chr(10).join(tool_descriptions)}

Routing Guidelines:
- Questions about customers, portfolios, holdings → use database_query_tool
- Questions about current stock prices, market data → use finance_market_search_tool
- Questions about company business, strategy, financials from SEC filings → use document tools (AAPL_10k_filing_tool, GOOGL_10k_filing_tool, TSLA_10k_filing_tool)
- Complex queries may require multiple tools

Select the tool(s) needed to answer this query. Return ONLY a comma-separated list of tool indices (0-based), nothing else.
For example: "0,3" or "1,2,4" or "5"

Selected tools:"""
        
        try:
            # Use LLM to select tools
            response = self.llm.complete(prompt)
            selected_indices_str = str(response.text).strip()
            
            # Parse LLM response to get tool indices
            import re
            # Extract numbers from response
            indices = [int(x) for x in re.findall(r'\d+', selected_indices_str)]
            
            # Filter valid indices
            valid_indices = [idx for idx in indices if 0 <= idx < len(all_tools)]
            
            # If no valid indices, use simple heuristics as fallback
            if not valid_indices:
                query_lower = query.lower()
                for idx, (tool_name, tool_desc, tool, tool_type) in enumerate(all_tools):
                    # Simple keyword matching
                    if 'database' in tool_name.lower() and any(kw in query_lower for kw in ['customer', 'portfolio', 'holding', 'database']):
                        valid_indices.append(idx)
                    elif 'market' in tool_name.lower() and any(kw in query_lower for kw in ['price', 'stock', 'market', 'current']):
                        valid_indices.append(idx)
                    elif '10k' in tool_name.lower() or 'filing' in tool_name.lower():
                        if any(kw in query_lower for kw in ['apple', 'aapl', 'google', 'googl', 'tesla', 'tsla', 'company', 'business', 'strategy', 'revenue']):
                            # Check if query mentions specific company
                            if 'aapl' in tool_name.lower() and ('apple' in query_lower or 'aapl' in query_lower):
                                valid_indices.append(idx)
                            elif 'googl' in tool_name.lower() and ('google' in query_lower or 'googl' in query_lower or 'alphabet' in query_lower):
                                valid_indices.append(idx)
                            elif 'tsla' in tool_name.lower() and ('tesla' in query_lower or 'tsla' in query_lower):
                                valid_indices.append(idx)
            
            # Remove duplicates and sort
            valid_indices = sorted(list(set(valid_indices)))
            
            # Execute selected tools and collect results
            results = []
            for idx in valid_indices:
                if idx < len(all_tools):
                    tool_name, tool_desc, tool, tool_type = all_tools[idx]
                    
                    try:
                        # Execute tool based on type
                        if tool_type == 'document':
                            # Document tool - use query_engine
                            result = tool.query_engine.query(query)
                            result_str = str(result)
                        else:
                            # Function tool - use call method
                            if 'database' in tool_name.lower():
                                result_str = tool.call(query)
                            elif 'market' in tool_name.lower():
                                result_str = tool.call(query)
                            elif 'pii' in tool_name.lower():
                                # PII tool shouldn't be called directly here
                                continue
                            else:
                                result_str = tool.call(query)
                        
                        # Apply PII protection to database results
                        result_str = self._check_and_apply_pii_protection(tool_name, result_str)
                        
                        results.append((tool_name, tool_desc, result_str))
                        
                    except Exception as e:
                        logger.error(f"Error executing tool {tool_name}: {e}")
                        results.append((tool_name, tool_desc, f"Error: {e}"))
            
            return results
            
        except Exception as e:
            logger.error(f"Routing error: {e}")
            return []
    
    def query(self, question: str, verbose: bool = None) -> str:
        """Process query with dynamic tool routing and result synthesis
        
        This is the main entry point for the financial agent. It handles:
        1. Tool routing and selection using LLM
        2. Multi-tool execution 
        3. Result synthesis for comprehensive answers
        4. Automatic PII protection
        
        Args:
            question: User's financial question
            verbose: Whether to show detailed processing info
            
        Returns:
            Comprehensive answer synthesized from relevant tools
        """
        
        # Use instance verbose if parameter not provided
        if verbose is None:
            verbose = self.verbose
        
        # Ensure tools are initialized
        if not self._tools_initialized:
            self.setup()
            self._tools_initialized = True
        
        if verbose:
            print(f"🎯 Query: {question}")
        
        # Route query to appropriate tools using _route_query()
        tool_results = self._route_query(question)
        
        if not tool_results:
            return "Unable to process query. No appropriate tools found or error occurred."
        
        # Display tool selection info if verbose
        if verbose:
            print(f"   Selected {len(tool_results)} tool(s):")
            for tool_name, tool_desc, _ in tool_results:
                print(f"      - {tool_name}")
        
        # If single tool result, return it directly
        if len(tool_results) == 1:
            _, _, result = tool_results[0]
            return str(result)
        
        # If multiple tool results, synthesize using LLM
        # Build synthesis prompt
        synthesis_prompt = f"""You are a financial analyst assistant. Synthesize the following information from multiple sources into a comprehensive, coherent answer.

Original Query: {question}

Information from Tools:
"""
        
        for i, (tool_name, tool_desc, result) in enumerate(tool_results, 1):
            synthesis_prompt += f"\n{i}. {tool_name} ({tool_desc}):\n{result}\n"
        
        synthesis_prompt += "\n\nProvide a comprehensive answer that integrates all the information above. Be clear, concise, and ensure all relevant details are included."
        
        try:
            # Use LLM to synthesize results
            synthesis_response = self.llm.complete(synthesis_prompt)
            synthesized_answer = str(synthesis_response.text).strip()
            
            return synthesized_answer
            
        except Exception as e:
            logger.error(f"Synthesis error: {e}")
            # Fallback: return concatenated results
            fallback_answer = f"Query: {question}\n\n"
            for tool_name, _, result in tool_results:
                fallback_answer += f"From {tool_name}:\n{result}\n\n"
            return fallback_answer
    
    def get_available_tools(self) -> Dict[str, Any]:
        """
        Get information about available tools with full compatibility.
        
        Returns:
            Dictionary with comprehensive tool information
        """
        return {
            "document_tools": ["apple", "google", "tesla"] if len(self.document_tools) >= 3 else [],
            "function_tools": ["sql", "market", "pii"] if len(self.function_tools) >= 3 else [],
            "total_tools": len(self.document_tools) + len(self.function_tools),
            "document_tool_count": len(self.document_tools),
            "function_tool_count": len(self.function_tools)
        }
    
    def get_status(self) -> Dict[str, Any]:
        """
        Get comprehensive agent status with full compatibility.
        
        Returns:
            Dictionary with detailed status information
        """
        tool_count = len(self.document_tools) + len(self.function_tools)
        system_ready = len(self.document_tools) >= 3 and len(self.function_tools) >= 3
        
        return {
            "companies": self.companies,
            "document_tools": len(self.document_tools),
            "function_tools": len(self.function_tools),
            "total_tools": tool_count,
            "ready": system_ready,
            "architecture": "modular",
            "coordinator_ready": system_ready,
            "available_companies": ['AAPL', 'GOOGL', 'TSLA'],
            "capabilities": [
                "Document analysis (10-K filings)",
                "Database queries (customer portfolios)",
                "Real-time market data",
                "PII protection",
                "Multi-tool coordination",
                "Intelligent routing"
            ],
            "system_ready": system_ready
        }

    def list_available_tools(self) -> List[str]:
        """
        List all available tools by name.

        Returns:
            List of tool names
        """
        if not self._tools_initialized:
            self._create_tools()

        tool_names = []

        # Add document tool names
        for tool in self.document_tools:
            if hasattr(tool, 'metadata') and hasattr(tool.metadata, 'name'):
                tool_names.append(tool.metadata.name)
            elif hasattr(tool, '_name'):
                tool_names.append(tool._name)

        # Add function tool names
        for tool in self.function_tools:
            if hasattr(tool, 'metadata') and hasattr(tool.metadata, 'name'):
                tool_names.append(tool.metadata.name)
            elif hasattr(tool, '_name'):
                tool_names.append(tool._name)

        return tool_names

    def _intelligent_routing(self, query: str) -> List[Tuple[str, str, Any]]:
        """
        Alias for _route_query for backward compatibility.

        Args:
            query: Natural language query

        Returns:
            List of tuples: (tool_name, tool_description, result)
        """
        return self._route_query(query)
