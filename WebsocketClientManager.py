import ssl
import json
import websocket


class WebsocketClientManager(object):
    def __init__(self, server, api_token, base_url="/ws/", protocol="wss", port=None, connect=True, delay=0):
        """ Object initializer

        Initializer also authenticates using the credentials, and stores the generated
        authentication ticket/token.

        Args:
            server (str): cluster server name (routable DNS address or ip)
            base_url (str): default/constant portion of the url
            api_token (str): API Token for Authentication
            protocol (str): network protocol - wss
            port (str): port number
            connect (bool): Connects if True

        Raises:
            Exception: when unsupported protocol is passed
        """

        self.server = server
        self.total_api_calls = 0

        self.port = str(port) if port and not isinstance(port, str) else port
        if port:
            self.server = self.server + ":" + self.port

        if protocol not in ["wss"]:
            print("Not supported protocol {}.".format(protocol))
            raise Exception("Not supported protocol {}.".format(protocol))

        self.base_url = "{}://{}{}".format(protocol, self.server, base_url)

        self._default_headers = {}
        self.api_token = api_token
        self.delay = delay
        self.ws = None
        self.ws_token = None
        if connect:
            self.connect()

    def connect(self):
        """ Generates a new ticket/token.

        Args:
            force (bool): If true, forces a new connection, else authenticates the existing one
        """

        print("Connecting to the API client.")
        self.authenticate()

    def disconnect(self, connection):
        """ Disconnect from API client"""

        print("Disconnecting from the API client.")
        connection.close()

    def authenticate(self):
        """ Generates a new authentication ticket or token. """

        print("Authenticating websocket connection.")
        self.ws = websocket.WebSocket(sslopt={"cert_reqs": ssl.CERT_NONE})
        protocol_str = "Authorization: Token " + self.api_token
        self.ws.connect(self.base_url, header=[protocol_str])
        noop_response = json.loads(self.receive_message())
        self.ws_token = noop_response['token']

    @property
    def default_headers(self):
        """ Set default headers of client. """
        return self._default_headers

    @default_headers.setter
    def default_headers(self, headers):
        """ Set default headers of client.

        Args:
            headers (dict): headers to set.
        """

        self._default_headers.update(headers)

    def send_message(self, message):
        """ Send message to the server. """
        print("Sending websocket message from API client")
        self.ws.send(message)

    def receive_message(self):
        """ Receives message from the server. """
        print("Receiving websocket message response from server")
        return self.ws.recv()

    def close(self):
        """ Close websocket connection. """
        print("Closing websocket connection")
        self.ws.close()
