"""Evidence-bounded global IP provenance and stewardship contract.

The vault records provenance, rights status, contributors, jurisdictions and
license constraints. It does not itself grant ownership or legal protection.
Legal filing/registration decisions remain human/legal-professional actions.
"""

from dataclasses import dataclass, asdict
from typing import Literal


RightType = Literal[
    "copyright", "patent", "trademark", "design", "trade_secret",
    "database_right", "license", "contract", "open_source", "public_domain",
]


@dataclass(frozen=True)
class IPAssetRecord:
    asset_id: str
    title: str
    right_type: RightType
    provenance: str
    contributors: tuple[str, ...]
    owner_or_steward: str
    jurisdiction: str
    license_or_terms: str
    evidence_reference: str
    status: str = "PROVENANCE_RECORDED"


def record_asset(record: IPAssetRecord) -> dict:
    if not record.asset_id or not record.title or not record.provenance:
        raise ValueError("asset_id, title and provenance are required")
    return asdict(record)


def stewardship_rules() -> tuple[str, ...]:
    return (
        "never claim ownership without evidence",
        "preserve contributor attribution",
        "preserve source and license terms",
        "track jurisdiction and filing status separately",
        "keep private/confidential material access-controlled",
        "record corrections without erasing provenance history",
        "route patent/trademark/design/copyright filing decisions to qualified counsel",
        "AI is not recorded as a legal inventor merely because it generated or assisted output",
    )
