const goals = {
  maxResponseMs: 30,
  allowError: false,
  memoryGrowthLimit: 50
};

function evaluate(metrics) {
  let score = 0;

  if (metrics.avgResponse <= goals.maxResponseMs) {
    score += 1;
  }

  if (!metrics.error) {
    score += 1;
  }

  if (metrics.memoryGrowth <= goals.memoryGrowthLimit) {
    score += 1;
  }

  return {
    score,
    passed: score === 3
  };
}

module.exports = { goals, evaluate };
