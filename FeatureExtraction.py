import ipaddress
import re
from urllib.parse import urlparse, urlencode
from bs4 import BeautifulSoup
import socket
import requests
from googlesearch import search
import whois
from datetime import date, datetime
import time
from dateutil.parser import parse as date_parse


def diff_month(d1, d2):
    return (d1.year - d2.year) * 12 + d1.month - d2.month


def generate_data_set(url):

    data_set = []

    if not re.match(r"^https?", url):
        url = "http://" + url

    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
    except:
        response = ""
        soup = -999

    domain = re.findall(r"://([^/]+)/?", url)[0]
    if re.match(r"^www.", domain):
        domain = domain.replace("www.", "")
    whois_response = whois.whois(domain)

    rank_checker_response = requests.post("https://www.checkpagerank.net/index.php", {
        "name": domain
    })

    try:
        global_rank = int(re.findall(
            r"Global Rank: ([0-9]+)", rank_checker_response.text)[0])
    except:
        global_rank = 1

    # 1.UsingIP
    try:
        ipaddress.ip_address(url)
        data_set.append(-1)
    except:
        data_set.append(1)

    if url.count('.')>4:
      data_set.append(1)
    else:
      data_set.append(0)
    # 4.Symbol@
    if re.findall("@", url):
        data_set.append(1)
    else:
        data_set.append(0)
    # 4.Symbol@
    if re.findall("#", url):
        data_set.append(1)
    else:
        data_set.append(0)

    # 2.LongURL
    if len(url) < 54:
        data_set.append(0)
    else:
        data_set.append(1)

    s = urlparse(url).path.split('/')
    depth = 0
    for j in range(len(s)):
      if len(s[j]) != 0:
        depth = depth+1
        return depth

    # 7.SubDomains
    if len(re.findall("\.", url)) == 1:
        data_set.append(0)
    elif len(re.findall("\.", url)) == 2:
        data_set.append(0)
    else:
        data_set.append(1)

    # 5.Redirecting//
    list = [x.start(0) for x in re.finditer('//', url)]
    if list[len(list)-1] > 6:
      if list[len(list)-1] > 7:
        data_set.append(1)
      else:
        data_set.append(0)
    else:
      data_set.append(0)
 
    # 12. HTTPSDomainURL
    if re.findall(r"^https://", url):
        data_set.append(1)
    else:
        data_set.append(0)
 
    # 3.ShortURL
    match = re.search('bit\.ly|goo\.gl|shorte\.st|go2l\.ink|x\.co|ow\.ly|t\.co|tinyurl|tr\.im|is\.gd|cli\.gs|'
                      'yfrog\.com|migre\.me|ff\.im|tiny\.cc|url4\.eu|twit\.ac|su\.pr|twurl\.nl|snipurl\.com|'
                      'short\.to|BudURL\.com|ping\.fm|post\.ly|Just\.as|bkite\.com|snipr\.com|fic\.kr|loopt\.us|'
                      'doiop\.com|short\.ie|kl\.am|wp\.me|rubyurl\.com|om\.ly|to\.ly|bit\.do|t\.co|lnkd\.in|'
                      'db\.tt|qr\.ae|adf\.ly|goo\.gl|bitly\.com|cur\.lv|tinyurl\.com|ow\.ly|bit\.ly|ity\.im|'
                      'q\.gs|is\.gd|po\.st|bc\.vc|twitthis\.com|u\.to|j\.mp|buzurl\.com|cutt\.us|u\.bb|yourls\.org|'
                      'x\.co|prettylinkpro\.com|scrnch\.me|filoops\.info|vzturl\.com|qr\.net|1url\.com|tweez\.me|v\.gd|tr\.im|link\.zip\.net', url)
    if match:
        data_set.append(1)
    else:
        data_set.append(0)

    # 6.PrefixSuffix-
    if re.findall(r"https?://[^\-]+-[^\-]+/", url):
        data_set.append(1)
    else:
        data_set.append(0)

   # 23. IframeRedirection
    if response == "":
        data_set.append(1)
    else:
        if re.findall(r"[<iframe>|<frameBorder>]", response.text):
            data_set.append(0)
        else:
            data_set.append(1)

    # 20. StatusBarCust
    if response == "":
        data_set.append(1)
    else:
        if re.findall("<script>.+onmouseover.+</script>", response.text):
            data_set.append(1)
        else:
            data_set.append(0)

    # 20. StatusBarCust
    if response == "":
        data_set.append(1)
    else:
        if re.findall("<script>.+onload.+</script>", response.text):
            data_set.append(1)
        else:
            data_set.append(0)

    # 21. DisableRightClick
    if response == "":
        data_set.append(1)
    else:
        if re.findall(r"event.button ?== ?2", response.text):
            data_set.append(0)
        else:
            data_set.append(1)

    # 19. WebsiteForwarding
    if response == "":
        data_set.append(1)
    else:
        if len(response.history) <= 2:
            data_set.append(0)
        else:
            data_set.append(1)
            
    return data_set
