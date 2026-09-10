const crypto = require("crypto")

function idFor(value) {
    return crypto
        .createHash("sha256")
        .update(JSON.stringify(value))
        .digest("hex")
        .slice(0, 16)
}

function calculate(offer) {
    const buy = Number(offer.buy_price || 0)
    const sell = Number(offer.sell_price || 0)

    const shipping = Number(offer.shipping_cost || 0)
    const duty = Number(offer.duty_cost || 0)
    const platform = Number(offer.platform_fee || 0)
    const other = Number(offer.other_costs || 0)

    const total_cost =
        buy +
        shipping +
        duty +
        platform +
        other

    const profit = sell - total_cost

    const margin_pct =
        sell > 0
            ? (profit / sell) * 100
            : 0

    const roi_pct =
        total_cost > 0
            ? (profit / total_cost) * 100
            : 0

    return {
        ...offer,
        total_cost,
        profit,
        margin_pct,
        roi_pct,
        id: offer.id || idFor({
            product: offer.product,
            buy_source: offer.buy_source,
            sell_market: offer.sell_market,
            buy,
            sell
        }),
        status: profit > 0 ? "OPPORTUNITY" : "REJECTED"
    }
}

function rank(opportunity) {
    const confidence = Number(opportunity.confidence || 0)
    const freshness = Number(opportunity.freshness || 0)

    const score =
        Math.max(0, opportunity.margin_pct) * 0.5 +
        Math.max(0, opportunity.roi_pct) * 0.25 +
        confidence * 0.15 +
        freshness * 0.10

    return {
        ...opportunity,
        score
    }
}

function scan(offers = []) {
    return offers
        .map(calculate)
        .filter(x => x.status === "OPPORTUNITY")
        .map(rank)
        .sort((a, b) => b.score - a.score)
}

function createLead(opportunity) {
    return {
        type: "BROKER_LEAD",
        id: idFor({
            opportunity: opportunity.id,
            time: Date.now()
        }),
        opportunity_id: opportunity.id,
        product: opportunity.product,
        buy_source: opportunity.buy_source,
        sell_market: opportunity.sell_market,
        estimated_profit: opportunity.profit,
        margin_pct: opportunity.margin_pct,
        score: opportunity.score,
        action: "CONTACT_AND_VERIFY",
        automatic_purchase: false,
        automatic_payment: false,
        created_at: new Date().toISOString()
    }
}

function health() {
    return {
        status: "READY",
        mode: "READ_ONLY",
        automatic_purchase: false,
        automatic_payment: false
    }
}

module.exports = {
    calculate,
    rank,
    scan,
    createLead,
    health
}
