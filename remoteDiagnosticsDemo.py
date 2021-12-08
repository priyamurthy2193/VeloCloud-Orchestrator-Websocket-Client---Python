import time
import json
import shlex
from setupWebsocketClient import setup_websocket_client


""" This Demo covers the following Remote Diagnostics test: 
        1. ARP_DUMP
        2. CLEAR_ARP
        3. DNS_TEST
        4. RESTART_DNSMASQ
"""

class RemoteDiagnosticsDemo():

    def __init__(self):
        self.websocket_client = setup_websocket_client()
        self.default_params = dict()
        self.default_params['runDiagnostics'] = {
            "action": "runDiagnostics",
            "data": {
                "logicalId": "sample",
                "test": "test_name",
                "parameters": {},
                "resformat": "JSON",
            },
            "token": "test",
        }

    def get_test_parameters(self, test, param = None, edge_index=0):
        """ Returns test parameters for run diagnostic actions
        Args:
            test(str) : name of run diagnostic action
            edge_index(number): index of edge on which test will be executed
        Returns
            parameters (object): run diagnostic test parameters
        """

        with open('runDiagnosticsDefaultParameters.json') as f:
            testdata = json.load(f)

        print(testdata)
        parameters = testdata[test]

        if test == 'ARP_DUMP':
            parameters['count'] = param
        elif test == 'CLEAR_ARP':
            parameters['interface'] = param
        elif test == 'DNS_TEST':
            parameters['name'] = param

        return parameters

    def get_run_diagnostics_request(self, test, param, edge_logical_id, is_html_test=False):
        """ Returns run diagnostics request object
        Args:
            test(str) : name of run diagnostic action
            is_html_test(boolean): Set to true, if action is HTML test
        Returns
            run_diagnostics_request (object): Returns object with all required request parameters
        """

        parameters = self.get_test_parameters(test, param)
        run_diagnostics_request = self.default_params['runDiagnostics']
        run_diagnostics_request['data']['logicalId'] = edge_logical_id

        if is_html_test:
            run_diagnostics_request['data']['resformat'] = 'HTML'

        if parameters:
            run_diagnostics_request['data']['parameters'] = parameters
        else:
            run_diagnostics_request['data'].pop("parameters", None)

        run_diagnostics_request['data']['test'] = test
        run_diagnostics_request['token'] = self.websocket_client.ws_token

        return run_diagnostics_request

    def execute_run_diagnostics_request(self, run_diagnostics_request):
        """Run run diagnostics test helper

           Args:
            test (str): test name
            run_diagnostics_request (obj): run diagnostics request object

            Returns:
            response: Run Diagnostics response
        """

        # Send runDiagnostics request and receive response
        self.websocket_client.send_message(json.dumps(run_diagnostics_request))

        print("Wait for 30 seconds before receiving response")
        time.sleep(30)

        response = None
        try:
            response = json.loads(self.websocket_client.receive_message())
        except Exception:
            raise ValueError(
                f'Received invalid JSON response for run Diagnostics')

        return response

    def test(self, action_name, param, edge_logical_id):
        """ Test Run Diagnostics ARP_DUMP response from edge """

        print("Testing run diagnostic action " + action_name + " edge")
        run_diagnostics_request = self.get_run_diagnostics_request(
            action_name, param, edge_logical_id)
        
        print(run_diagnostics_request)

        return self.execute_run_diagnostics_request(run_diagnostics_request)



remoteDiagnosticsDemo = RemoteDiagnosticsDemo()

print("This is Remote Diagnostics Sample Websocket Client Demo!")
print('Enter a command[ARP_DUMP, CLEAR_ARP, DNS_TEST, EXIT] to do something, e.g. `ARP_DUMP edgeLogicalId 100`, `CLEAR_ARP edgeLogicalId GE5`, `RESTART_DNSMASQ edgeLogicalId`.')

while True:
    cmd, *args = shlex.split(input('> '))
    cmd = cmd.upper()

    if cmd=='EXIT':
        break

    elif cmd=='ARP_DUMP' or cmd=='CLEAR_ARP' or cmd=='DNS_TEST' or cmd=='RESTART_DNSMASQ':
        param = None
        if len(args) == 1:
            edge_logical_id = args[0]
        else:
            edge_logical_id, param = args
        
        run_diagnostics_response = remoteDiagnosticsDemo.test(cmd, param, edge_logical_id)
        print("Received Response:")
        print(run_diagnostics_response)

    else:
        print('Unknown command: {}'.format(cmd))