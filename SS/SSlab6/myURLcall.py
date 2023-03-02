# import requests
# import webbrowser 

# url = 'https://www.cnn.com'
# webbrowser.register('firefox', None, webbrowser.BackgroundBrowser(r"C:/Users/tkokhing/Desktop/Tor Browser/Browser/firefox.exe"))

# webbrowser.get('firefox').open(url)
# # import user_agents 
# # from fake_useragent import UserAgent


from typing import Dict, List
import requests
import urllib.request
import pandas as pd
import time
from random import shuffle
import json
# websites = [
#     "https://google.com",
#     "https://youtube.com",
#     "https://facebook.com",
#     "https://baidu.com",
#     "https://instagram.com",
#     "https://cnn.com",
#     "https://yahoo.com",
#     "https://msn.com",
#     "https://wikipedia.org",
#     "https://twitter.com",
#     "https://amazon.com",
#     "https://sutd.edu.sg",
#     "https://linkedin.com",
#     "https://whatsapp.com",
#     "https://ntu.edu.sg/",
#     "https://outlook.live.com/owa/",
#     "https://bing.com",
#     "https://live.com",
#     "https://www.mail.com/",
#     "https://www.okta.com/"
# ]
# Testing with two sites
websites = [
    "https://google.com",
    "https://youtube.com",
        "https://sutd.edu.sg",
    "https://linkedin.com",
    "https://whatsapp.com",
    "https://ntu.edu.sg/",
    "https://outlook.live.com"
]

if __name__ == "__main__":
    website_load_times : Dict[str, List[float]] = { w: [] for w in websites}
    website_requests = websites * 20
    shuffle(website_requests)
    for r in website_requests:
        start_time = time.time()
        # print(r)
        # print(type(r))
        # requests.post(r)
        # # requests.
        urllib.request.urlretrieve(str(r))
        end_time = time.time()
        website_load_times[r].append(end_time - start_time)
    f = open("20results_wout_tor.json", "w")

    computed_data = [
        {
            "website": website,
            "min": min(load_times),
            "max": max(load_times),
            "avg": sum(load_times) / 20,
            "median": sorted(load_times)[10]
        }
        for website, load_times in website_load_times.items()
        
            
    ]
    json.dump(website_load_times, f)
    df = pd.DataFrame(computed_data)
    df.to_csv("20results_wout_tor.csv")