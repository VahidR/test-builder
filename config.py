"""
Copyright (C) 2014  Vahid Rafiei (@vahid_r)

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import os
import loadimpact

# The basedir folder .. relative paths will be calculated based on this value
basedir = root_dir = os.path.abspath(os.path.dirname(__file__))

# OBS. if you prefer you can put the API Token here. However, it's not a good practice for the production environments 
# api_token='HARD-CODED-API-TOKEN'

api_token = os.getenv("LOADIMPACT_API_TOKEN", None)
client = loadimpact.ApiTokenClient(api_token=api_token)