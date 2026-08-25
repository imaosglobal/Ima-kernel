// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;
contract Governance {
    struct Proposal { string description; uint votes; bool executed; }
    mapping(uint => Proposal) public proposals; mapping(address => mapping(uint => bool)) public voted;
    uint public proposalCount; address public treasury;
    event ProposalCreated(uint id, string desc); event Voted(uint id, address voter);
    modifier onlyTreasury() { require(msg.sender == treasury, "Not treasury"); _; }
    constructor(address _treasury) { treasury = _treasury; }
    function createProposal(string memory _desc) external onlyTreasury returns(uint) { proposals[proposalCount] = Proposal(_desc, 0, false); emit ProposalCreated(proposalCount, _desc); proposalCount++; return proposalCount - 1; }
    function vote(uint _id) external { require(!voted[msg.sender][_id], "Already voted"); proposals[_id].votes++; voted[msg.sender][_id] = true; emit Voted(_id, msg.sender); }
}
