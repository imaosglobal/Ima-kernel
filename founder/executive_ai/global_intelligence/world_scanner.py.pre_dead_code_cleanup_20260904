from __future__ import annotations

import time
import signal as signal_module

from founder.executive_ai.memory.memory_store import save_memory
from learning.source_manager import registry


class SignalScanner:
    def normalize(
        self,
        source,
        title,
        category,
        importance,
        content="",
        url="",
    ):
        return {
            "source": source,
            "title": title,
            "category": category,
            "importance": importance,
            "content": content[:5000],
            "url": url,
            "timestamp": time.time(),
        }

    def ingest(self, signal):
        save_memory("market_signals", signal)
        return signal


class WorldScanner:
    """
    Canonical world discovery layer.

    Uses the single learning.source_manager registry.
    Does not create another source registry or discovery loop.
    """

    DISCOVERY_QUESTIONS = (
        "latest artificial intelligence research and technology developments",
        "latest scientific research discoveries",
        "latest technology industry developments",
        "latest government digital innovation programs",
    )

    def __init__(self):
        self.scanner = SignalScanner()

    def scan_sources(self):
        signals = []
        seen = set()

        class SourceTimeout(Exception):
            pass

        def timeout_handler(signum, frame):
            raise SourceTimeout("source collection timeout")

        previous_handler = signal_module.signal(signal_module.SIGALRM, timeout_handler)

        try:
            for question in self.DISCOVERY_QUESTIONS:
                try:
                    # Never allow one external source to block the autonomous cycle.
                    signal_module.setitimer(signal_module.ITIMER_REAL, 5.0)
                    results = registry.collect(question)
                    signal_module.setitimer(signal_module.ITIMER_REAL, 0)
                except (SourceTimeout, Exception):
                    signal_module.setitimer(signal_module.ITIMER_REAL, 0)
                    continue

                for result in results:
                    if not isinstance(result, dict):
                        continue

                    content = str(result.get("content", "")).strip()
                    source = str(
                        result.get("source")
                        or result.get("registry_source")
                        or ""
                    ).strip()

                    if not source or not content:
                        continue

                    title = str(
                        result.get("title")
                        or f"{source}: discovery signal"
                    ).strip()

                    key = (
                        source.casefold(),
                        title.casefold(),
                        content[:300],
                    )

                    if key in seen:
                        continue

                    seen.add(key)

                    discovery_signal = self.scanner.normalize(
                        source=source,
                        title=title,
                        category="world_discovery",
                        importance=int(result.get("importance", 50)),
                        content=content,
                        url=str(result.get("url", "")),
                    )

                    self.scanner.ingest(discovery_signal)
                    signals.append(discovery_signal)
        finally:
            signal_module.setitimer(signal_module.ITIMER_REAL, 0)
            signal_module.signal(signal_module.SIGALRM, previous_handler)

        return signals

        for question in self.DISCOVERY_QUESTIONS:
            try:
                results = registry.collect(question)
            except Exception:
                continue

            for result in results:
                if not isinstance(result, dict):
                    continue

                content = str(result.get("content", "")).strip()
                source = str(
                    result.get("source")
                    or result.get("registry_source")
                    or ""
                ).strip()

                if not source or not content:
                    continue

                title = str(
                    result.get("title")
                    or f"{source}: discovery signal"
                ).strip()

                key = (
                    source.casefold(),
                    title.casefold(),
                    content[:300],
                )

                if key in seen:
                    continue

                seen.add(key)

                signal = self.scanner.normalize(
                    source=source,
                    title=title,
                    category="world_discovery",
                    importance=int(result.get("importance", 50)),
                    content=content,
                    url=str(result.get("url", "")),
                )

                self.scanner.ingest(signal)
                signals.append(signal)

        return signals


world_scanner = WorldScanner()
