
from founder.executive_ai.memory.memory_store import save_memory
import time


class SignalScanner:


    def normalize(
        self,
        source,
        title,
        category,
        importance
    ):

        return {

            "source": source,

            "title": title,

            "category": category,

            "importance": importance,

            "timestamp": time.time()

        }



    def ingest(self,signal):

        save_memory(
            "market_signals",
            signal
        )

        return signal



class WorldScanner:


    def __init__(self):

        self.scanner = SignalScanner()



    def scan_sources(self):

        signals=[]


        # placeholders for external adapters

        sources=[

            {
                "source":"ai_news",
                "title":"AI infrastructure growth signal",
                "category":"AI",
                "importance":80
            },

            {
                "source":"government",
                "title":"New digital education program",
                "category":"government",
                "importance":70
            }

        ]


        for s in sources:

            signal=self.scanner.normalize(
                **s
            )

            self.scanner.ingest(
                signal
            )

            signals.append(
                signal
            )


        return signals



world_scanner = WorldScanner()

