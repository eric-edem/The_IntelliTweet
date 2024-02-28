import ssl
from urllib.parse import urlparse
from urllib.request import urlopen
import whois
import datetime
from tldextract import extract
# import dnspython as dns
import pandas as pd
import dns.resolver
import bs4
from bs4 import BeautifulSoup
import regex
import socket
import requests
import time



def url_is_internal(url, compare):
    # url is the param needed to be compared to compare
    if ".".join(extract(url)) == ".".join(extract(compare)) or (url[0:4] != "http" and url[0] != "#"):
        return True
    else:
        return False


class CheckUrlFeature():

    def check_connection(url):
        try:
            r = requests.get(url, timeout=7)
            print("Url connected")
            return 0

        except:
            ("Url not connected")
            return 0

    def having_IP_Address(url):
        try:
            symbol = regex.findall(r'\b(?:\d{1,3}\.){3}\d{1,3}\b', url)
            if (len(symbol) != 0):
                having_ip = 1
                print("Ip present")
            else:
                having_ip = -1
                print("no ip")
            return (having_ip)
        except Exception as e:
            print("err_having_IP_Address", e)
            return 0

    def having_At_Symbol(url):
        try:
            symbol = regex.findall(r'@', url)
            if (len(symbol) == 0):
                print("No @ symbol")
                return -1

            else:
                print("Url is having @ symbol")
                return 1

        except Exception as e:
            print("err_having_At_Symbol", e)
            return 0

    def Prefix_Suffix(url):
        try:
            subDomain, domain, suffix = extract(url)
            if (domain.count('-')):
                print("Url has prefix")
                return 1

            else:
                return -1
        except Exception as e:
            print("err_Prefix_Suffix", e)
            return 0

    def having_Sub_Domain(url):
        try:
            subDomain, domain, suffix = extract(url)
            if (subDomain.count('.') == 0):
                return -1
            elif (subDomain.count('.') == 1):
                print("subdomains 2")
                return 0

            else:
                print("Subdomains more than 1")
                return 1

        except Exception as e:
            print("err_having_Sub_Domain", e)
            return 0

    def Domain_registeration_length(url):
        try:
            w = whois.whois(url)
            updated = w.creation_date
            exp = w.expiration_date
            if type(updated) == list:
                updated = updated[-1]
            if type(exp) == list:
                exp = exp[-1]

            length = (exp - updated).days
            if (length <= 365):
                return 1
            else:
                return -1
        except Exception as e:
            print("err_Domain_registration_length", e)
            return 0

    def port(url):
        try:
            subDomain, domain, suffix = extract(url)
            host_name = domain + "." + suffix
            DEFAULT_TIMEOUT = 0.5
            open_port = []
            list_ports = [21, 22, 23, 80, 443, 445, 1433, 1521, 3306, 3389]
            timeout = DEFAULT_TIMEOUT
            TCPsock = socket.socket()
            TCPsock.settimeout(timeout)
            TCPsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            try:
                for i in list_ports:
                    result = TCPsock.connect((host_name, i))
                    if result == 0:
                        open_port.append(i)
            except:
                pass
            if (80, 443 in open_port) and len(list_ports) > 2:
                return 1
            elif (80, 443 in open_port) and len(list_ports) == 2:
                return -1
            else:
                return 1
        except Exception as e:
            print("err_port", e)
            return 0

    def HTTPS_token(url):
        try:
            subDomain, domain, suffix = extract(url)
            host = subDomain + '.' + domain + '.' + suffix
            if (host.count('https')):
                return 1
            else:
                return -1
        except Exception as e:
            print("errr https")
            return 0

    def Request_URL(url):
        try:
            r = requests.get(url, timeout=7)
            html = r.text
            url_elems = extract(url)
            domain = url_elems[1] + "." + url_elems[2]

            regex_external = "(href=|src=)(\"|')((https|http)://)"

            links = regex.findall(regex_external, html)

            regex_all = "(href=|src=)(\"|')(.*?)(\"|')"
            total_links = len(regex.findall(regex_all, html))

            count_diff = 0  # number of external domains
            for link in links:
                domain_of_link = urlparse(link[2])[1]
                domain_elements = domain_of_link.split(".")
                domain_of_link = ".".join(domain_elements[len(domain_elements) - 2:len(domain_elements)])
                count_diff += domain_of_link != domain
            if (total_links == 0):
                return 1

            diff_rate = count_diff / total_links

            if diff_rate < 0.22:
                return -1
            elif diff_rate <= 0.61:
                return 0
            else:
                return 1
        except Exception as e:
            return 0

    def URL_of_Anchor(url):
        try:
            t1 = time.time()
            regex_str = "<a href=\".*?\""
            html = requests.get(url, timeout=7).text
            links_list = regex.findall(regex_str, html)
            count_internal = 0

            for link in links_list:
                if url_is_internal(link, url):
                    count_internal += 1

            if len(links_list) == 0:
                return 1

            count_anchor = len(links_list) - count_internal
            rate = count_anchor / len(links_list)
            if (rate < 0.31):
                return -1
            elif (0.31 <= rate <= 0.67):
                return 0
            else:
                return 1
        except Exception as e:
            return 0

    def Redirect(url):
        try:
            r = requests.get(url, timeout=7)
            redirections = len(r.history)

            if redirections == 0:
                return -1
            elif redirections > 0 and redirections < 3:
                return 0
            else:
                return 1
        # still need to validate client redirecting sites
        except Exception as e:
            return 0

    def on_mouseover(url):
        try:
            html = requests.get(url, timeout=7).text
            soup = BeautifulSoup(html, 'html.parser')
            p = soup.find_all('script')
            result = 1
            strr = ""
            for jss in p:
                strr = strr + jss.text
            if "window.status" in strr:
                result = -1
            return result
        except Exception as e:
            return 0

    def RightClick(url):
        try:
            html = requests.get(url, timeout=7).text
            soup = BeautifulSoup(html, 'html.parser')
            p = soup.find_all('script')
            result = 1
            strr = ""
            for jss in p:
                strr = strr + jss.text
            if "contextmenu" in strr:
                result = -1
            return result
        except Exception as e:
            return 0

    def popUpWidnow(url):
        try:
            html = requests.get(url, timeout=7).text
            soup = BeautifulSoup(html, 'html.parser')
            p = soup.find_all('script')
            result = 1
            strr = ""
            for jss in p:
                strr = strr + jss.text
            if "window.open" in strr:
                result = -1
            return result
        except Exception as e:
            return 0

    def Iframe(url):
        try:
            html = requests.get(url, timeout=7).text
            if "</iframe>" in html:
                return -1
            else:
                return 1
        except Exception as e:
            return 0

    def age_of_domain(url):
        try:
            w = whois.whois(url)
            start_date = w.creation_date
            current_date = datetime.datetime.now()

            if type(start_date) == list:
                start_date = start_date[-1]

            age = (current_date - start_date).days

            if (age >= 180):
                return -1
            else:
                return 1
        except Exception as e:
            return 0

    def DNSRecord(url):
        try:
            try:
                subDomain, domain, suffix = extract(url)
                print(domain + "." + suffix)
                result = dns.resolver.query(domain + "." + suffix, 'A')
                print(result)
                for i in result:
                    print(i)
                    if i:
                        return -1
            except:
                return 1
        except Exception as e:
            print("err_DNSRecord")
            return 0

    def web_traffic(url):
    try:
        subDomain, domain, suffix = extract(url)
            
        host_name = domain + "." + suffix
    
        # Load the Alexa CSV file into a DataFrame
        alexa_data = pd.read_csv('top-1m.csv')

        # Find the rank for the given URL
        rank_info = alexa_data[alexa_data['domain'] == host_name]

        # Check if the URL exists in the Alexa data
        if rank_info.empty:
            return 1

        # Extract the rank value
        rank = rank_info.index[0]

        if rank < 100000:
            return -1
        else:
            return 1
    except Exception as e:
        return 0

    def Page_Rank(url):
        try:
            s, dom, ss, is_private = extract(url)

            # Check the number of values returned by extract(url)
            if len(s) != 3:
                # Handle the case where the expected number of values is not returned
                raise ValueError("extract(url) should return 3 values")

            URL = "https://openpagerank.com/api/v1.0/getPageRank"
            PARAMS = {'domains[]': dom + '.' + ss}
            r = requests.get(URL, params=PARAMS, headers={'API-OPR': '8044swwk8og00wwgc8ogo80cocs00o0o4008kkg0'},
                             timeout=7)
            json_data = r.json()
            domainarray = json_data['response']
            target = domainarray[0]
            rank = target['rank']
            print(rank)
            print(float(rank or 0.1))
            if rank == "None" or float(rank or 0.1) < 0.2:
                return 1
            else:
                return -1
        except ValueError as ve:
            return 0
        except Exception as e:
            return 0


    def Google_Index(url):
        try:
            r = requests.head("https://webcache.googleusercontent.com/search?q=cache:" + url, timeout=7)
            if r.status_code == 404:
                return 1
            else:
                return -1
        except:
            return 0


def fix_url(url_string):
    # Function to fix the URL format
    if "http://" in url_string or "https://" in url_string:
        url_string = url_string
    else:
        url_string = ''.join(("http://", url_string))

    if "www" in url_string:
        url_string = url_string
    else:
        ur = url_string.split('://')[-1]
        ur1 = url_string.split(ur)[0]
        ur2 = ''.join(("www.", ur))
        url_string = ''.join((ur1, ur2))

    return url_string

def run(url):
    urll = url
    data = {}
    data['check_connection'] = CheckUrlFeature.check_connection(urll)
    data['having_IP_Address'] = CheckUrlFeature.having_IP_Address(urll)
    data['having_At_Symbol'] = CheckUrlFeature.having_At_Symbol(urll)
    data['Prefix_Suffix'] = CheckUrlFeature.Prefix_Suffix(urll)
    data['having_Sub_Domain'] = CheckUrlFeature.having_Sub_Domain(urll)
    data['Domain_registeration_length'] = CheckUrlFeature.Domain_registeration_length(urll)
    data['port'] = CheckUrlFeature.port(urll)
    data['HTTPS_token'] = CheckUrlFeature.HTTPS_token(urll)
    data['Request_URL'] = CheckUrlFeature.Request_URL(urll)
    data['URL_of_Anchor'] = CheckUrlFeature.URL_of_Anchor(urll)
    data['Redirect'] = CheckUrlFeature.Redirect(urll)
    data['on_mouseover'] = CheckUrlFeature.on_mouseover(urll)
    data['RightClick'] = CheckUrlFeature.RightClick(urll)
    data['popUpWidnow'] = CheckUrlFeature.popUpWidnow(urll)
    data['Iframe'] = CheckUrlFeature.Iframe(urll)
    data['age_of_domain'] = CheckUrlFeature.age_of_domain(urll)
    data['DNSRecord'] = CheckUrlFeature.DNSRecord(urll)
    data['web_traffic'] = CheckUrlFeature.web_traffic(urll)
    data['Page_Rank'] = CheckUrlFeature.Page_Rank(urll)
    data['Google_Index'] = CheckUrlFeature.Google_Index(urll)
    data['URL'] = urll
    return data
