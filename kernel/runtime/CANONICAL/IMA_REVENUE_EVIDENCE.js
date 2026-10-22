"use strict";

function isVerifiedRevenue(event = {}) {
  return Boolean(
    event.event_id &&
    event.timestamp &&
    event.source &&
    event.provider &&
    event.currency &&
    Number.isFinite(Number(event.gross)) &&
    Number.isFinite(Number(event.net)) &&
    event.evidence &&
    event.payout_status === "RECEIVED"
  );
}

function normalize(event = {}) {
  const verified = isVerifiedRevenue(event);
  return {
    ...event,
    verified_revenue: verified,
    status: verified ? "VERIFIED" : "GAPS_RECORDED"
  };
}

module.exports = { isVerifiedRevenue, normalize };
