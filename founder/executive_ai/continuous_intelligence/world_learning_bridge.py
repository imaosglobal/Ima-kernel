from founder.executive_ai.global_intelligence.world_scanner import world_scanner


def collect_world_learning():
    """
    Canonical world-learning bridge.

    The master cycle and autonomous action cycle now consume the
    same WorldScanner implementation.
    """

    items = world_scanner.scan_sources()

    return {
        "source": "world",
        "status": "collected",
        "items": items,
    }
