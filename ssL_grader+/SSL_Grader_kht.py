# NAME: tkokhing
# STUDENT ID: 1**6*92
# # This program took refernce from https://github.com/narbehaj/ssl-checker
# And sslabs, https://github.com/ssllabs/ssllabs-scan/blob/master/ssllabs-api-docs-v3.md 
# # heavily modification as stated in the report.

#!/usr/bin/env python3
import socket
import sys
import json
import time as tm

from argparse import ArgumentParser, SUPPRESS
from datetime import datetime
from ssl import PROTOCOL_TLSv1   
from time import sleep
from csv import DictWriter


try:
    from OpenSSL import SSL, crypto
    from json2html import *
except ImportError:
    print('Please install required modules: pip install -r requirements.txt')
    sys.exit(1)


class Clr:
    """Text colors."""

    RST = '\033[39m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'


class SSLChecker:

    # for summing the overall run
    total_failed = 0
    total_valid = 0
    total_warning = 0
    total_expired = 0


    def __init__ (self):

        self.myFileName = 'Write_SSL_output.txt'
        self.saveFile = open(self.myFileName, 'w')
        self.saveFile.write('-----------Recording for SSL Grader-----------\n')   

    def WriteToFile(self,myMessage,fileMode):
        i = 0
        self.saveFile = open(self.myFileName, fileMode)
        self.saveFile.write(myMessage + '\n')   
        
    def CloseFile(self):
        self.saveFile.close()

    def testBit(self, int_type, offset):
        mask = 1 << offset
        return(int_type & mask)
        
    def get_cert(self, host, port, user_args):

        cert_context = {}
        """Connection to the host."""
        if user_args.socks:
            import socks
            if user_args.verbose:
                print('{}Socks proxy enabled{}\n'.format(Clr.YELLOW, Clr.RST))

            socks_host, socks_port = self.filter_hostname(user_args.socks)
            socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, socks_host, int(socks_port), True)
            socket.socket = socks.socksocket

        if user_args.verbose:
            print('{}Connecting to socket{}\n'.format(Clr.YELLOW, Clr.RST))
            self.WriteToFile('Connecting to socket','a')


        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # sock = socket.socket()

        osobj = SSL.Context(PROTOCOL_TLSv1)         
        sock.connect((host, int(port)))
        oscon = SSL.Connection(osobj, sock)
        oscon.set_tlsext_host_name(host.encode())
        oscon.set_connect_state()
        oscon.do_handshake()

        # print('Connection state AFTER handshake', oscon.get_state_string().decode())

        # Retrieve the SSL or TLS protocol version of the current connection.
        cert_context['proto_ver_n'] = oscon.get_protocol_version_name()
        print('Protocol Version Name --- >', oscon.get_protocol_version_name())        
        
        cert_context['proto_ver'] = oscon.get_protocol_version()
        print('Protocol Version  --- >', oscon.get_protocol_version())

        # Obtain the name of the currently used cipher.
        cert_context['cipher_n'] = oscon.get_cipher_name()
        print('Name of the currently used cipher  --- >', oscon.get_cipher_name())
        

        # cert_context['cipher_list'] = oscon.get_cipher_list() # # # this is wrong
        # Retrieve the list of ciphers used by the Connection object, Returns A list of native cipher strings.
        # print('List of ciphers used by the Connection object --- >', oscon.get_cipher_list())
        
        # Obtain the number of secret bits of the currently used cipher.
        # Returns The number of secret bits of the currently used cipher or 
        # None if no connection has been established.
        # Return type intor NoneType
        cert_context['cipher_sec_bits'] = oscon.get_cipher_bits()
        print('Number of secret bits of the currently used cipher  --- >', oscon.get_cipher_bits())
        
        # Obtain the protocol version of the currently used cipher, 
        # Returns The protocol name of the currently used cipher or 
        # None if no connection has been established.
        cert_context['cipher_ver'] = oscon.get_cipher_version()
        print('Protocol version of the currently used cipher  --- >', oscon.get_cipher_version())
        
        oscrypto = crypto.PKey()
        # print('\t\toscrypto ---> ', oscrypto)
        # print('\t\toscrypto.bits ---> ', oscrypto.bits)
        # print('\t\toscrypto.bits() ---> ', oscrypto.bits())

        cert_bits = oscrypto.bits()
        cert_context['cert_bits'] = cert_bits
        print('Cert Public Key bit ---> ', cert_bits)


        # # # no clue how to do this
        # print('OCSP Request --->', oscon.request_ocsp())

        cert = oscon.get_peer_certificate()

        cert_Pkey = cert.get_pubkey()
        print('Cert Public Key ---> ', cert_Pkey)
        cert_context['cert_Pkey'] = cert_Pkey

        sock.close()

        # print('Connection state AFTER sock closed', oscon.get_state_string().decode())

        if user_args.verbose:
            print('{}Closing socket{}\n'.format(Clr.YELLOW, Clr.RST))

        return cert, cert_context

    def border_msg(self, message):
        """Print the message in the box."""
        row = len(message)
        h = ''.join(['+'] + ['-' * row] + ['+'])
        result = h + '\n' "|" + message + "|"'\n' + h
        print(result)

    def analyze_ssl(self, host, context, user_args):
        """Analyze the security of the SSL certificate."""
        try:
            from urllib.request import urlopen
        except ImportError:
            from urllib.request  import urlopen

        api_url = 'https://api.ssllabs.com/api/v3/'
        while True:
            if user_args.verbose:
                print('{}Requesting analyze to {}{}\n'.format(Clr.YELLOW, api_url, Clr.RST))

            main_request = json.loads(urlopen(api_url + 'analyze?host={}'.format(host)).read().decode('utf-8'))
            if main_request['status'] in ('DNS', 'IN_PROGRESS'):
                if user_args.verbose:
                    print('{}Analyze waiting for reports to be finished (1 secs){}\n'.format(Clr.YELLOW, Clr.RST))

                sleep(5)
                continue
            elif main_request['status'] == 'READY':
                if user_args.verbose:
                    print('{}Analyze is ready{}\n'.format(Clr.YELLOW, Clr.RST))

                break

        endpoint_data = json.loads(urlopen(api_url + 'getEndpointData?host={}&s={}'.format(
            host, main_request['endpoints'][0]['ipAddress'])).read().decode('utf-8'))

        if user_args.verbose:
            print('{}Analyze report message: {}{}\n'.format(Clr.YELLOW, endpoint_data['statusMessage'], Clr.RST))

        # if the certificate is invalid
        if endpoint_data['statusMessage'] == 'Certificate not valid for domain name':
            return context

        try:
            context[host]['grade'] = main_request['endpoints'][0]['grade']
        except:
            context[host]['grade'] = "NO DATA"
            
        try:
            context[host]['poodle_vuln'] = endpoint_data['details']['poodle']
        except:
            context[host]['poodle_vuln'] = "NO DATA"
            
        try:     
            context[host]['heartbleed_vuln'] = endpoint_data['details']['heartbleed']
        except:
            context[host]['heartbleed_vuln'] = "NO DATA"
                    
        try: 
            context[host]['heartbeat_vuln'] = endpoint_data['details']['heartbeat']
        except:
            context[host]['heartbeat_vuln'] = "NO DATA"

        try:
            context[host]['freak_vuln'] = endpoint_data['details']['freak']
        except:
            context[host]['freak_vuln'] = "NO DATA"

        try: 
            context[host]['logjam_vuln'] = endpoint_data['details']['logjam']
        except:
            context[host]['logjam_vuln'] = "NO DATA"

        try: 
            context[host]['drownVulnerable'] = endpoint_data['details']['drownVulnerable']
        except:
            context[host]['drownVulnerable'] = "NO DATA"

        try:
            context[host]['renego'] = "N" 
            renegvar = int(endpoint_data['details']['renegSupport'])
            renegp = self.testBit(renegvar, 0)
            if renegp != 0:
                context[host]['renego'] = "Y"

        except:
            context[host]['renego'] = "NO DATA" 

		#sgrade
        try:
            context[host]['sgrade'] = endpoint_data['gradeTrustIgnored']
        except:
            context[host]['sgrade'] = "NO DATA"

        try:
            context[host]['OCSP_Status'] = endpoint_data['details']['ocspStapling']
        except:
            context[host]['OCSP_Status'] = "NO DATA"

        # OpenSSL CCS Injection Vulnerability (CVE-2014-0224) Alert 
        try:
            # Refer to SSL lab doc
            # 1  
            # -1 - test failed
            # 0 - unknown
            # 1 - not vulnerable
            # 2 - possibly vulnerable, but not exploitable
            # 3 - vulnerable and exploitable
            context[host]['SSL-CCS'] = endpoint_data['details']['openSslCcs']

        except:
            context[host]['SSL-CCS'] = "NO DATA"
            pass # test failed -1 will take care of this


        #insecure dh
        try:
            insecureProtocolList = []
            protocolList = []
            kxStrengthList = []
            # not all sites have this but created as placeholder for easy comparison
            context[host]['cipher_list'] = []
            context[host]['cipher_Cnt'] = 0
            context[host]['inSec_DH_list'] = []
            context[host]['inSec_DH']= 0
            context[host]['keyStrength'] = 0

            # suites may have more than a Dict
            for s in range(len(endpoint_data['details']['suites'])):
                # list may have more than a List
                for suite in endpoint_data['details']['suites'][s]['list']:
                    # print('each suite name is  ---> ', suite['name'])

                    # capture the no duplicate list of secure protocol
                    if suite['name'] not in protocolList:
                        protocolList.append(suite['name'])
                    
                    # not all fields inside suite will be key() kxStgrength
                    try:
                        kxStrengthList.append(suite['kxStrength']) 
                        # print('kxStrength is  ---> ', suite['kxStrength'])
                    except Exception as e:
                        pass
                    # print('kxStrength is  ---> ', type(suite['kxStrength']))
                    # print('Looping -------->',s)
                    # input()

                    try:
                        if "DHE" in suite['name']:
                            try:
                                if suite['q']==0: # 0 if the protocol is insecure, null otherwise
                                    if suite['name'] not in insecureProtocolList:
                                        insecureProtocolList.append(suite['name'])
                                    # print("This is possible insec DH " + suite['name'])
                                # elif suite['q']==1: # 1 if the protocol is secure
                                #     print("This is Secure DH " + suite['name'])
                                # else:
                                #     print('q is not 0 or 1 haha')
                            except Exception as e:
                                # enter here when there is no field q
                                pass
                                
                    except Exception as e:
                        pass

            # return protocol list and count
            if len(protocolList) != 0:
                context[host]['cipher_list'].extend(protocolList)
                context[host]['cipher_Cnt'] = len(protocolList)

            # return insecure protocol list and count
            if len(insecureProtocolList) != 0:
                context[host]['inSec_DH_list'].extend(insecureProtocolList)
                context[host]['inSec_DH'] = len(insecureProtocolList)
            
            # return key Strength of protocols, it should be the same for all protocol 
            # but i cannot be 100% sure
            if len(kxStrengthList) != 0:
                context[host]['keyStrength'] = max(kxStrengthList)

        except Exception as e:
            pass
        
        # SSL_versions
        try:
            # not all sites have this but created as placeholder for easy comparison
            context[host]['SSL_1']=[]
            context[host]['SSL_2']=[]
            context[host]['SSL_3']=[]
            context[host]['v2SuitesDisabled']=[]
            ssl1, ssl2, ssl3 = "N", "N", "N"      
            v2SuitesDisabled= "Y"
            for protocol in endpoint_data['details']['protocols']:
                if "SSL" in protocol['name'] and protocol['version']=="1.0":
                    ssl1 = "Y"

                if "SSL" in protocol['name'] and protocol['version']=="2.0":
                    ssl2 = "Y"
                    if protocol['v2SuitesDisabled']== True:
                        v2SuitesDisabled = "Y"
                    else:
                        v2SuitesDisabled = "N"
            
                if "SSL" in protocol['name'] and protocol['version']=="3.0":
                    ssl3 = "Y"
            
            context[host]['SSL_1']=ssl1
            context[host]['SSL_2']=ssl2         
            context[host]['SSL_3']=ssl3
            context[host]['v2SuitesDisabled']=v2SuitesDisabled


        except Exception as e:
            pass

        # TLS_versions 
        try:
            # not all sites have this but created as placeholder for easy comparison
            context[host]['TLS_1-0']=[]
            tls10= "N"
            context[host]['TLS_1-1']=[]
            tls11= "N"
            context[host]['TLS_1-2']=[]
            tls12= "Y"
            context[host]['TLS_1-3']=[]
            tls13= "Y"

            for protocol in endpoint_data['details']['protocols']:
                if "TLS" in protocol['name'] and protocol['version']=="1.0":
                    tls10 = "Y"
                if "TLS" in protocol['name'] and protocol['version']=="1.1":
                    tls11 = "Y"
                if "TLS" in protocol['name'] and protocol['version']=="1.2":
                    tls12 = "Y"
                if "TLS" in protocol['name'] and protocol['version']=="1.3":
                    tls13 = "Y"

            context[host]['TLS_1-0']=tls10
            context[host]['TLS_1-1']=tls11
            context[host]['TLS_1-2']=tls12
            context[host]['TLS_1-3']=tls13            

        except Exception as e:
            pass

        return context

    def get_cert_sans(self, x509cert):
        """
        Get Subject Alt Names from Certificate. Shameless taken from stack overflow:
        https://stackoverflow.com/users/4547691/anatolii-chmykhalo
        """

        # print('\t\t\t\tCert Cryptography', x509cert.to_cryptography())
        # # # Cert Cryptography <Certificate(subject=<Name(C=SG,L=Singapore,O=Oversea-Chinese Banking Corporation Limited,CN=www.ocbc.com)>, ...)>

        san = ''
        ext_count = x509cert.get_extension_count()
        for i in range(0, ext_count):
            ext = x509cert.get_extension(i)
            if 'subjectAltName' in str(ext.get_short_name()):
                san = ext.__str__()
        # replace commas to not break csv output
        san = san.replace(',', ';')
        return san

    def get_cert_info(self, host, cert):
        """Get all the information about cert and create a JSON file."""
        context = {}
        # print('cert --->',cert)
        # # # # cert ---> <OpenSSL.crypto.X509 object at 0x000001A4C5F0E6D0>
        # # # # cert is not a Dict or Tuple or List of List
        # print('Class cert --->',type(cert))
        # # # # Class cert ---> <class 'OpenSSL.crypto.X509'>

        cert_subject = cert.get_subject()
        # print('cert_subject --->', cert_subject) 
        # # # # cert_subject ---> <X509Name object '/C=US/ST=California/L=Los Gatos/O=Netflix, Inc./CN=www.netflix.com'>

        # # # keeps getting 
        cert_Pkey = cert.get_pubkey()
        print('Cert Public Key ---> ', cert_Pkey)

        context['host'] = host
        context['issued_to'] = cert_subject.CN
        context['issued_o'] = cert_subject.O
        
        context['issuer_c'] = cert.get_issuer().countryName
        context['issuer_o'] = cert.get_issuer().organizationName
        
        context['issuer_ou'] = cert.get_issuer().organizationalUnitName
        context['issuer_cn'] = cert.get_issuer().commonName

        context['cert_sn'] = str(cert.get_serial_number())
        context['cert_sha1'] = cert.digest('sha1').decode()
        context['cert_sha256'] = cert.digest('sha256').decode()
        context['cert_alg'] = cert.get_signature_algorithm().decode()
        context['cert_ver'] = cert.get_version()
        context['cert_sans'] = self.get_cert_sans(cert)
        context['cert_exp'] = cert.has_expired()
        # context['cert_valid'] = False if cert.has_expired() else True
        context['cert_valid'] = 0 if cert.has_expired() else 1

        # # #  Valid from 
        valid_from = datetime.strptime(cert.get_notBefore().decode('ascii'),
                                       '%Y%m%d%H%M%SZ')
        context['valid_from'] = valid_from.strftime('%Y-%m-%d')

        # # #  Valid till
        valid_till = datetime.strptime(cert.get_notAfter().decode('ascii'),
                                       '%Y%m%d%H%M%SZ')
        context['valid_till'] = valid_till.strftime('%Y-%m-%d')

        # # #  Validity days (total number of days the cert will be valid)
        context['validity_days'] = (valid_till - valid_from).days

        # # #  Valid days left 
        context['valid_days_to_expire'] = (datetime.strptime(context['valid_till'],
                                           '%Y-%m-%d') - datetime.now()).days

        if cert.has_expired():
            self.total_expired += 1
        else:
            self.total_valid += 1

        # If the certificate has less than 30 days validity
        if context['valid_days_to_expire'] <= 30:
            self.total_warning += 1

        # print('get_cert_info() == Class type of <context> ',type(context))
        # # # # get_cert_info() == Class type of <context>  <class 'dict'>
        # # # # <context> is declared as a  <class 'dict'> to fill up the site details gathereds

        # print('get_cert_info() == These are inside <context>  --->', context)
        # # # # get_cert_info() == These are inside <context>  ---> 
        # # # # {'host': 'www.dbs.com', 'issued_to': 'www.dbs.com', 
        # # # # 'issued_o': 'DBS Bank Ltd', 'issuer_c': 'US', 
        # # # # 'issuer_o': 'Entrust, Inc.', 'issuer_ou': 'See www.entrust.net/legal-terms',
        # # # #  'issuer_cn': 'Entrust Certification Authority - L1M',
        # # # #  'cert_sn': '138536995130289955891549547836603450318',
        # # # #  'cert_sha1': '62:69:8B:70:63:4A:81:BB:C4:0E:13:99:D7:6F:E0:18:53:7F:7F:F5',
        # # # #  'cert_alg': 'sha256WithRSAEncryption', 'cert_ver': 2,
        # # # #  'cert_sans': 'DNS:www.dbs.com; DNS:cug.www.dbs.com',
        # # # #  'cert_exp': False, 'cert_valid': True, 'valid_from': '2021-09-08',
        # # # #  'valid_till': '2022-10-07', 'validity_days': 394,
        # # # #  'days_left': 47, 'valid_days_to_expire': 47}
        # # # .
        # # .
        # #  

        return context

    def show_result(self, user_args):
        """Get the context."""

        print('\n')
        host_counter = 1
        context = {}
        all_context ={}
        start_time = datetime.now()
        hosts = user_args.hosts

        if not user_args.json_true and not user_args.summary_true:
            self.border_msg(' Analyzing {} host(s) '.format(len(hosts)))
            self.WriteToFile(' Analyzing ' +  str(len(hosts)) + ' host(s)','a')


        if not user_args.json_true and user_args.analyze:
            print('{}Warning: -a/--analyze is enabled. It takes more time...{}\n'.format(Clr.YELLOW, Clr.RST))
            self.WriteToFile(' Warning: -a/--analyze is enabled. It takes more time...' ,'a')

        for host in hosts:
            if user_args.verbose:
                print('\n{} ({}) Working on host: {}{}\n'.format(Clr.YELLOW, host_counter, host, Clr.RST))
                self.WriteToFile('\n(' + str(host_counter) +')' + ' Working on host: ' +  host,'a')

            host_counter += 1

            host, port = self.filter_hostname(host)

            # Check duplication
            if host in context.keys():
                continue

            try:
                cert, cert_context = self.get_cert(host, port, user_args)
                context[host] = self.get_cert_info(host, cert)
                context[host]['tcp_port'] = int(port)


                # Analyze the certificate if enabled
                if user_args.analyze:
                    context = self.analyze_ssl(host, context, user_args)

                if not user_args.json_true and not user_args.summary_true:
                    self.print_status(host, context, user_args.analyze)

                all_context[host] = {**context[host], **cert_context}
                
            except SSL.SysCallError:
                if not user_args.json_true:
                    print('\t{}[-]{} {:<20s} Failed: Misconfigured SSL/TLS\n'.format(Clr.RED, Clr.RST, host))
                    self.WriteToFile(' [-] ' +  (host) + ' Failed: Misconfigured SSL/TLS','a')
                    self.total_failed += 1
            except Exception as error:
                if not user_args.json_true:
                    print('\t{}[-]{} {:<20s} Failed: {}\n'.format(Clr.RED, Clr.RST, host, error))
                    self.WriteToFile('\t[-] ' +  host + ' Failed: ' + str(error),'a')
                    self.total_failed += 1

            except KeyboardInterrupt:
                print('{}Canceling script...{}\n'.format(Clr.YELLOW, Clr.RST))
                self.WriteToFile('Canceling script... ','a')
                sys.exit(1)

        if not user_args.json_true:
            self.border_msg(' Successful: {} | Failed: {} | Valid: {} | Warning: {} | Expired: {} | Duration: {} '.format(
                len(hosts) - self.total_failed, self.total_failed, self.total_valid,
                self.total_warning, self.total_expired, datetime.now() - start_time))
            
            self.WriteToFile('\nSuccessful: ' + str(len(hosts) - self.total_failed) + ' | Failed: ' + str(self.total_failed) + ' | Valid: ' + str(self.total_valid) + ' | Warning ' + str(self.total_warning) + ' | Expired: ' + str(self.total_expired) + ' | Duration: ' + str(datetime.now() - start_time),'a')  

            if user_args.summary_true:
                # Exit the script just
                return

        # CSV export if -c/--csv is specified
        if user_args.csv_enabled:
            self.export_csv(all_context, user_args.csv_enabled, user_args)

        # HTML export if -x/--html is specified
        if user_args.html_true:
            self.export_html(all_context)

        # While using the script as a module
        if __name__ != '__main__':
            return json.dumps(all_context)

        # Enable JSON output if -j/--json argument specified
        if user_args.json_true:
            print(json.dumps(all_context))

        if user_args.json_save_true:
            for host in all_context.keys():
                with open(host + '.json', 'w', encoding='UTF-8') as fp:
                    fp.write(json.dumps(all_context[host]))

        self.CloseFile()

    def print_status(self, host, context, analyze=False):
        """Print all the usefull info about host."""
        print('\t{}[+]{} {}\n\t{}'.format(Clr.GREEN, Clr.RST, host, '-' * (len(host) + 5)))
        print('\t\tIssued domain: {}'.format(context[host]['issued_to']))
        print('\t\tIssued to: {}'.format(context[host]['issued_o']))
        print('\t\tIssued by: {} ({})'.format(context[host]['issuer_o'], context[host]['issuer_c']))
        print('\t\tValid from: {}'.format(context[host]['valid_from']))
        print('\t\tValid to: {} ({} days left)'.format(context[host]['valid_till'], context[host]['valid_days_to_expire']))
        print('\t\tValidity days: {}'.format(context[host]['validity_days']))
        print('\t\tCertificate valid: {}'.format(context[host]['cert_valid']))
        print('\t\tCertificate S/N: {}'.format(context[host]['cert_sn']))
        print('\t\tCertificate SHA1 FP: {}'.format(context[host]['cert_sha1']))
        print('\t\tCertificate SHA256 FP: {}'.format(context[host]['cert_sha256']))
        print('\t\tCertificate version: {}'.format(context[host]['cert_ver']))
        print('\t\tCertificate algorithm: {}'.format(context[host]['cert_alg']))


        self.WriteToFile('\t[+] ' +  host + '\n\t' + '-' * (len(host) + 5),'a')
        self.WriteToFile('\t\tIssued domain              : ' + str(context[host]['issued_to']),'a')
        self.WriteToFile('\t\tIssued to                  : ' + str(context[host]['issued_o']),'a')
        self.WriteToFile('\t\tIssued by                  : ' + str(context[host]['issuer_o']) + '(' + str(context[host]['issuer_c']) + ')','a')
        self.WriteToFile('\t\tValid from                 : ' + str(context[host]['valid_from']),'a')
        self.WriteToFile('\t\tValid to                   : ' + str(context[host]['valid_till']) + ' (' + str(context[host]['valid_days_to_expire']) + ' days left)','a') 
        self.WriteToFile('\t\tValidity days              : ' + str(context[host]['validity_days']),'a')
        self.WriteToFile('\t\tCertificate valid          : ' + str(context[host]['cert_valid']),'a')
        self.WriteToFile('\t\tCertificate S/N            : ' + str(context[host]['cert_sn']),'a')
        self.WriteToFile('\t\tCertificate SHA1 FP        : ' + str(context[host]['cert_sha1']),'a')
        self.WriteToFile('\t\tCertificate SHA256 FP      : ' + str(context[host]['cert_sha256']),'a')
        self.WriteToFile('\t\tCertificate version        : ' + str(context[host]['cert_ver']),'a')
        self.WriteToFile('\t\tCertificate algorithm      : ' + str(context[host]['cert_alg']),'a')

        if analyze:
            print('\t\tKey Strength: {}'.format(context[host]['keyStrength'] ))
            print('\t\tCertificate grade: {}'.format(context[host]['grade']))
            print('\t\tCiphers Supported by Server: {}'.format(context[host]['cipher_list']))
            print('\t\tPoodle vulnerability: {}'.format(context[host]['poodle_vuln']))
            print('\t\tHeartbleed vulnerability: {}'.format(context[host]['heartbleed_vuln']))
            print('\t\tHeartbeat vulnerability: {}'.format(context[host]['heartbeat_vuln']))
            print('\t\tFREAK vulnerability: {}'.format(context[host]['freak_vuln']))
            print('\t\tLogjam vulnerability: {}'.format(context[host]['logjam_vuln']))
            print('\t\tDROWN vulnerability: {}'.format(context[host]['drownVulnerable']))
 
            self.WriteToFile('\t\tKey Strength               : ' + str(context[host]['keyStrength']),'a')
            self.WriteToFile('\t\tCertificate grade          : ' + str(context[host]['grade']),'a')
            self.WriteToFile('\t\tCiphers Supported by Server: ' + (', '.join(context[host]['cipher_list'])),'a')
            self.WriteToFile('\t\tPoodle vulnerability       : ' + str(context[host]['poodle_vuln']),'a')
            self.WriteToFile('\t\tHeartbleed vulnerability   : ' + str(context[host]['heartbleed_vuln']),'a')
            self.WriteToFile('\t\tHeartbeat vulnerability    : ' + str(context[host]['heartbeat_vuln']),'a')
            self.WriteToFile('\t\tFREAK vulnerability        : ' + str(context[host]['freak_vuln']),'a')
            self.WriteToFile('\t\tLogjam vulnerability       : ' + str(context[host]['logjam_vuln']),'a')
            self.WriteToFile('\t\tDROWN vulnerability        : ' + str(context[host]['drownVulnerable']),'a')

        print('\t\tExpired: {}'.format(context[host]['cert_exp']))
        print('\t\tCertificate SAN\'s: ')

        self.WriteToFile('\t\tExpired:  ' + str(context[host]['cert_exp']),'a')
        self.WriteToFile('\t\tCertificate SAN\'s:   ','a')

        for san in context[host]['cert_sans'].split(';'):
            print('\t\t \\_ {}'.format(san.strip()))
            self.WriteToFile('\t\t \\_   ' + str(san.strip()),'a')


        print('\n')


    def export_csv(self, context, filename, user_args):
        """Export all context results to CSV file."""
        # prepend dict keys to write column headers
        if user_args.verbose:
            print('{}Generating CSV export{}\n'.format(Clr.YELLOW, Clr.RST))

        with open(filename, 'w') as csv_file:
            csv_writer = DictWriter(csv_file, list(context.items())[0][1].keys())
            csv_writer.writeheader()
            for host in context.keys():
                csv_writer.writerow(context[host])

    def export_html(self, context):
        """Export JSON to HTML."""
        html = json2html.convert(json=context)
        file_name = datetime.strftime(datetime.now(), '%Y_%m_%d_%H_%M_%S')
        with open('{}.html'.format(file_name), 'w') as html_file:
            html_file.write(html)

        return

    def filter_hostname(self, host):
        """Remove unused characters and split by address and port."""
        host = host.replace('http://', '').replace('https://', '').replace('/', '')
        port = 443
        if ':' in host:
            host, port = host.split(':')

        print('HOST ----- >',host,'PORT ----- >', port)
        return host, port

    def get_args(self, json_args={}):
        """Set argparse options."""
        parser = ArgumentParser(prog='ssl_checker.py', add_help=False,
                                description="""Collects useful information about given host's SSL certificates.""")

        if len(json_args) > 0:
            args = parser.parse_args()
            setattr(args, 'json_true', True)
            setattr(args, 'verbose', False)
            setattr(args, 'csv_enabled', False)
            setattr(args, 'html_true', False)
            setattr(args, 'json_save_true', False)
            setattr(args, 'socks', False)
            setattr(args, 'analyze', False)
            setattr(args, 'hosts', json_args['hosts'])
            return args

        group = parser.add_mutually_exclusive_group(required=True)
        group.add_argument('-H', '--host', dest='hosts', nargs='*',
                           required=False, help='Hosts as input separated by space')
        group.add_argument('-f', '--host-file', dest='host_file',
                           required=False, help='Hosts as input from file')
        parser.add_argument('-s', '--socks', dest='socks',
                            default=False, metavar='HOST:PORT',
                            help='Enable SOCKS proxy for connection')
        parser.add_argument('-c', '--csv', dest='csv_enabled',
                            default=False, metavar='FILENAME.CSV',
                            help='Enable CSV file export')
        parser.add_argument('-j', '--json', dest='json_true',
                            action='store_true', default=False,
                            help='Enable JSON in the output')
        parser.add_argument('-S', '--summary', dest='summary_true',
                            action='store_true', default=False,
                            help='Enable summary output only')
        parser.add_argument('-x', '--html', dest='html_true',
                            action='store_true', default=False,
                            help='Enable HTML file export')
        parser.add_argument('-J', '--json-save', dest='json_save_true',
                            action='store_true', default=False,
                            help='Enable JSON export individually per host')
        parser.add_argument('-a', '--analyze', dest='analyze',
                            default=False, action='store_true',
                            help='Enable SSL security analysis on the host')
        parser.add_argument('-v', '--verbose', dest='verbose',
                            default=False, action='store_true',
                            help='Enable verbose to see what is going on')
        parser.add_argument('-h', '--help', default=SUPPRESS,
                            action='help',
                            help='Show this help message and exit')

        args = parser.parse_args()

        # Get hosts from file if provided
        if args.host_file:
            with open(args.host_file) as f:
                args.hosts = f.read().splitlines()

        # Checks hosts list
        if isinstance(args.hosts, list):
            if len(args.hosts) == 0:
                parser.print_help()
                sys.exit(0)
        return args


if __name__ == '__main__':

    SSLCheckerObject = SSLChecker()
    SSLCheckerObject.show_result(SSLCheckerObject.get_args(json_args={}))
