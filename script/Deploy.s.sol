// SPDX-License-Identifier: MIT
pragma solidity 0.8.19;
import "forge-std/Script.sol";
import "../src/Token.sol";
import "../src/Gov.sol";

contract DeployScript is Script {
    function run() external {
        vm.startBroadcast();
        IMAToken token = new IMAToken();
        IMAGovernance gov = new IMAGovernance(address(token));
        console.log("Token deployed to:", address(token));
        console.log("Governance deployed to:", address(gov));
        console.log("=== COUNCIL V4.2: LOCAL TESTNET LIVE ===");
        vm.stopBroadcast();
    }
}
