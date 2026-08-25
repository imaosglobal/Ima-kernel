
from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any, Dict, Optional


@dataclass
class EconomicModel:
    customer: str
    offer: str
    price: float = 0.0
    expected_revenue: float = 0.0
    acquisition_cost: float = 0.0
    operating_cost: float = 0.0
    expected_conversion: float = 0.0
    expected_lifetime_value: float = 0.0

    @property
    def gross_profit(self) -> float:
        return self.expected_revenue - self.operating_cost

    @property
    def contribution_profit(self) -> float:
        return self.expected_revenue - self.acquisition_cost - self.operating_cost

    @property
    def margin(self) -> float:
        if self.expected_revenue <= 0:
            return 0.0
        return self.contribution_profit / self.expected_revenue

    @property
    def roi(self) -> float:
        cost = self.acquisition_cost + self.operating_cost
        if cost <= 0:
            return 0.0
        return self.contribution_profit / cost

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data.update({
            "gross_profit": self.gross_profit,
            "contribution_profit": self.contribution_profit,
            "margin": self.margin,
            "roi": self.roi,
        })
        return data


def evaluate_opportunity(
    customer: str,
    offer: str,
    price: float,
    conversion: float,
    acquisition_cost: float = 0.0,
    operating_cost: float = 0.0,
    lifetime_value: Optional[float] = None,
) -> Dict[str, Any]:

    expected_revenue = price * max(0.0, min(1.0, conversion))

    model = EconomicModel(
        customer=customer,
        offer=offer,
        price=float(price),
        expected_revenue=expected_revenue,
        acquisition_cost=float(acquisition_cost),
        operating_cost=float(operating_cost),
        expected_conversion=float(conversion),
        expected_lifetime_value=float(
            lifetime_value if lifetime_value is not None else expected_revenue
        ),
    )

    return model.to_dict()
