import os
from WebsocketClientManager import WebsocketClientManager

"""

 A helper module to setup VCO WebSocket Client using Token Based Authentication

 Requires that the following environment variables are specified:
  - VCO_HOST : VCO hostname or IP address (e.g. 'vco.velocloud.net' or '12.34.56.7')
  - VCO_API_TOKEN: Valid API Token issued for a given user

"""

def setup_websocket_client():
    """ Setups WebSocket API Client using environment variables specified

    Returns:
        WebsocketClientManager: instance of WebSocket API Client
    """
    return WebsocketClientManager(server=os.environ['VCO_HOST'],
                                  api_token=os.environ['VCO_API_TOKEN'])
