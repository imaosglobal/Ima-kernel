from typing import Any


class EvidenceFilter:

    name = "EVIDENCE_FILTER"

    def filter_sources(self, sources: list[dict[str, Any]]) -> dict[str, Any]:

        accepted = []
        rejected = []

        for source in sources or []:

            title = str(
                source.get("title", "")
            ).strip()

            if not title:
                rejected.append({
                    "source": source,
                    "reason": "missing_title",
                })
                continue

            source_type = str(
                source.get("type", "")
            ).lower()

            metadata_only = source_type in {
                "dataset",
                "book",
                "book-chapter",
                "posted-content",
                "reference-entry",
            }

            item = dict(source)

            item["metadata_only"] = metadata_only

            item["evidence_status"] = (
                "BIBLIOGRAPHIC_ONLY"
                if metadata_only
                else "CANDIDATE_EVIDENCE"
            )

            accepted.append(item)

        return {
            "accepted": accepted,
            "rejected": rejected,
            "accepted_count": len(accepted),
            "rejected_count": len(rejected),
        }
