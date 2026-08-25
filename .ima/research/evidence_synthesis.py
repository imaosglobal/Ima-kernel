
class EvidenceSynthesis:

    def synthesize(self, agent_results):

        successful = []
        unavailable = []
        sources = []

        for result in agent_results:

            status = result.get("status")

            if status in (
                "ANSWER_READY",
                "READY"
            ):
                successful.append(result)

            elif status in (
                "TIMEOUT",
                "CAPABILITY_PENDING",
                "ERROR",
                "EXCEPTION"
            ):
                unavailable.append(result)

            for paper in result.get(
                "papers", []
            ):
                sources.append(paper)

            for paper in result.get(
                "results", []
            ):
                sources.append(paper)

        return {
            "successful_results": len(
                successful
            ),
            "unavailable_results": len(
                unavailable
            ),
            "source_count": len(sources),
            "sources": sources,
            "principles": [
                "A retrieved source is not automatically evidence.",
                "Relevance does not establish truth.",
                "Citation count does not establish correctness.",
                "Separate empirical evidence from interpretation.",
                "Preserve competing hypotheses.",
                "Preserve unresolved disagreement.",
            ],
        }
