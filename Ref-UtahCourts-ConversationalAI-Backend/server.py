"""
Server startup module.
Loads env variables before running servers.
"""

from dotenv import load_dotenv
from rasa.__main__ import main

# Load environment variables.
load_dotenv()

if __name__ == '__main__':
    main()
