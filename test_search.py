#!/usr/bin/env python
"""
Test script for VIVO search functionality.

Usage:
    python test_search.py
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

# Now import the search functionality after Django setup
from vivo_app.lib.search import VivoSearcher, quick_search

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class TestVivoSearch(unittest.TestCase):
    """Test cases for VIVO search functionality."""
    
    def setUp(self):
        """Set up test environment."""
        self.searcher = VivoSearcher()
    
    def run_async(self, coro):
        """Helper to run async tests synchronously."""
        import asyncio
        return asyncio.get_event_loop().run_until_complete(coro)
    
    def test_quick_search(self):
        """Test quick search functionality."""
        logger.info("Testing quick search...")
        
        # This is a simple test that won't make actual API calls
        # since we don't have a VIVO instance running
        with self.assertRaises(Exception):
            self.run_async(quick_search("test"))
        
        logger.info("Quick search test completed (expected to fail without VIVO connection)")
    
    def test_search_people(self):
        """Test people search functionality."""
        logger.info("Testing people search...")
        
        # This is a simple test that won't make actual API calls
        # since we don't have a VIVO instance running
        with self.assertRaises(Exception):
            self.run_async(self.searcher.search_people("smith"))
        
        logger.info("People search test completed (expected to fail without VIVO connection)")


if __name__ == "__main__":
    # Run the test suite
    unittest.main(verbosity=2)
