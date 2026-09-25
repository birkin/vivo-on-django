#!/usr/bin/env python
"""
Script to check connection to VIVO API endpoints.
"""
import os
import sys
import asyncio
import httpx
from pathlib import Path

# Add project root to Python path
project_root = str(Path(__file__).resolve().parent)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
import django
django.setup()

from django.conf import settings

async def check_endpoint(url: str, method: str = 'GET', **kwargs) -> bool:
    """Check if an endpoint is accessible."""
    try:
        async with httpx.AsyncClient() as client:
            if method.upper() == 'GET':
                response = await client.get(url, **kwargs)
            elif method.upper() == 'POST':
                response = await client.post(url, **kwargs)
            else:
                print(f"Unsupported HTTP method: {method}")
                return False
            
            print(f"{method} {url} - Status: {response.status_code}")
            return response.status_code < 400
    except Exception as e:
        print(f"Error connecting to {url}: {str(e)}")
        return False

async def main():
    """Check VIVO endpoints."""
    endpoints = {
        'SPARQL Query': settings.VIVO_SPARQL_ENDPOINT,
        'SPARQL Update': settings.VIVO_UPDATE_ENDPOINT,
    }
    
    print("Checking VIVO endpoints:")
    print(f"- SPARQL Query: {settings.VIVO_SPARQL_ENDPOINT}")
    print(f"- SPARQL Update: {settings.VIVO_UPDATE_ENDPOINT}")
    print(f"- Username: {settings.VIVO_USERNAME}")
    print("\nTesting connections...")
    
    # Test each endpoint
    for name, url in endpoints.items():
        method = 'POST' if 'Update' in name else 'GET'
        success = await check_endpoint(
            url,
            method=method,
            auth=(settings.VIVO_USERNAME, settings.VIVO_PASSWORD) if settings.VIVO_USERNAME and settings.VIVO_PASSWORD else None,
            timeout=5.0
        )
        print(f"{name} endpoint: {'✅' if success else '❌'}")

if __name__ == "__main__":
    asyncio.run(main())
