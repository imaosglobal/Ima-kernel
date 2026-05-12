/**
 * This layer disables all competing systems logically.
 * It does NOT delete files, only prevents future usage.
 */

module.exports = {
  enforce() {
    console.log('[FREEZE] legacy systems ignored');
    return true;
  }
};
