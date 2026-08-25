class GeminiAgent:
    def investigate(self, question):
        q = question.lower()
        if "revenue" in q or "70/20/10" in q:
            ans = "GEMINI: Business Model. 70% Vault = IMA operating revenue. 20% Impact = tax benefits + government grants. 10% Growth = CAC. Risk: No multisig. Fix: 2-of-3 multisig + 24h timelock before any auto-deposit."
        elif "operationally" in q or "run" in q:
            ans = "GEMINI: Ops Flow. 1. EducationEngine collects payment 2. Treasury contract auto-splits 70/20/10 3. Governance DAO votes on 20% 4. Growth pool funds marketing. Need: Monitoring + alerts for failed splits."
        elif "productization" in q or "global" in q or "1000" in q:
            ans = "GEMINI: GTM. Phase1: Free pilots in 3 countries funded by 20% Impact. Phase2: B2B $2/student. Phase3: API ecosystem. First 1000 users = teachers. Price: Freemium. Key: 'We give 20% back' is your differentiator."
        else:
            ans = "GEMINI REVIEW: Security first. Add multisig, timelock, emergency pause, child safety filters."
        return {"agent": "GEMINI", "status": "ANSWER_READY", "answer": ans}
