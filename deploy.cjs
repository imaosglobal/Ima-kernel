import { ThirdwebSDK } from "@thirdweb-dev/sdk";

async function main() {
  const sdk = new ThirdwebSDK("mumbai"); // TESTNET
  const governance = await sdk.deployGovernance({
    name: "IMA Governance",
    voting_token: "treasury.getAddress()",
  });
  console.log("Governance deployed to:", await governance.getAddress());
}
main();
