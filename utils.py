"""
utils.py
Helper functions for formatting output and error handling.
"""

def format_resources(resources):
    """Format resources for display."""
    if not resources:
        return "No resources available."
    
    lines = []
    for r in resources:
        lines.append(f"- {r}")
    return "\n".join(lines)

def format_capabilities(capabilities):
    """Format server capabilities for display."""
    if not capabilities:
        return "No capabilities reported."
    
    lines = []
    for k, v in capabilities.items():
        lines.append(f"{k}: {v}")
    return "\n".join(lines)

def handle_error(e):
    """Print error details to user."""
    print(f"\nError: {e}\n")
    # Optionally, log or format more details here
