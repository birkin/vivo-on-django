"""
Search functionality for VIVO data.

This module provides classes and functions for searching VIVO data using SPARQL queries.
It includes support for different types of searches (people, organizations, publications, etc.)
and handles pagination, filtering, and result formatting.
"""

import logging
from dataclasses import asdict, dataclass
from typing import Any

from .vivo_api import VivoApiClient

logger = logging.getLogger(__name__)

# Default VIVO API client
vivo_client = VivoApiClient()


@dataclass
class SearchResult:
    """Represents a single search result item."""

    uri: str
    label: str
    type: str
    description: str | None = None
    thumbnail: str | None = None
    score: float | None = None

    def to_dict(self) -> dict[str, Any]:
        """Convert the search result to a dictionary."""
        return asdict(self)


class VivoSearcher:
    """Handles searching VIVO data using SPARQL queries."""

    def __init__(self, client: VivoApiClient | None = None):
        """Initialize the searcher with an optional VIVO API client."""
        self.client = client or vivo_client
        self.default_limit = 20

    async def search_people(
        self, query: str, limit: int = 20, offset: int = 0, **filters
    ) -> dict[str, Any]:
        """
        Search for people in VIVO.

        Args:
            query: The search query string
            limit: Maximum number of results to return
            offset: Offset for pagination
            **filters: Additional filters (e.g., organization, expertise)

        Returns:
            Dictionary containing search results and metadata
        """
        # Build the SPARQL query
        sparql = """
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX foaf: <http://xmlns.com/foaf/0.1/>
        PREFIX vivo: <http://vivoweb.org/ontology/core#>
        
        SELECT DISTINCT ?person ?name ?title ?email ?thumbnail
        WHERE {
            ?person a foaf:Person .
            ?person rdfs:label ?name .
            
            # Basic text search on name
            FILTER(REGEX(STR(?name), "%s", "i"))
            
            # Optional fields
            OPTIONAL { ?person vivo:preferredTitle ?title . }
            OPTIONAL { ?person vivo:primaryEmail ?email . }
            OPTIONAL { ?person vivo:thumbnailImage ?thumbnail . }
            
            # Apply additional filters if provided
            %s
        }
        ORDER BY ?name
        LIMIT %d OFFSET %d
        """ % (query, self._build_filters(filters), limit, offset)

        # Execute the query
        results = await self.client.query(sparql)

        # Process and return results
        return self._format_search_results(results, "person")

    async def search_organizations(
        self, query: str, limit: int = 20, offset: int = 0, **filters
    ) -> dict[str, Any]:
        """
        Search for organizations in VIVO.

        Args:
            query: The search query string
            limit: Maximum number of results to return
            offset: Offset for pagination
            **filters: Additional filters

        Returns:
            Dictionary containing search results and metadata
        """
        # Similar implementation to search_people but for organizations
        # ...
        pass

    def _build_filters(self, filters: dict[str, Any]) -> str:
        """Build SPARQL FILTER clauses from a dictionary of filters."""
        filter_clauses = []

        for key, value in filters.items():
            if key == "organization":
                filter_clauses.append(f"""
                    ?person vivo:personInPosition ?position .
                    ?position vivo:positionInOrganization <{value}> .
                """)
            elif key == "expertise":
                filter_clauses.append(f"""
                    ?person vivo:hasResearchArea <{value}> .
                """)
            # Add more filter types as needed

        return "\n".join(filter_clauses)

    def _format_search_results(
        self, sparql_results: dict[str, Any], result_type: str
    ) -> dict[str, Any]:
        """Format SPARQL query results into a standard format."""
        formatted = {
            "count": len(sparql_results.get("results", {}).get("bindings", [])),
            "results": [],
            "facets": {},
        }

        for result in sparql_results.get("results", {}).get("bindings", []):
            item = {
                "uri": result.get(f"?{result_type}", {}).get("value", ""),
                "label": result.get("?name", {}).get("value", ""),
                "type": result_type,
                "description": result.get("?title", {}).get("value", ""),
                "thumbnail": result.get("?thumbnail", {}).get("value"),
            }
            formatted["results"].append(item)

        return formatted


# Helper functions for common search tasks


async def quick_search(query: str, limit: int = 10) -> dict[str, Any]:
    """
    Perform a quick search across all entity types.

    Args:
        query: The search query string
        limit: Maximum number of results to return per entity type

    Returns:
        Dictionary containing search results grouped by entity type
    """
    searcher = VivoSearcher()

    # Search for people
    people = await searcher.search_people(query, limit=limit)

    # Search for organizations
    organizations = await searcher.search_organizations(query, limit=limit)

    return {"people": people, "organizations": organizations, "query": query}
