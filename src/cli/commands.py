"""
Command-line interface for the Databricks MCP server.

This module provides command-line functionality for interacting with the Databricks MCP server.
"""

import argparse
import asyncio
import logging
import sys
from typing import List, Optional

from src.server.databricks_mcp_server import DatabricksMCPServer, main as server_main

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def parse_args(args: Optional[List[str]] = None) -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Databricks MCP Server CLI")
    
    # Create subparsers for different commands
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # Start server command
    start_parser = subparsers.add_parser("start", help="Start the MCP server")
    start_parser.add_argument(
        "--debug", action="store_true", help="Enable debug logging"
    )
    
    # List tools command
    list_parser = subparsers.add_parser("list-tools", help="List available tools")
    
    # Version command
    subparsers.add_parser("version", help="Show server version")
    
    return parser.parse_args(args)


async def list_tools() -> None:
    """List all available tools in the server."""
    print("\nAvailable tools:")
    
    # Create a server instance to introspect the tools
    try:
        server = DatabricksMCPServer()
        
        # Get the tools from the server instance using introspection
        # FastMCP stores tools in the _tools attribute
        if hasattr(server, '_tools'):
            tools = server._tools
            for tool_name, tool_info in tools.items():
                description = getattr(tool_info, 'description', 'No description available')
                print(f"  - {tool_name}: {description}")
        else:
            # Fallback to known tools if introspection fails
            known_tools = [
                ("list_clusters", "List all Databricks clusters"),
                ("create_cluster", "Create a new Databricks cluster"),
                ("terminate_cluster", "Terminate a specific Databricks cluster"),
                ("get_cluster", "Get detailed information about a specific Databricks cluster"),
                ("start_cluster", "Start a stopped Databricks cluster"),
                ("list_jobs", "List all Databricks jobs"),
                ("create_job", "Create a new Databricks job"),
                ("run_job", "Run a Databricks job"),
                ("list_notebooks", "List notebooks in a workspace directory"),
                ("export_notebook", "Export a notebook from the workspace"),
                ("list_files", "List files and directories in DBFS"),
                ("execute_sql", "Execute a SQL statement in Databricks SQL warehouse"),
            ]
            for tool_name, description in known_tools:
                print(f"  - {tool_name}: {description}")
                
    except Exception as e:
        print(f"Error getting tools: {e}")
        print("Showing known tools as fallback:")
        known_tools = [
            ("list_clusters", "List all Databricks clusters"),
            ("create_cluster", "Create a new Databricks cluster"),
            ("terminate_cluster", "Terminate a specific Databricks cluster"),
            ("get_cluster", "Get detailed information about a specific Databricks cluster"),
            ("start_cluster", "Start a stopped Databricks cluster"),
            ("list_jobs", "List all Databricks jobs"),
            ("create_job", "Create a new Databricks job"),
            ("run_job", "Run a Databricks job"),
            ("list_notebooks", "List notebooks in a workspace directory"),
            ("export_notebook", "Export a notebook from the workspace"),
            ("list_files", "List files and directories in DBFS"),
            ("execute_sql", "Execute a SQL statement in Databricks SQL warehouse"),
        ]
        for tool_name, description in known_tools:
            print(f"  - {tool_name}: {description}")


def show_version() -> None:
    """Show the server version."""
    try:
        # Try to get version from package configuration
        import pkg_resources
        version = pkg_resources.get_distribution("databricks-mcp-server").version
        print(f"\nDatabricks MCP Server v{version}")
    except Exception:
        # Fallback to hardcoded version
        print("\nDatabricks MCP Server v1.0.0")
        print("Note: Version is from fallback, not package configuration")


def main(args: Optional[List[str]] = None) -> int:
    """Main entry point for the CLI."""
    parsed_args = parse_args(args)
    
    # Set log level
    if hasattr(parsed_args, "debug") and parsed_args.debug:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Execute the appropriate command
    if parsed_args.command == "start":
        logger.info("Starting Databricks MCP server")
        asyncio.run(server_main())
    elif parsed_args.command == "list-tools":
        asyncio.run(list_tools())
    elif parsed_args.command == "version":
        show_version()
    else:
        # If no command is provided, show help
        parse_args(["--help"])
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main()) 