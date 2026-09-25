"""
VIVO API Client for interacting with the VIVO SPARQL endpoint.
"""

import logging
import httpx
from typing import Any
from django.conf import settings
from django.core.cache import cache

logger = logging.getLogger(__name__)

class VivoApiError(Exception):
    """Base exception for VIVO API errors."""
    pass

class VivoApiClient:
    """Client for interacting with the VIVO SPARQL endpoint."""

    def __init__(self, query_endpoint: str = None, update_endpoint: str = None, auth: tuple = None, timeout: int = None):
        """Initialize the VIVO API client."""
        self.query_endpoint = query_endpoint or getattr(settings, 'VIVO_SPARQL_ENDPOINT')
        self.update_endpoint = update_endpoint or getattr(settings, 'VIVO_UPDATE_ENDPOINT')
        self.auth = auth or (
            getattr(settings, 'VIVO_USERNAME', ''),
            getattr(settings, 'VIVO_PASSWORD', '')
        )
        self.timeout = timeout or getattr(settings, 'VIVO_REQUEST_TIMEOUT', 30)
        self.headers = {
            'Accept': 'application/sparql-results+json, application/json',
            'Content-Type': 'application/sparql-query'
        }

    async def _make_request(self, query: str, is_update: bool = False) -> dict[str, Any]:
        """Execute a SPARQL query against the VIVO endpoint."""
        url = self.update_endpoint if is_update else self.query_endpoint
        headers = self.headers.copy()
        headers['Content-Type'] = 'application/sparql-update' if is_update else 'application/sparql-query'
        
        try:
            async with httpx.AsyncClient(auth=self.auth, timeout=self.timeout) as client:
                response = await client.post(
                    url,
                    content=query,
                    headers=headers
                )
                response.raise_for_status()
                return response.json() if response.content else {}
        except httpx.HTTPStatusError as e:
            logger.error(f"VIVO API request failed with status {e.response.status_code}: {e.response.text}")
            raise VivoApiError(f"HTTP error: {e.response.status_code} - {e.response.text}")
        except httpx.RequestError as e:
            logger.error(f"VIVO API request failed: {str(e)}")
            raise VivoApiError(f"Request failed: {str(e)}")

    async def query(self, sparql: str, use_cache: bool = True) -> dict[str, Any]:
        """Execute a SPARQL SELECT or CONSTRUCT query.
        
        Args:
            sparql: The SPARQL query string to execute
            use_cache: Whether to use cached results if available
            
        Returns:
            Dict containing the query results
        """
        cache_key = f"vivo_query:{hash(sparql)}"
        
        if use_cache:
            cached = cache.get(cache_key)
            if cached is not None:
                return cached
                
        result = await self._make_request(sparql)
        
        if use_cache:
            cache_timeout = getattr(settings, 'VIVO_CACHE_TIMEOUT', 3600)
            cache.set(cache_key, result, timeout=cache_timeout)
            
        return result

    async def update(self, sparql: str) -> bool:
        """Execute a SPARQL UPDATE query.
        
        Args:
            sparql: The SPARQL UPDATE query string to execute
            
        Returns:
            bool: True if the update was successful
            
        Raises:
            VivoApiError: If the update fails
        """
        await self._make_request(sparql, is_update=True)
        return True

# Default client instance
vivo_client = VivoApiClient()
