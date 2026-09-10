import ganache from "ganache";
import { ethers } from "ethers";
import solc from "solc";

const TOKEN = `pragma solidity 0.8.19; contract IMAToken { string public name="IMA Token"; string public symbol="IMA"; uint public totalSupply=1000000; }`;
const GOV = `pragma solidity 0.8.19; contract IMAGovernance { address public token; constructor(address _t) { token = _t; } }`;

async function main() {
  // 1. מרים רשת לוקלית בזיכרון עם 10 ארנקים ו-10000 ETH
  const ganacheProvider = ganache.provider({ logging: { quiet: true } });
  const provider = new ethers.providers.Web3Provider(ganacheProvider);
  const wallet = provider.getSigner(0);
  
  console.log("Wallet:", await wallet.getAddress());

  // 2. קומפילציה
  const input = { language: "Solidity", sources: { "T.sol": {content: TOKEN}, "G.sol": {content: GOV} }, settings: { outputSelection: {"*": {"*": ["*"]} } } };
  const output = JSON.parse(solc.compile(JSON.stringify(input)));

  // 3. פורס טוקן
  const tokenFactory = new ethers.ContractFactory(output.contracts["T.sol"].IMAToken.abi, output.contracts["T.sol"].IMAToken.evm.bytecode.object, wallet);
  const token = await tokenFactory.deploy();
  await token.deployed();
  console.log("Token deployed to:", token.address);

  // 4. פורס גברננס
  const govFactory = new ethers.ContractFactory(output.contracts["G.sol"].IMAGovernance.abi, output.contracts["G.sol"].IMAGovernance.evm.bytecode.object, wallet);
  const gov = await govFactory.deploy(token.address);
  await gov.deployed();
  console.log("Governance deployed to:", gov.address);
  
  console.log("=== COUNCIL V4.2: LOCAL TESTNET LIVE ===");
}
main().catch(console.error);
