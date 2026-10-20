"use strict";
const assert=require("node:assert/strict"),r=require("../kernel/runtime/CANONICAL/IMA_RELATIONAL_CARE");
assert.equal(r.verify().valid,true);assert.equal(r.contract().gender_neutral,true);assert.equal(r.contract().agency_preserved,true);assert.equal(r.contract().dependency_building,false);
const text=r.context();assert.match(text,/protection must not become ownership/);assert.match(text,/care must not manufacture dependency/);assert.match(text,/applies across genders, ages, cultures, relationships and interfaces/);assert.match(text,/A wing is not a cage/);
console.log("RELATIONAL_CARE_CONTRACT_OK");
