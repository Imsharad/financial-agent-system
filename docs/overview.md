Introduction
Welcome to the FinTool Analyst project! In this hands-on project, you'll build a sophisticated multi-tool agentic system that serves as an intelligent financial analyst assistant. This system combines the power of document analysis, database querying, and real-time market data to provide comprehensive financial insights.

Financial institutions deal with multiple data sources daily: regulatory filings, internal customer databases, and live market feeds. Your agentic system will intelligently coordinate between these sources, automatically selecting the right tools and synthesizing information to answer complex financial queries.

This project represents a real-world application of agentic AI in financial services, where systems must be modular, maintainable, and capable of handling sensitive customer information with appropriate privacy protections.

The Challenge
Financial analysts need to answer questions that require information from multiple sources simultaneously. For example, "How does Tesla's business strategy from their 10-K filing align with our customers' investment positions and current market performance?" requires document analysis, database queries, and real-time market data—all synthesized into a coherent answer.

Your challenge is to build a modular multi-tool agentic system that can intelligently route queries to appropriate tools (document search, database queries, market data APIs), automatically detect when sensitive customer information needs protection, and synthesize results from multiple sources into comprehensive answers. The system must handle diverse query types ranging from simple single-source questions to complex multi-tool coordination scenarios, all while maintaining clean modular architecture and automatic privacy protection.

Your Product
By the end of this project, you will have created a Modular Financial Agent System with the following capabilities:

Core Components:

DocumentToolsManager: Analyzes SEC 10-K filings for Apple, Google, and Tesla using vector search and RAG
FunctionToolsManager: Provides database querying with automatic SQL generation, real-time market data from Yahoo Finance, and automatic PII protection
AgentCoordinator: Intelligently routes queries to appropriate tools using LLM-based decision making and synthesizes multi-source results
Key Features:

Intelligent Routing: Automatically selects the right tools based on query content using LLM analysis
Multi-Tool Coordination: Seamlessly combines information from documents, databases, and market APIs
Automatic PII Protection: Detects and masks sensitive customer information without manual intervention
Modular Architecture: Clean separation of concerns with independently testable components
Comprehensive Coverage: Handles 6 specialized tools working together through intelligent coordination
The system you build will demonstrate enterprise-grade agentic AI architecture suitable for production financial services applications.

Deliverables
Submit the following components for project evaluation:

Helper Modules Implementation (helper_modules/ directory):

document_tools.py - Complete DocumentToolsManager with vector indexing and query tools
function_tools.py - Complete FunctionToolsManager with database, market, and PII tools
agent_coordinator.py - Complete AgentCoordinator with routing and synthesis logic
Code includes clear comments explaining key implementation decisions
Working Notebook (financial_agent_walkthrough.ipynb):

Successfully executes from start to finish without errors
Demonstrates all query types: document analysis, database queries, market data, and multi-tool coordination
Shows automatic PII protection in action
Note: All placeholder code (e.g., # YOUR CODE HERE, pass statements) must be replaced with working implementations. The grading rubric in GRADING_RUBRIC.md provides detailed evaluation criteria.