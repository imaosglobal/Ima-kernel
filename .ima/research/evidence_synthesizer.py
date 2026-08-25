from collections import Counter


class EvidenceSynthesizer:

    name = "EVIDENCE_SYNTHESIZER"

    def synthesize(self, agent_results):

        successful = []
        unavailable = []
        statuses = Counter()

        for result in agent_results or []:

            status = result.get(
                "status",
                "UNKNOWN"
            )

            statuses[status] += 1

            if status in {
                "ANSWER_READY",
                "READY",
                "COMPLETE",
                "SUCCESS",
            }:
                successful.append(result)

            else:
                unavailable.append(result)

        return {
            "successful_results": len(successful),
            "failed_or_unavailable": len(unavailable),
            "status_counts": dict(statuses),
            "successful_agents": [
                r.get("agent")
                for r in successful
            ],
            "unavailable_agents": [
                r.get("agent")
                for r in unavailable
            ],
            "disagreement_policy": {
                "never_collapse_disagreement": True,
                "separate_evidence_from_inference": True,
                "preserve_competing_hypotheses": True,
            },
        }
