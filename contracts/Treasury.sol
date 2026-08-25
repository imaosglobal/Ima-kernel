// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;
import "@openzeppelin/contracts/security/ReentrancyGuard.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
contract Treasury is ReentrancyGuard, Ownable {
    address[3] public owners; uint public required = 2;
    mapping(bytes32 => mapping(address => bool)) public approvals;
    bool public paused = false;
    mapping(bytes32 => uint) public timelocks; uint public constant TIMELOCK = 24 hours;
    address public vault70; address public impactDAO; address public growth10;
    event Split(uint amount, uint toVault, uint toImpact, uint toGrowth); event Paused(bool status);
    modifier onlyOwners() { require(isOwner(msg.sender), "Not owner"); _; }
    modifier whenNotPaused() { require(!paused, "Paused"); _; }
    constructor(address[3] memory _owners, address _vault, address _dao, address _growth) {
        owners = _owners; vault70 = _vault; impactDAO = _dao; growth10 = _growth; transferOwnership(_owners[0]);
    }
    function isOwner(address _addr) public view returns(bool) { for(uint i=0; i<3; i++) if(owners[i] == _addr) return true; return false; }
    function setPaused(bool _status) external onlyOwner { paused = _status; emit Paused(_status); }
    function deposit() external payable whenNotPaused nonReentrant {
        uint amount = msg.value; uint toVault = amount * 70 / 100; uint toImpact = amount * 20 / 100; uint toGrowth = amount - toVault - toImpact;
        (bool s1,)=vault70.call{value: toVault}(""); (bool s2,)=impactDAO.call{value: toImpact}(""); (bool s3,)=growth10.call{value: toGrowth}(""); require(s1 && s2 && s3, "Transfer failed");
        emit Split(amount, toVault, toImpact, toGrowth);
    }
}
