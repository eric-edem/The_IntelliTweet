import ast
import requests
import csv

class LinkVerifier:
    def __init__(self, api_key):
        self.api_key = api_key
        self.Links = []
        self.Verified_Links = []
        self.Unverified_links = []
        self.Links_Dict = {}
        self.urll = 'https://www.virustotal.com/vtapi/v2/url/report'

    def collect_links(self, df):
        for i in df.URLs:
            for j in ast.literal_eval(i):
                if j not in self.Links:
                    if 'twitter' not in j:
                        self.Links.append(j)

    def verify_links(self):
        for link in self.Links:
            params = {'apikey': self.api_key, 'resource': link}
            response = requests.get(self.urll, params=params)
            try:
                yes = response.json().get("scans").items()
                for key, value in yes:
                    for k, v in value.items():
                        if v == True:
                            if link not in self.Verified_Links:
                                self.Verified_Links.append(link)

                            if link in self.Links_Dict:
                                self.Links_Dict[link].append(list((key, value)))
                            else:
                                self.Links_Dict[link] = list((key, value))
            except:
                self.Unverified_links.append(link)
                print(response.json().get("verbose_msg"))

    def save_results(self, verified_links_file, unverified_links_file):
        with open(verified_links_file, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Verified Links'])
            for link in self.Verified_Links:
                writer.writerow([link])

        with open(unverified_links_file, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Unverified Links'])
            for link in self.Unverified_links:
                writer.writerow([link])
