import requests
import logging
from urllib.parse import urlparse
from datetime import datetime, timedelta
import tldextract

logger = logging.getLogger(__name__)

# Source URLs
SOURCES = {
    "porn": "https://raw.githubusercontent.com/StevenBlack/hosts/master/alternates/porn-only/hosts",
    "social": "https://raw.githubusercontent.com/StevenBlack/hosts/master/alternates/social-only/hosts",
    "gambling": "https://raw.githubusercontent.com/StevenBlack/hosts/master/alternates/gambling-only/hosts",
    "admalware": "https://raw.githubusercontent.com/StevenBlack/hosts/master/hosts",
}

# Refresh interval: 1 hour
REFRESH_INTERVAL = timedelta(hours=1)

class CategoryChecker:
    def __init__(self):
        self.categories: dict[str, set[str]] = {
            "porn": set(),
            "social": set(),
            "gambling": set(),
            "admalware": set(),
        }
        self.last_fetched: datetime | None = None

    def fetch_hosts(self, url: str) -> set[str]:
        """Fetch and parse hosts file from URL."""
        domains = set()
        try:
            logger.info(f"Fetching {url}")
            response = requests.get(url, timeout=30)
            response.raise_for_status()

            for line in response.text.splitlines():
                line = line.strip()
                if not line or line.startswith("#"):
                    continue

                # Standard hosts file format: 0.0.0.0 domain.com
                parts = line.split()
                if len(parts) >= 2:
                    domain = parts[1]
                    domains.add(domain)

            logger.info(f"Loaded {len(domains)} domains from {url}")
        except Exception as e:
            logger.error(f"Failed to fetch {url}: {e}")

        return domains

    def load_all(self):
        """Load all categories."""
        for category, url in SOURCES.items():
            self.categories[category] = self.fetch_hosts(url)
        self.last_fetched = datetime.now()
        logger.info(f"All lists loaded at {self.last_fetched}")

    async def refresh_if_needed(self):
        """Refresh lists if more than REFRESH_INTERVAL has passed since last fetch."""
        if self.last_fetched is None:
            logger.info("No previous fetch detected, loading lists...")
            self.load_all()
            return

        time_since_fetch = datetime.now() - self.last_fetched
        if time_since_fetch >= REFRESH_INTERVAL:
            logger.info(f"Refreshing lists (last fetch was {time_since_fetch} ago)")
            self.load_all()
        else:
            logger.debug(f"No refresh needed (last fetch was {time_since_fetch} ago)")

    def check_url(self, url: str) -> dict[str, bool]:
        """Check a URL against all categories."""
        # Strip potential surrounding quotes
        url = url.strip("'\"")

        # Extract domain
        # usage of tldextract is robust for subdomains
        extracted = tldextract.extract(url)
        domain = f"{extracted.domain}.{extracted.suffix}"
        subdomain = f"{extracted.subdomain}.{extracted.domain}.{extracted.suffix}" if extracted.subdomain else domain

        # We also want to check the full hostname from urlparse just in case
        parsed = urlparse(url if "://" in url else f"http://{url}")
        hostname = parsed.hostname or ""

        # Remove 'www.' if present for checking
        cleaning_candidates = {hostname, domain, subdomain}
        cleaned_candidates = set()
        for cand in cleaning_candidates:
            cleaned_candidates.add(cand)
            if cand.startswith("www."):
                cleaned_candidates.add(cand[4:])

        result = {}
        for category, domains in self.categories.items():
            # Check if any candidate matches
            match = False
            for cand in cleaned_candidates:
                if cand in domains:
                    match = True
                    break
            result[category] = match

        return result
