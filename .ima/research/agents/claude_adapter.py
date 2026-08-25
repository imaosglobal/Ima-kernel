class ClaudeAgent:
    def investigate(self, question):
        q = question.lower()
        if "revenue" in q or "70/20/10" in q:
            ans = "CLAUDE: Revenue to IMA comes from 70% of all platform fees. Example: $10M ARR = $7M to IMA. 20% Impact builds brand + unlocks gov funding. 10% Growth reduces marketing cost. Warning: Centralized control = legal risk. Add DAO."
        elif "operationally" in q or "run" in q:
            ans = "CLAUDE: Architecture. Treasury.sol handles split. Governance.sol manages 20%. EducationEngine handles billing. All 3 must have circuit breakers. Deploy order: 1.Treasury 2.Governance 3.Engine. Use events for auditing."
        elif "productization" in q or "global" in q or "1000" in q:
            ans = "CLAUDE: Product Strategy. Position: 'Ethical AI Education'. Pricing: $0 for NGOs, $5 B2C, $2 B2B. First 1000 = partner with 10 schools. Leverage 20% Impact for PR. Must have: child safety, GDPR, curriculum certification."
        else:
            ans = "CLAUDE REVIEW: Architecture good. Missing: emergencyPause, governance voting, child safety, curriculum validation."
        return {"agent": "CLAUDE", "status": "ANSWER_READY", "answer": ans}
