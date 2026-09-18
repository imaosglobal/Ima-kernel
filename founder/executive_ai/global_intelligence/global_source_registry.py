from __future__ import annotations
from dataclasses import dataclass, asdict

@dataclass(frozen=True)
class Source:
    name: str
    kind: str
    verticals: tuple[str, ...]
    geography: str
    monetization: tuple[str, ...]
    url: str
    access: str = "public_or_account"

SOURCES = (
    Source("Awin", "affiliate_network", ("retail","travel","finance","insurance","services"), "global", ("cpa","cps","lead"), "https://www.awin.com/"),
    Source("CJ", "affiliate_network", ("retail","travel","services","finance"), "global", ("cpa","cps","lead"), "https://www.cj.com/"),
    Source("Partnerize", "partnership_network", ("retail","travel","finance","subscriptions"), "global", ("commission","referral"), "https://partnerize.com/"),
    Source("PartnerStack", "b2b_network", ("software","b2b","services"), "global", ("revshare","cpl","cpa","deal_registration"), "https://partnerstack.com/"),
    Source("impact.com", "partnership_platform", ("software","b2b","travel","finance","retail","services"), "global", ("affiliate","referral","cpa","revshare"), "https://impact.com/"),
    Source("Referr", "lead_marketplace", ("services","professional","b2b"), "country_dependent", ("lead_fee","referral"), "https://www.referr.co.uk/"),
    Source("Google News RSS", "public_demand", ("all"), "global", ("direct_referral","brokerage"), "https://news.google.com/"),
    Source("Partner program directories", "program_directory", ("all"), "global", ("affiliate","referral","reseller"), "https://www.partnerstack.com/"),
    Source("SAM.gov Contract Opportunities", "public_demand", ("b2b","equipment","services"), "US", ("brokerage","referral","reseller"), "https://sam.gov/opportunities"),
    Source("TED Search API", "public_demand", ("b2b","equipment","services"), "EU", ("brokerage","referral","reseller"), "https://api.ted.europa.eu/v3/notices/search"),
    Source("TED Open Data", "public_demand", ("b2b","equipment","services"), "EU", ("brokerage","referral","reseller"), "https://docs.ted.europa.eu/ODS/latest/"),
)

def all_sources():
    return [asdict(s) for s in SOURCES]
