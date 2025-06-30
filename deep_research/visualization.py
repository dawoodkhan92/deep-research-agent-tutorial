"""Agency Visualization - Based on Agency Swarm Examples"""

from pathlib import Path

def create_agency_visualization(agency, output_dir="outputs"):
    """
    Create interactive HTML visualization of the agency structure.
    
    Args:
        agency: The Agency instance to visualize
        output_dir: Directory to save the visualization file
        
    Returns:
        str: Path to the generated HTML file
    """
    Path(output_dir).mkdir(exist_ok=True)
    
    return agency.create_interactive_visualization(
        output_file=f"{output_dir}/agency_structure.html"
    )