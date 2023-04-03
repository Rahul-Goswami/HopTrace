"""This python file contains ACI API methods related to different functionalities.
It is created to be used as it is in different Projects as per your requirement"""

# import necessary modules
import requests
from urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)


# Create class for ACI


class CiscoAPIC:
    # Assign attributes corresponding to APICs
    def __init__(self, dcapic):
        self.apic = dcapic

# Create a method for login to APIC using API
    def login(self, usr, passwd):
        """Method to Login to user provided DC APIC

        Returns : [String] Cookie to be used in subsequent API calls to this DC APIC"""
        login_url = 'https://'+self.apic+'/api/aaaLogin.json'
        login_request_body = {
            "aaaUser": {
                "attributes": {
                    "name": usr,
                    "pwd": passwd
                }
            }
        }
        # Create a POST request to push Login credentials to APIC, use verify=False if APIC does not use SSL
        print("Logging in to "+self.apic)
        try:
            resp = requests.post(url=login_url, json=login_request_body, verify=False)
            resp_output = resp.json()
            # Check if user creds allowed login by TACACS auth of ACI
            if resp_output['imdata'][0] == 'error':
                if resp_output['imdata'][0]['error']['attributes']['code'] == '401':
                    print(resp_output['imdata'][0]['error']['attributes']['text'])
                    raise SystemExit('Exiting due to incorrect Username/Password...')
            else:
                cookie = {'APIC-Cookie': resp_output['imdata'][0]['aaaLogin']['attributes']['token']}
                print("Successfully logged in for "+usr+"...")
                return cookie
        except requests.exceptions.RequestException as error:
            raise SystemExit(error)

    def searchendpointip(self, ipaddress, session_cookie):
        """Method to search of endpoint using IP Address in APIC

        Returns: [Dictionary] Details of Endpoint IP"""
        print("Searching for Endpoint with IP "+ipaddress+" in "+self.apic+"...")
        search_url = 'https://'+self.apic + '/api/node/class/fvCEp.json?rsp-subtree=full&rsp-subtree-include=required&rsp-subtree-filter=eq(fvIp.addr,"'+ipaddress+'")'
        try:
            resp = requests.get(url=search_url, cookies=session_cookie, verify=False)
            resp_output = resp.json()
            resp.close()
            return resp_output
        except requests.exceptions.RequestException as error:
            raise SystemExit(error)

    def searchendpointinterface(self, endpointmac, tenant, epg, session_cookie):
        '''Method to search for endpoint interface using Endpoint MAC, Tenant and EPG in APIC

        Returns: [Dictionary] Learning Interface details'''
        search_url = 'https://' + self.apic + '/api/node/mo/uni/tn-' + tenant + '/ap-rhoAppProfile/epg-' + epg + '/cep-' + endpointmac + '.json?query-target=subtree&target-subtree-class=fvCEp,fvRsCEpToPathEp,fvRsHyper,fvRsToNic,fvRsToVm'
        try:
            resp = requests.get(url=search_url, cookies=session_cookie, verify=False)
            resp_output = resp.json()
            resp.close()
            return resp_output
        except requests.exceptions.RequestException as error:
            raise SystemExit(error)