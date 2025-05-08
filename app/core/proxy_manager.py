import requests
import random
import time
from bs4 import BeautifulSoup

class FreeProxyManager:
    def __init__(self, sources=None, https_only=True):
        """
        Enhanced proxy manager supporting multiple free proxy sources.
        """
        self.https_only = https_only
        self.user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'
        self.sources = sources or [
            'proxyscrape',   # Plaintext API
            'openproxyspace',# Plaintext API
            'proxynova',     # HTML table
        ]
        self.proxies = []
        self.refresh_proxies()
        
    def refresh_proxies(self):
        """
        Refresh proxy list from all configured sources.
        """
        proxies = []
        for source in self.sources:
            try:
                if source == 'proxyscrape':
                    proxies += self._fetch_proxyscrape()
                elif source == 'openproxyspace':
                    proxies += self._fetch_openproxyspace()
                elif source == 'proxynova':
                    proxies += self._fetch_proxynova()
            except Exception as e:
                print(f"Error fetching from {source}: {e}")
        # Remove duplicates while preserving order
        seen = set()
        self.proxies = [p for p in proxies if not (p in seen or seen.add(p))]
        print(f"Fetched {len(self.proxies)} proxies from {self.sources}")

    def _fetch_proxyscrape(self):
        """
        Fetch proxies from proxyscrape.com (plain text list).
        """
        url = "https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=5000&country=all&ssl=all&anonymity=all"
        headers = {'User-Agent': self.user_agent}
        resp = requests.get(url, headers=headers, timeout=10)
        proxies = []
        for line in resp.text.strip().splitlines():
            if line:
                ip_port = line.strip()
                if ':' in ip_port:
                    proxy = f"http://{ip_port}"
                    proxies.append(proxy)
        return proxies

    def _fetch_openproxyspace(self):
        """
        Fetch proxies from openproxy.space (plain text list).
        """
        url = "https://openproxy.space/list/http"
        headers = {'User-Agent': self.user_agent}
        resp = requests.get(url, headers=headers, timeout=10)
        proxies = []
        for line in resp.text.strip().splitlines():
            if line and ':' in line:
                proxy = f"http://{line.strip()}"
                proxies.append(proxy)
        return proxies

    def _fetch_proxynova(self):
        """
        Fetch proxies from proxynova.com (HTML table).
        """
        url = "https://www.proxynova.com/proxy-server-list/"
        headers = {'User-Agent': self.user_agent}
        resp = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(resp.content, 'html.parser')
        proxies = []
        table = soup.find('table', attrs={'id': 'tbl_proxy_list'})
        if not table:
            return proxies
        for row in table.find_all('tr')[1:]:
            cols = row.find_all('td')
            if len(cols) >= 2:
                ip = cols[0].text.strip()
                port = cols[1].text.strip()
                if ip and port and ip != 'IP Address':
                    proxy = f"http://{ip}:{port}"
                    proxies.append(proxy)
        return proxies

    def get_proxy_list(self):
        """
        Return current list of proxies.
        """
        return self.proxies.copy()
    
    def get_random_proxy(self, max_attempts=20):
        """
        Get a random working proxy with basic validation.
        """
        for attempt in range(1, max_attempts + 1):
            if not self.proxies:
                self.refresh_proxies()
                if not self.proxies:
                    return None
            proxy = random.choice(self.proxies)
            print(f"Attempt {attempt}: Testing {proxy}")
            if self._validate_proxy(proxy):
                print(f"Valid proxy found: {proxy}")
                return proxy
            self.proxies.remove(proxy)
            time.sleep(0.5)
        print(f"No working proxies found after {max_attempts} attempts")
        return None

    def _validate_proxy(self, proxy, timeout=8):
        """
        Validate proxy by making a test request.
        """
        test_urls = [
            'https://httpbin.org/ip',
            'https://api.ipify.org?format=json',
            'https://icanhazip.com'
        ]
        try:
            session = requests.Session()
            session.proxies.update({'http': proxy, 'https': proxy})
            session.headers.update({'User-Agent': self.user_agent})
            for url in test_urls:
                try:
                    response = session.get(url, timeout=timeout)
                    if response.status_code == 200:
                        return True
                except requests.RequestException:
                    continue
        except Exception:
            pass
        return False
