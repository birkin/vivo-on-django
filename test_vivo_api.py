#!/usr/bin/env python
"""
Test script for VIVO API client.

Usage:
    python test_vivo_api.py
"""
import os
import sys
import logging
import unittest
from pathlib import Path

# Add project root to Python path before importing Django
project_root = str(Path(__file__).resolve().parent)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
import django
django.setup()

# Import VIVO client after Django setup
from vivo_app.lib.vivo_api import VivoApiClient, VivoApiError

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


@unittest.skipUnless(os.getenv('VIVO_API_ONLINE') == '1', 'Skipping VIVO API tests (offline)')
class TestVivoApi(unittest.TestCase):
    """Test cases for VIVO API client."""
    
    def setUp(self):
        """Set up test environment."""
        self.client = VivoApiClient()
    
    def run_async(self, coro):
        """Helper to run async tests synchronously."""
        import asyncio
        return asyncio.get_event_loop().run_until_complete(coro)
    
    def test_connection(self):
        """Test connection to VIVO SPARQL endpoint."""
        logger.info("Testing VIVO API connection...")
        
        # Simple SPARQL query to test connection
        test_query = """
        SELECT ?s ?p ?o
        WHERE {
            ?s ?p ?o .
        }
        LIMIT 5
        """
        
        try:
            result = self.run_async(self.client.query(test_query, use_cache=False))
            self.assertIn('results', result)
            self.assertIn('bindings', result['results'])
            logger.info(f"✅ Connection successful! Found {len(result['results']['bindings'])} results")
            return True
        except Exception as e:
            logger.error(f"❌ Connection failed: {str(e)}")
            logger.error("Please check your VIVO endpoint and credentials in settings.py")
            self.fail(f"Connection test failed: {str(e)}")
    
    def test_invalid_query(self):
        """Test handling of invalid SPARQL queries."""
        invalid_query = "INVALID SPARQL QUERY"
        with self.assertRaises(VivoApiError):
            self.run_async(self.client.query(invalid_query))
    
    def test_cache_behavior(self):
        """Test query caching functionality."""
        test_query = """
        SELECT ?s ?p ?o
        WHERE {
            ?s ?p ?o .
        }
        LIMIT 1
        """
        # First query - should not be cached
        result1 = self.run_async(self.client.query(test_query, use_cache=True))
        # Second query - should be cached
        result2 = self.run_async(self.client.query(test_query, use_cache=True))
        self.assertEqual(result1, result2, "Cached query should return same result")


if __name__ == "__main__":
    # Run the test suite
    unittest.main(verbosity=2)
