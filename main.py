from ACI import CiscoAPIC
import getpass
import os


def getcredentials():
    """Method to obtain Cerner ASP credential from user

    Returns: [String, String]: username and password"""
    username = input("Please enter your CERNER ASP username: ")
    password = getpass.getpass("Please enter your CERNER ASP password: ")
    return username, password


class Endpoint:
    """Class to work on endpoint"""
    def __int__(self):
        self.ipaddress = None
        self.macaddress = None
        self.tenant = None
        self.epg = None
        self.switch = None
        self.interface = None
        self.appProfile = None

    def getipaddress(self):
        """Method to obtain IP address to be searched from user"""
        self.ipaddress = input("Please enter the IP address to search for: ")

    def searchendpointinaci(self):
        """Method to search user provided IP in all ACI Fabrics across KC/LS RHO"""
        usr, passwd = getcredentials()
        dclist = ["ls2apic3", "ls3apic3", "ls4apic3", "ls5apic3", "ls6apic3", "kc1apic3", "kc2apic3", "kc3apic1", "kc8apic1"]
        for apic in dclist:
            dcapic = CiscoAPIC(apic)
            session_cookie = dcapic.login(usr, passwd)
            epdetails = dcapic.searchendpointip(self.ipaddress, session_cookie)
            if epdetails['totalCount'] == '0':
                print("Could not find endpoint in "+apic+"...\n")
                continue
            else:
                print('Found details of Endpoint as below: ')
                self.macaddress = epdetails['imdata'][0]["fvCEp"]["attributes"]["mac"]
                self.tenant = epdetails['imdata'][0]['fvCEp']['attributes']['dn']
                self.epg = epdetails['imdata'][0]['fvCEp']['attributes']['dn']
                self.appProfile = epdetails['imdata'][0]['fvCEp']['attributes']['dn']
                self.switch = epdetails['imdata'][0]['fvCEp']['children'][0]['fvIp']['children'][0]['fvReportingNode']['attributes']['id']
                print(f'IP: {self.ipaddress}')
                print(f'MAC: {self.macaddress}')
                self.tenant = self.tenant.split('/')[1].split('-')[1]  # original output = "uni/tn-uhbny/ap-rhoAppProfile/epg-159_140_33_128/cep-02:50:56:87:46:FB"
                print(f'Tenant: {self.tenant}')
                self.appProfile = self.appProfile.split('/')[2].split('-')[1]
                print(f'App Profile: {self.appProfile}')
                self.epg = self.epg.split('/')[3].split('-')[1]  # original output = "uni/tn-uhbny/ap-rhoAppProfile/epg-159_140_33_128/cep-02:50:56:87:46:FB"
                print(f'EPG: {self.epg}')
                print(f'Switch: {self.switch}')
                interfacedetails = dcapic.searchendpointinterface(self.macaddress, self.tenant, self.appProfile, self.epg, session_cookie)
                self.interface = interfacedetails['imdata'][0]['fvRsCEpToPathEp']['attributes']['tDn']
                print(f'Interface: {self.interface}')
                break


if __name__ == '__main__':
    os.system('cls')
    print("Welcome to Endpoint Search Tool!")
    ep = Endpoint()
    ep.getipaddress()
    ep.searchendpointinaci()
