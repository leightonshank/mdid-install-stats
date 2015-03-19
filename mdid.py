import requests
import ssl
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.poolmanager import PoolManager
from google import search
from urlparse import urlparse
from bs4 import BeautifulSoup

hosts_seen = []
mdid_sites = {}
result_count = 0

class SSLTLSv1Adapter(HTTPAdapter):
    """Adapter to force SSL TLSv1"""
    def init_poolmanager(self, connections, maxsize, block=False):
        self.poolmanager = PoolManager(num_pools=connections,
                maxsize=maxsize,
                block=block,
                ssl_version=ssl.PROTOCOL_TLSv1)


def get_hostname(url):
    """Parse the hostname from a URL"""
    result = urlparse(url)
    return result.hostname


def detect_version(url):
    """Simple detector to determine what version of MDID a site is running"""
    try:
        r = requests.get(url)
    except requests.exceptions.SSLError:
        # got an SSLError, which I'm assuming to be the error you get when a
        # site wants to use TLSv1, so we'll give that a shot
        s = requests.Session()
        s.mount('https://', SSLTLSv1Adapter())
        try:
            r = s.get(url)
        except requests.exceptions.SSLError:
            # if we got an SSLError here, then as a last-ditch we'll try the
            # request again w/o SSL verification
            try:
                r = s.get(url, verify=False)
            except requests.exceptions.SSLError:
                print "  ERROR!  Too many SSLError exceptions.  Giving up."
                return None

    if r.status_code == 200:
        soup = BeautifulSoup(r.content)
        # look for MDID3 by detecting the help link, it seems the most unique
        # <a href="..." id="pagehelp" target="rooibos_help">Help</a>
        a = soup.find(id='pagehelp')
        if a and a.get('target') == 'rooibos_help':
            return 'MDID3'

        # look for MDID2 by checking the help link also.  why not, eh?
        a = soup.find(id='_ctl0_HelpLink')
        if a and a.get('href') == '/help/helpfile.htm':
            return 'MDID2'

    # No MDID found
    return None

# main
try:
    for url in search('mdid', only_standard=True, stop=20):
        # get the hostname from the url
        hostname = get_hostname(url)
        # don't process if we've already seen this host
        if hostname in hosts_seen:
            continue

        print 'examining {url}...'.format(url=url)
        # try and detect the MDID version running on the host
        version = detect_version(url)
        if version:
            mdid_sites[hostname] = version
            print '    {host} => {mdid}'.format(host=hostname, mdid=version)
        else:
            print '    No MDID installation detected'
        result_count += 1
except KeyboardInterrupt:
    # capture ctrl-c so we can stop the script but still
    # save our state below
    # TODO: dump mdid_sites and result_count to json so we can pickup where
    #       we stopped
    print 'INTERRUPT!  Saving state and quitting.'
