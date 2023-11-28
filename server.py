# This script implements a FastAPI server that provides an API endpoint 
# for retrieving information about packages from a repository, 
# based on user-provided query parameters.

import json
import os
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional

# Usage example:
# Return the complete list of packages for a given branch and architecture
# curl -X GET "http://127.0.0.1:8000/packages/?architecture=amd64&branch=main"

# Return only the information of a specific package
# curl -X GET "http://127.0.0.1:8000/packages/?package_name=0ad&architecture=amd64&branch=main"


# Use of Pydantic for validation of query parameters
class PackageQueryParams(BaseModel):
    package_name: Optional[str] = None
    architecture: str
    branch: str

app = FastAPI()

def get_query_params(query_params: PackageQueryParams = Depends()):
    return query_params

# Main endpoint
@app.get("/packages/")
async def get_packages(query_params: PackageQueryParams = Depends(get_query_params)):
    try:
        # Access validated input using query_params.package_name, query_params.architecture, query_params.branch

        # Build the path to the Packages.json file
        file_path = os.path.join("output", query_params.branch, f"binary-{query_params.architecture}", "Packages.json")

        # Read the contents of the Packages.json file.
        with open(file_path, "r") as file:
            packages_data = json.load(file)

        if query_params.package_name:
            # If a package name is specified, it searches only for that package
            package = next((pkg for pkg in packages_data if pkg["Package"] == query_params.package_name), None)
            if package:
                return [package]
            else:
                raise HTTPException(status_code=404, detail="Package not found")
        else:
            # If no package name is specified, return the full list of packages
            return packages_data

    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Repository not found")
