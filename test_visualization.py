#!/usr/bin/env python
"""
Test script for VIVO visualization components.

Usage:
    python test_visualization.py
"""
import logging
import os
import sys
import unittest
from pathlib import Path

# Add project root to Python path
project_root = str(Path(__file__).resolve().parent)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Set up Django environment before importing Django models
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
import django
django.setup()

# Now import the visualization components after Django setup
from vivo_app.lib.visualization import (
    NetworkVisualizer, TimelineVisualizer, OrganizationVisualizer,
    export_network_to_cytoscape, export_timeline_to_vis
)

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class TestVisualization(unittest.TestCase):
    """Test cases for VIVO visualization components."""
    
    def setUp(self):
        """Set up test environment."""
        self.network_viz = NetworkVisualizer()
        self.timeline_viz = TimelineVisualizer()
        self.org_viz = OrganizationVisualizer()
    
    def run_async(self, coro):
        """Helper to run async tests synchronously."""
        import asyncio
        return asyncio.get_event_loop().run_until_complete(coro)
    
    def test_network_visualizer(self):
        """Test network visualization functionality."""
        logger.info("Testing network visualization...")
        
        # Test with a mock person URI
        person_uri = "http://vivo.example.edu/individual/n1234"
        
        # This will use the mock implementation
        network = self.run_async(self.network_viz.coauthorship_network(person_uri))
        
        # Check basic structure
        self.assertIn('nodes', network)
        self.assertIn('links', network)
        self.assertGreaterEqual(len(network['nodes']), 1)
        
        # Convert to Cytoscape format
        cyto_data = export_network_to_cytoscape(network)
        self.assertIn('elements', cyto_data)
        self.assertIn('nodes', cyto_data['elements'])
        self.assertIn('edges', cyto_data['elements'])
        
        logger.info("Network visualization test completed")
    
    def test_timeline_visualizer(self):
        """Test timeline visualization functionality."""
        logger.info("Testing timeline visualization...")
        
        # Test with a mock person URI
        person_uri = "http://vivo.example.edu/individual/n1234"
        
        # This will use the mock implementation
        timeline = self.run_async(self.timeline_viz.publication_timeline(person_uri))
        
        # Check basic structure
        self.assertIn('events', timeline)
        self.assertGreaterEqual(len(timeline['events']), 1)
        
        # Convert to vis.js format
        vis_data = export_timeline_to_vis(timeline)
        self.assertIn('items', vis_data)
        self.assertIn('groups', vis_data)
        
        logger.info("Timeline visualization test completed")
    
    def test_organization_visualizer(self):
        """Test organization visualization functionality."""
        logger.info("Testing organization visualization...")
        
        # Test with a mock organization URI
        org_uri = "http://vivo.example.edu/individual/org123"
        
        # This will use the mock implementation
        org_chart = self.run_async(self.org_viz.organization_chart(org_uri))
        
        # Check basic structure
        self.assertIn('name', org_chart)
        self.assertIn('type', org_chart)
        self.assertIn('children', org_chart)
        
        logger.info("Organization visualization test completed")


if __name__ == "__main__":
    # Run the test suite
    unittest.main(verbosity=2)
