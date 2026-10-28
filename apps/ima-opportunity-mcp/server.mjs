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
