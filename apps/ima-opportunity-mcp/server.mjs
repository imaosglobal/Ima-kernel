import express from "express";
import { randomUUID } from "node:crypto";
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StreamableHTTPServerTransport } from "@modelcontextprotocol/sdk/server/streamableHttp.js";
import { z } from "zod";

const PORT = Number(process.env.PORT || 8000);

function createServer() {
  const server = new McpServer({
    name: "ima-opportunity-intelligence",
    version: "1.0.0"
  });

  server.registerTool(
    "evaluate_ecosystem_opportunity",
    {
      title: "Evaluate Full Ecosystem Opportunity",
      description:
        "Evaluate a product, launch or technology together with its surrounding ecosystem: platform, distribution, content, community, merchandise, advertising, APIs, integrations, competitors, substitutes, accessibility, partnerships, business models and legal/privacy/safety constraints. Never invent demand, licensing, partners, approval, prices or results.",
      inputSchema: {
        subject: z.string().min(1).describe("Product, launch, technology or opportunity."),
        context: z.string().optional().describe("Known facts or supplied context."),
        budget: z.string().optional().describe("Available budget; default is zero."),
        authorizedActions: z.string().optional().describe("Explicitly authorized actions, if any.")
      },
      annotations: { readOnlyHint: true, destructiveHint: false, openWorldHint: false }
    },
    async ({ subject, context = "", budget = "0", authorizedActions = "" }) => {
      const dimensions = [
        "core_product_or_service",
        "launch_and_lifecycle",
        "official_ecosystem_and_distribution",
        "companion_products_accessories_merchandise_licensing",
        "advertising_sponsorship_commercial_formats",
        "content_creators_community_media_education",
        "apis_sdks_mcp_agents_integrations",
        "competitors_substitutes_adjacent_solutions",
        "users_accessibility_underserved_needs",
        "business_model_value_capture_zero_cost_test",
        "ip_licensing_terms_privacy_safety_authorization",
        "ima_capability_fit_and_reuse",
        "evidence_uncertainty_outcomes"
      ];
      const text = [
        "IMA Ecosystem Opportunity Intelligence v1.0",
        "",
        `Subject: ${subject}`,
        `Context: ${context || "none supplied"}`,
        `Budget: ${budget}`,
        `Authorized actions: ${authorizedActions || "none supplied"}`,
        "",
        "Required ecosystem scan:",
        ...dimensions.map((d, i) => `${i + 1}. ${d}`),
        "",
        "Canonical execution:",
        "DISCOVER → MAP ECOSYSTEM → VERIFY EVIDENCE → CHECK AUTHORITY/IP/TERMS/PRIVACY/SAFETY → REUSE IMA → BUILD ONLY MISSING REUSABLE CAPABILITY → INTEGRATE → TEST END-TO-END → DEPLOY → RUNTIME VERIFY → MEASURE VALUE → DOCUMENT PROVENANCE → REGRESSION TEST.",
        "",
        "Truth boundary: planned, implemented, deployed, runtime-verified, usable-now and successful are distinct states.",
        "Action boundary: zero-cost reversible technical work may be executed when authorized; purchases, spending, unsolicited outreach, irreversible commitments and unverified partnership/licensing claims require explicit authorization and evidence.",
        "Initial verdict: INSUFFICIENT EVIDENCE until material claims and the relevant ecosystem dimensions are verified."
      ].join("\n");
      return {
        content: [{ type: "text", text }],
        structuredContent: {
          subject,
          dimensions,
          verdict: "insufficient_evidence",
          next_action: "verify_material_claims_then_run_smallest_zero_cost_reversible_test",
          canonicalContract: "docs/IMA_ECOSYSTEM_OPPORTUNITY_CONTRACT_v1.0.md"
        }
      };
    }
  );

  server.registerTool(
    "evaluate_opportunity",
    {
      title: "Evaluate Business Opportunity",
      description:
        "Evaluate a business opportunity using evidence, uncertainty, commercial risk and a zero-cost reversible test. Never invent demand, customers, partners, prices or results.",
      inputSchema: {
        opportunity: z.string().min(1).describe("The business opportunity to evaluate."),
        evidence: z.string().optional().describe("Known evidence supporting or contradicting the opportunity."),
        budget: z.string().optional().describe("Available budget; use 0 or free-first when applicable.")
      },
      annotations: {
        readOnlyHint: true,
        destructiveHint: false,
        openWorldHint: false
      }
    },
    async ({ opportunity, evidence = "", budget = "0" }) => {
      const text = [
        "IMA Opportunity Intelligence",
        "",
        `Opportunity: ${opportunity}`,
        `Evidence supplied: ${evidence || "none"}`,
        `Budget supplied: ${budget}`,
        "",
        "Method:",
        "1. Separate facts, assumptions, estimates and unknowns.",
        "2. Assess demand evidence, revenue clarity, acquisition friction, delivery cost, trust/risk, time-to-value and reversibility.",
        "3. Identify the weakest link.",
        "4. Propose the cheapest zero-cost reversible test.",
        "5. Do not invent customers, demand, partners, commissions, prices, legal status or results.",
        "6. Do not purchase, pay, spam, sign or make external commercial commitments without explicit human authorization.",
        "",
        "Initial verdict: INSUFFICIENT EVIDENCE until the opportunity's claims are verified.",
        "Recommended next action: run the smallest zero-cost test that can disprove the weakest assumption."
      ].join("\n");

      return {
        content: [{ type: "text", text }],
        structuredContent: {
          opportunity,
          evidence,
          budget,
          verdict: "insufficient_evidence",
          next_action: "zero_cost_reversible_test"
        }
      };
    }
  );

  return server;
}

const app = express();
app.use(express.json({ limit: "1mb" }));
app.get("/health", (_req, res) => res.json({ ok: true, service: "ima-opportunity-mcp", version: "1.0.0" }));

app.all("/mcp", async (req, res) => {
  const server = createServer();
  const transport = new StreamableHTTPServerTransport({
    sessionIdGenerator: undefined
  });

  res.on("close", () => {
    transport.close().catch(() => {});
    server.close().catch(() => {});
  });

  try {
    await server.connect(transport);
    await transport.handleRequest(req, res, req.body);
  } catch (error) {
    if (!res.headersSent) res.status(500).json({ error: "MCP request failed" });
  }
});

app.listen(PORT, "0.0.0.0", () => {
  console.log(`IMA Opportunity MCP listening on :${PORT}`);
});
