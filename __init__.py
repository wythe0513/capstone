import os
import sys
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
from app import create_app

application = create_app()