import { ethers } from "hardhat";

async function main() {
  const [wallet] = await ethers.getSigners();
  console.log("Wallet:", wallet.address);

  const Token = await ethers.getContractFactory("IMAToken");
  const token = await Token.deploy();
  await token.deployed();
  console.log("Token deployed to:", token.address);

  const Gov = await ethers.getContractFactory("IMAGovernance");
  const gov = await Gov.deploy(token.address);
  await gov.deployed();
  console.log("Governance deployed to:", gov.address);

  console.log("=== COUNCIL V4.2: LOCAL TESTNET LIVE ===");
}
main().catch(console.error);
