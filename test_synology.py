
import os
from dotenv import load_dotenv
from connectors.synology import Client

load_dotenv()
client = Client(username=os.getenv("SYNOLOGY_USERNAME"),
                password=os.getenv("SYNOLOGY_PASSWORD"),
                server_url=os.getenv("SYNOLOGY_SERVER_URL"),
                server_port=os.getenv("SYNOLOGY_SERVER_PORT"))

client.authenticate()
client.logout()