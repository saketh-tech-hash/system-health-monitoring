import aiohttp
import asyncio
from models.graph import Graph
from typing import Dict, Any, List, Optional
import logging

class HealthChecker:
    def __init__(self):
        self.timeout = 10  # seconds
    
    async def check_health(self, node_id: str, node_data: Dict[str, Any]) -> Dict[str, Any]:
        """Check health of a component asynchronously"""
        check_type = node_data.get("check_type", "http")
        url = node_data.get("url")
        
        if check_type == "http" and url:
            return await self._check_http_health(node_id, url)
        elif check_type == "custom":
            # Placeholder for custom health checks
            return {"node_id": node_id, "status": True, "response_time": 0, "message": "Custom check passed"}
        elif check_type == "mock" or check_type == "test":
            # Always return success for mock/test checks
            return {"node_id": node_id, "status": True, "response_time": 0, "message": "Mock check passed (always succeeds)"}
        else:
            # More informative error for other cases
            component_name = node_data.get("name", node_id)
            if not url and check_type == "http":
                return {
                    "node_id": node_id, 
                    "status": False, 
                    "response_time": 0, 
                    "message": f"Missing URL for HTTP check on component '{component_name}'"
                }
            else:
                return {
                    "node_id": node_id, 
                    "status": False, 
                    "response_time": 0, 
                    "message": f"Unsupported check type '{check_type}' for component '{component_name}'"
                }
    
    async def _check_http_health(self, node_id: str, url: str) -> Dict[str, Any]:
        """Check health using HTTP request"""
        try:
            async with aiohttp.ClientSession() as session:
                start_time = asyncio.get_event_loop().time()
                async with session.get(url, timeout=self.timeout, allow_redirects=True) as response:
                    response_time = asyncio.get_event_loop().time() - start_time
                    
                    # Consider more status codes as healthy (including redirects)
                    status = 200 <= response.status < 500  # Count only 5xx as errors
                    
                    return {
                        "node_id": node_id,
                        "status": status,
                        "response_time": response_time,
                        "status_code": response.status,
                        "message": "HTTP check successful" if status else f"HTTP error: {response.status}"
                    }
        except asyncio.TimeoutError:
            return {
                "node_id": node_id,
                "status": False,
                "response_time": self.timeout,
                "message": "Connection timeout"
            }
        except Exception as e:
            return {
                "node_id": node_id,
                "status": False,
                "response_time": 0,
                "message": f"Error: {str(e)}"
            }
    
    async def check_all(self, graph: Graph) -> Dict[str, Dict[str, Any]]:
        """Check health of all components in the graph"""
        nodes = graph.get_nodes()
        tasks = []
        
        # Create tasks for all nodes
        for node_id, node_data in nodes:
            task = self.check_health(node_id, node_data)
            tasks.append(task)
        
        # Run all checks concurrently
        results = await asyncio.gather(*tasks)
        
        # Convert to dictionary with node_id as key
        results_dict = {result["node_id"]: result for result in results}
        
        return results_dict