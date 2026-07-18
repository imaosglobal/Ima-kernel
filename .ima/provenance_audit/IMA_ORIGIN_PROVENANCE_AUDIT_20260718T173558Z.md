# IMA — Origin & Provenance Audit

- Audit time UTC: `2026-07-18T17:35:59.139159+00:00`
- Base: `/data/data/com.termux/files/home/ima_kernel`
- Mode: `READ_ONLY`
- Existing files modified: `NO`

## Verdict

**PROVENANCE_SYSTEM_PRESENT**

Score: **7/7 (100.0%)**

- [x] identity_or_origin_documented
- [x] canonical_authority_exists
- [x] git_history_exists
- [x] hash_or_integrity_artifacts_exist
- [x] timestamped_history_exists
- [x] historical_artifacts_exist
- [x] registries_exist

## Identity / Origin

Status: **FOUND**
Candidate files: 24
Files containing identity signals: 20

- `.ima/legacy/ori_legacy.before_identity_pattern.json` — Ori Cohen, IMA, creator, vision, creator, חזון
- `.ima/runtime_snapshots/product_before_finalize_20260713_165823/product/identity/identity_registry.json` — IMA
- `.ima/archive_final/ima_backup_1783804250/.ima/legacy/ori_legacy.before_identity_pattern.json` — Ori Cohen, IMA, creator, vision, creator, חזון
- `.ima/archive_final/backups/ima_1783804993/legacy/ori_legacy.before_identity_pattern.json` — Ori Cohen, IMA, creator, vision, creator, חזון
- `.ima/legacy/ori_legacy.json` — Ori Cohen, IMA, creator, vision, creator, חזון
- `.ima/legacy/ori_legacy.locked.json` — Ori Cohen, IMA, creator, vision, creator, חזון
- `.ima/legacy/ori_legacy.backup.json` — Ori Cohen, IMA, creator, creator, חזון
- `.ima/archive_final/ima_backup_1783804250/.ima/legacy/ori_legacy.json` — Ori Cohen, IMA, creator, vision, creator, חזון
- `.ima/archive_final/ima_backup_1783804250/.ima/legacy/ori_legacy.locked.json` — Ori Cohen, IMA, creator, vision, creator, חזון
- `.ima/archive_final/ima_backup_1783804250/.ima/legacy/ori_legacy.backup.json` — Ori Cohen, IMA, creator, creator, חזון
- `.ima/archive_final/backups/ima_1783804993/legacy/ori_legacy.json` — Ori Cohen, IMA, creator, vision, creator, חזון
- `.ima/archive_final/backups/ima_1783804993/legacy/ori_legacy.locked.json` — Ori Cohen, IMA, creator, vision, creator, חזון
- `.ima/archive_final/backups/ima_1783804993/legacy/ori_legacy.backup.json` — Ori Cohen, IMA, creator, creator, חזון
- `docs/vision.md` — IMA, vision
- `.ima/vision_governance_backups/20260718_175920/docs/vision.md` — IMA, vision
- `deployment/cloud_manifest.json` — IMA
- `kernel/_legacy_releases/v1778001671191/manifest.json` — IMA
- `ima-ui/public/manifest.json` — IMA
- `.ima/runtime/canonical_manifest.json` — IMA
- `.ima/releases/canonical/canonical_manifest.json` — IMA

## Canonical Authority

Exists: **True**
Files: **114**

## Git Provenance

Repository: **True**

### Remote

```
ima_core_backup	/data/data/com.termux/files/home/kernel/projects/ima_core (fetch)
ima_core_backup	/data/data/com.termux/files/home/kernel/projects/ima_core (push)
origin	https://github.com/imaosglobal/Ima-kernel.git (fetch)
origin	https://github.com/imaosglobal/Ima-kernel.git (push)

```

### First Commit

```
0bfa36d8b542804f1c392557a4a373d534c0f2e5
17bdeba272f900fb6012fc99384791051d212251

```

### Recent History

```
5dd8bec2ffe788eb5957422c5c517a4604f6d1b9|2026-07-18T13:50:32+03:00|Ori Cohen|imaosglobal@gmail.com/|baseline: working IMA API with brain connected
2c5fc132fba98968fa079c48465ce2868d7ca7a2|2026-07-17T06:32:36+03:00|Ori Cohen|imaosglobal@gmail.com/|IMA autonomous evolution checkpoint 2026-07-17_06-15-24
1e765e054af91b3199b2613ddcb56563d9b8368f|2026-07-17T03:06:30+03:00|Ori Cohen|imaosglobal@gmail.com/|Update AGI runtime evaluation state
132c587c52ca11a1de6b8228ce643983d20f85f2|2026-07-17T03:05:33+03:00|Ori Cohen|imaosglobal@gmail.com/|Fix AGI benchmark lifecycle execution path
c13a5c8f35e09b48afce9c5e51871533d6e99ac5|2026-07-17T03:02:54+03:00|Ori Cohen|imaosglobal@gmail.com/|Connect AGI benchmark into canonical evolution lifecycle
9fece6a7fa14abd3d71ca83f3ebfa252e9711857|2026-07-17T02:54:24+03:00|Ori Cohen|imaosglobal@gmail.com/|Register cognitive pipeline in canonical runtime
bd93dae370ab760015480f3eeface36aaa0e760f|2026-07-17T02:52:22+03:00|Ori Cohen|imaosglobal@gmail.com/|Connect cognitive pipeline to canonical lifecycle
3c9cb6463cac1dafcfd795d6d831761a07767702|2026-07-17T02:38:11+03:00|Ori Cohen|imaosglobal@gmail.com/|Add global canonical chain verification
1594b02d2e1c5f843439df8b89adf6280d62e5b6|2026-07-17T02:35:11+03:00|Ori Cohen|imaosglobal@gmail.com/|Add canonical component admission guard
f05cc85860bef30067ef085a010c7e9e309b5527|2026-07-17T02:31:09+03:00|Ori Cohen|imaosglobal@gmail.com/|Update canonical registry hashes
6ff9c3c04b63ae7e8a1d8cc24f33d74cb60e11a5|2026-07-17T02:29:45+03:00|Ori Cohen|imaosglobal@gmail.com/|Enforce canonical registry in boot gate
b6b4c06be3f10c736392599b63c4bf4c1dd1c257|2026-07-16T21:41:50+03:00|Ori Cohen|imaosglobal@gmail.com/|Add global canonical guard for Termux and future entry points
ba3dbc7f68f883e03ffef6f6210505b2ffab8587|2026-07-16T21:40:35+03:00|Ori Cohen|imaosglobal@gmail.com/|Update canonical registry hash after guard enforcement
171628cef51774404021d3473fffa9bc181f6bbc|2026-07-16T21:39:42+03:00|Ori Cohen|imaosglobal@gmail.com/|Enforce canonical registry at boot
1c9e11d5e39a4f9d2f20cf533662488ed6a67a50|2026-07-16T21:38:01+03:00|Ori Cohen|imaosglobal@gmail.com/|Create canonical component registry
de8552672d7c9883fb404dfcf6f7002064a7c328|2026-07-16T21:37:51+03:00|Ori Cohen|imaosglobal@gmail.com/|Create canonical component registry
84d3dc7939d36c3cd77450936c4fd04972f0a5c3|2026-07-16T21:36:58+03:00|Ori Cohen|imaosglobal@gmail.com/|Remove tracked runtime state files from version control
b7be1c26f5a3de2fe690d5c105ed8b42b9b88deb|2026-07-16T21:36:20+03:00|Ori Cohen|imaosglobal@gmail.com/|Ignore dynamic runtime state files
c64d26789cccbf2b20b9ff86b349ded5665b1624|2026-07-16T21:35:13+03:00|Ori Cohen|imaosglobal@gmail.com/|Finalize canonical runtime hardening
a9eed55e0c37dc637961a04f58123da26e2ee267|2026-07-16T21:33:43+03:00|Ori Cohen|imaosglobal@gmail.com/|Enforce canonical kernel policy at single entry
c26a9804a9e83738e0c232afcd9eddd7cceab358|2026-07-16T21:32:37+03:00|Ori Cohen|imaosglobal@gmail.com/|Harden canonical runtime with hash enforcement policy
018f31d13d906cefd914cf64044aa5fc64df721e|2026-07-16T21:29:25+03:00|Ori Cohen|imaosglobal@gmail.com/|Enforce canonical kernel access gate
d1e10765576dcfd42ffc2d09dd62ec250cc59358|2026-07-16T21:28:27+03:00|Ori Cohen|imaosglobal@gmail.com/|Ignore runtime state files
419b1726296a308f85d9304bcd97a2870f539ca7|2026-07-16T21:26:26+03:00|Ori Cohen|imaosglobal@gmail.com/|IMA single entry canonical runtime baseline
7fc99d750966983be3b1ac873b1531c089cf0d16|2026-07-16T21:24:08+03:00|Ori Cohen|imaosglobal@gmail.com/|Lock canonical kernel bridge
60b5e929f94be1d601b4eefe794bb9157c00bd46|2026-07-16T21:19:11+03:00|Ori Cohen|imaosglobal@gmail.com/|IMA real canonical kernel selector v2
c378af626c0d35fd272cdd601729c661b6b3cefe|2026-07-16T21:18:28+03:00|Ori Cohen|imaosglobal@gmail.com/|IMA real kernel handoff to master runtime
a254bfa41fd6975d2225cb2278b76ee49ed1c8ae|2026-07-16T21:17:52+03:00|Ori Cohen|imaosglobal@gmail.com/|IMA canonical kernel selector cleanup
780abd8112852cf631c82f52f7c9d6813a4c90e3|2026-07-16T21:14:34+03:00|Ori Cohen|imaosglobal@gmail.com/|IMA boot gate single entry layer
433fde928c48d1404de70568dad597638293cad4|2026-07-16T21:12:51+03:00|Ori Cohen|imaosglobal@gmail.com/|IMA kernel bridge integration
5d52aa8fdab7ec29572f5de06f39fdfe26f977e4|2026-07-16T21:11:28+03:00|Ori Cohen|imaosglobal@gmail.com/|IMA master lifecycle integration
cc980ea143142871e9834fb29a010910c9fadecd|2026-07-16T21:01:41+03:00|Ori Cohen|imaosglobal@gmail.com/|IMA autonomous evolution checkpoint 2026-07-16_21-01-36
63fd0c1fca76771c05e43884d780e9e14de7ac86|2026-07-16T19:45:37+03:00|Ori Cohen|imaosglobal@gmail.com/|fix FounderCore advisor integration
940fa76f052ef03b169b62569df01d06aada0134|2026-07-16T19:44:57+03:00|Ori Cohen|imaosglobal@gmail.com/|fix FounderCore memory bridge integration
a1de9a72f1899da235ac1eb5ad394a9d49405457|2026-07-16T19:43:25+03:00|Ori Cohen|imaosglobal@gmail.com/|create FounderCore orchestration layer
de083badc037af5a330bb66f4736041d7607150d|2026-07-16T19:36:24+03:00|Ori Cohen|imaosglobal@gmail.com/|guardian real release gate stop empty releases
0662a26fe7f3074fb30524de05596e540eeabf5e|2026-07-16T19:35:28+03:00|Ori Cohen|imaosglobal@gmail.com/|guardian release tag gate protection
77fcf4b0a17e27b9cd502ead0a5d67209adc0add|2026-07-16T19:34:52+03:00|Ori Cohen|imaosglobal@gmail.com/|guardian release pipeline handle clean working tree
3a85be422594abd50134502b2c26527e2ab53187|2026-07-16T19:34:15+03:00|Ori Cohen|imaosglobal@gmail.com/|guardian full audit moved to nightly schedule
e57f5980a140ced201fcc466a2ebbb0479c3f11e|2026-07-16T19:33:15+03:00|Ori Cohen|imaosglobal@gmail.com/|IMA automatic guarded commit 2026-07-16T19:33:15.141845
05fe527529d408c277371a097b7821ec413530d6|2026-07-16T19:32:05+03:00|Ori Cohen|imaosglobal@gmail.com/|add automatic guarded release pipeline
cbb1a3186610ce9153a0283489ede499415f9f61|2026-07-16T19:29:24+03:00|Ori Cohen|imaosglobal@gmail.com/|add guardian regression verification
3b9ad3626b490ba18d613c6d1c380e797a42ec84|2026-07-16T19:27:17+03:00|Ori Cohen|imaosglobal@gmail.com/|guardian audit baseline syntax clean
24821912e2be10a5720a5e9e512d5790a66f6797|2026-07-16T19:24:36+03:00|Ori Cohen|imaosglobal@gmail.com/|guardian connect automatic snapshot restore check
ba074e3ef6768ac95e0a511d245cec53fd155a07|2026-07-16T19:23:56+03:00|Ori Cohen|imaosglobal@gmail.com/|guardian add core snapshot restore mechanism
d710a33d40dc1f13706443b5bcaeb0efb670777e|2026-07-16T19:23:22+03:00|Ori Cohen|imaosglobal@gmail.com/|guardian create protected core snapshot
f461175aa7abaaf4a3c7a8debedc6c2ddc7c10f3|2026-07-16T19:22:48+03:00|Ori Cohen|imaosglobal@gmail.com/|guardian core self protection layer
9002b47f3fb5076dd63acaf5e118505dc55c193d|2026-07-16T19:21:58+03:00|Ori Cohen|imaosglobal@gmail.com/|guardian policy lock and protection gate
90d7908922ba672fb9d64313a85f70b1cc99d28f|2026-07-16T19:20:22+03:00|Ori Cohen|imaosglobal@gmail.com/|guardian stop master after successful incremental check
0f16c1fbc484ac4394bb171e1380ccf0ec07f8e9|2026-07-16T19:19:23+03:00|Ori Cohen|imaosglobal@gmail.com/|guardian skip master when target verification passes
edc4f92b70a3b99d8e153f2bd2eb1f98d01957f4|2026-07-16T19:18:37+03:00|Ori Cohen|imaosglobal@gmail.com/|guardian-master-after
6a9c950c8ec7c4774a2c720bdff098cfc39e6a6e|2026-07-16T19:18:36+03:00|Ori Cohen|imaosglobal@gmail.com/|guardian-after-cycle
5cc72281fd322309e44c7012162d1e89410c57b6|2026-07-16T19:18:36+03:00|Ori Cohen|imaosglobal@gmail.com/|guardian-before-cycle
b339203b9f57d6acaee93de5f1f6db1e43190576|2026-07-16T19:18:35+03:00|Ori Cohen|imaosglobal@gmail.com/|guardian-master-before
2e383ce3fea46df386b4b1193d2de0e577702294|2026-07-16T19:17:57+03:00|Ori Cohen|imaosglobal@gmail.com/|guardian connect target compile repair flow
be0e700cef11371729ee7f8c0f5dac6090d45f76|2026-07-16T19:17:24+03:00|Ori Cohen|imaosglobal@gmail.com/|guardian add target only compile verification
be86468130b3978806f0ce42fd1f0c4a1ad1a468|2026-07-16T19:16:42+03:00|Ori Cohen|imaosglobal@gmail.com/|guardian replace mtime scanner with git diff engine
955b0b1dbb4897ad313b93413b7967961b373e40|2026-07-16T19:15:45+03:00|Ori Cohen|imaosglobal@gmail.com/|guardian-master-after
e8d5c7d656907b719968b6f0c2844d0adbdbd30a|2026-07-16T19:15:44+03:00|Ori Cohen|imaosglobal@gmail.com/|guardian-before-cycle
fbb860ea495b07675cb96ad85f529551a3f98593|2026-07-16T19:15:44+03:00|Ori Cohen|imaosglobal@gmail.com/|guardian-master-before
785e7f914cbece837c858fb1af764cbc53eb507b|2026-07-16T19:15:36+03:00|Ori Cohen|imaosglobal@gmail.com/|guardian incremental cycle return status
12beb36dd26d50d64b9527779ff76509b442aa48|2026-07-16T19:15:13+03:00|Ori Cohen|imaosglobal@gmail.com/|guardian-master-after
0e1d213c7b5d61307518f061c4cafd0d6cab7fd1|2026-07-16T19:15:12+03:00|Ori Cohen|imaosglobal@gmail.com/|guardian-before-cycle
9b20514ee6dd5a758322fc375c86b34b5f0bec1f|2026-07-16T19:15:12+03:00|Ori Cohen|imaosglobal@gmail.com/|guardian-master-before
def1f294d4c8a090cbf84106c32b13e482970229|2026-07-16T19:15:04+03:00|Ori Cohen|imaosglobal@gmail.com/|guardian smart gate skip unnecessary master cycles
5f4cd09c850cf23a7853c0676f8ca9143352325c|2026-07-16T19:14:26+03:00|Ori Cohen|imaosglobal@gmail.com/|guardian-master-after
91b7dec260fec95be7c2f9661b483956b04a1124|2026-07-16T19:14:25+03:00|Ori Cohen|imaosglobal@gmail.com/|guardian-before-cycle
f26e26c3c36b827bac6b5dee78a0d59a38cfe7d7|2026-07-16T19:14:25+03:00|Ori Cohen|imaosglobal@gmail.com/|guardian-master-before
c47131063cf552bbd56b068abfc482b6f943b0a2|2026-07-16T19:14:22+03:00|Ori Cohen|imaosglobal@gmail.com/|fix guardian incremental json dependency
a3e72b7194c61db2744335fb6bf92795806acd91|2026-07-16T19:13:52+03:00|Ori Cohen|imaosglobal@gmail.com/|guardian-master-after
38e29c40847f18f340dbda8c72b27f5b732c38de|2026-07-16T19:13:51+03:00|Ori Cohen|imaosglobal@gmail.com/|guardian-before-cycle
c1c54357028db167c7b5c06badfd9217ccc7209b|2026-07-16T19:13:43+03:00|Ori Cohen|imaosglobal@gmail.com/|connect incremental cycle directly into guardian watch
572fca37e710ec0b8c34f7f3b9a870e9ccafd1b8|2026-07-16T19:12:41+03:00|Ori Cohen|imaosglobal@gmail.com/|guardian-master-after
af8dc2688214f676f75388db0a4d08eee1ac5451|2026-07-16T19:12:40+03:00|Ori Cohen|imaosglobal@gmail.com/|guardian-before-cycle
711efbd14bd6588083a1c9283d4586c3da451b0a|2026-07-16T19:12:33+03:00|Ori Cohen|imaosglobal@gmail.com/|connect incremental guardian into watch cycle
c23f3cd6261aa6068cb8a66592e0f8819beafa37|2026-07-16T19:11:54+03:00|Ori Cohen|imaosglobal@gmail.com/|guardian-master-after
8eac7c7e2b7eb72d02c515599bbb14a792e0dae3|2026-07-16T19:11:53+03:00|Ori Cohen|imaosglobal@gmail.com/|guardian-before-cycle
745c33ea2a252483aa35980fdf09f8d982fa9db0|2026-07-16T19:11:38+03:00|Ori Cohen|imaosglobal@gmail.com/|guardian incremental changed files verification
62559f472c01204ef6fde97408aad4ba74ff5029|2026-07-16T19:10:14+03:00|Ori Cohen|imaosglobal@gmail.com/|guardian-master-after
e00bdf94a2f943b389e4e932d9aed6ad01b4714c|2026-07-16T19:10:13+03:00|Ori Cohen|imaosglobal@gmail.com/|guardian-before-cycle
d2586cad8064b30bf14d0be28e7d1db8615dbff9|2026-07-16T19:10:13+03:00|Ori Cohen|imaosglobal@gmail.com/|guardian-master-before
4b92a3deee06c7cb03fd8b6583bb4a3399930138|2026-07-16T19:09:03+03:00|Ori Cohen|imaosglobal@gmail.com/|guardian robust syntax block repair
8c712772f4881c9b67c393ae45826369d23936bc|2026-07-16T19:04:28+03:00|Ori Cohen|imaosglobal@gmail.com/|guardian auto cycle repair syntax errors
396d6369f6025825290488c9e07c88416d3d56f4|2026-07-16T19:03:27+03:00|Ori Cohen|imaosglobal@gmail.com/|guardian-master-after
fe89e7eed1352a1300b4e72ec4b66272440af6f8|2026-07-16T19:03:26+03:00|Ori Cohen|imaosglobal@gmail.com/|guardian-before-cycle
9b582475bb838798f38962cf1eba0469e8586f07|2026-07-16T19:03:26+03:00|Ori Cohen|imaosglobal@gmail.com/|guardian-master-before
99c125bdb9619699d2ea4901736ce9353997b1b5|2026-07-16T19:03:26+03:00|Ori Cohen|imaosglobal@gmail.com/|guardian add unterminated string repair handler
7f7fbbb9cb74687b3357a7a9510da03581f086f5|2026-07-16T18:57:35+03:00|Ori Cohen|imaosglobal@gmail.com/|guardian-master-after
3eeb339d8e42e1c2a6965fafce3456c696c288b1|2026-07-16T18:57:34+03:00|Ori Cohen|imaosglobal@gmail.com/|guardian-before-cycle
954b1d2f21ee0e227623fa460533ceb532f11e27|2026-07-16T18:57:27+03:00|Ori Cohen|imaosglobal@gmail.com/|guardian report driven fast repair pipeline
956e60bffb3768db72b2f34f262231c25137b9ed|2026-07-16T18:53:35+03:00|Ori Cohen|imaosglobal@gmail.com/|repair daily evolution syntax error
676a83119e1ff6474cca6c1d7b318ba84b6e8bc2|2026-07-16T18:53:05+03:00|Ori Cohen|imaosglobal@gmail.com/|guardian fast repair and audit exclusions
0a56c201ba4a37992a9face0badc4afe125cbeb4|2026-07-16T18:50:27+03:00|Ori Cohen|imaosglobal@gmail.com/|guardian-after-cycle
12121174215f4bba74f07d1ef1f4d351ad8a6d7d|2026-07-16T18:49:28+03:00|Ori Cohen|imaosglobal@gmail.com/|guardian-before-cycle
bcf441b138ffefbf4f1b33a6e7fa57797c27df24|2026-07-16T18:49:28+03:00|Ori Cohen|imaosglobal@gmail.com/|guardian-master-after
e0026c24b28620365181c82fed611db12f74ddb5|2026-07-16T18:49:27+03:00|Ori Cohen|imaosglobal@gmail.com/|guardian-after-cycle
2fec9878fd532a37dba1698d0053d05471fcb546|2026-07-16T18:48:26+03:00|Ori Cohen|imaosglobal@gmail.com/|guardian-before-cycle
e3f77181790ce2dd7bb3735ae5db2c864fa556f7|2026-07-16T18:47:44+03:00|Ori Cohen|imaosglobal@gmail.com/|guardian-master-after
2a9fc148e8400aa66b9c7da19d5f7fe7547ffafe|2026-07-16T18:47:44+03:00|Ori Cohen|imaosglobal@gmail.com/|guardian-after-cycle
f84f86b45e51d798a55cb8c4f6fe15499f6c4969|2026-07-16T18:46:40+03:00|Ori Cohen|imaosglobal@gmail.com/|guardian-before-cycle
```

## Cryptographic / Integrity Evidence

Candidate artifacts: **116**

- `.ima/releases/render_activation/20260713_175739/HASHES.sha256` — SHA256 `86771b0dac85d13a05dcd915792decc87a1b230d2b1c3db4985b58a59c451862`
- `.ima/releases/external_release/20260713_175434/HASHES.sha256` — SHA256 `b55fa59e961026e5232bc024468d2d4adcf9bd9ff83e2dc7c768f1ca0fba365b`
- `.ima/releases/candidates/IMA_RC_MANIFEST.sha256` — SHA256 `6b7fb6ab63341442d68bd73e1a7058082ac7e5ed709ebd27b434ca16460a141b`
- `.ima/releases/integrity_seals/product_hashes.sha256` — SHA256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `.ima/releases/final_release/IMA_FINAL_RELEASE.sha256` — SHA256 `9231270429a0173a85b1dc9041e78a8b9b8c45d36478cd3aec896157ab1c10d6`
- `.ima/releases/master_manifest/IMA_PRODUCTION_RELEASE_MANIFEST.sha256` — SHA256 `f438623e0ead648ea5d7dc9f5dbf9935982df4f5ce42abab7ea034ad737833eb`
- `.ima/releases/deployment_provider/20260713_175248/DEPLOYMENT_PROVIDER_MANIFEST.sha256` — SHA256 `535b8d4fa9df5e35e776f69f3d9f8d1610847aa98c5c4468b0ef7657b2dc0058`
- `.ima/releases/production_infrastructure/20260713_175130/PRODUCTION_INFRASTRUCTURE.sha256` — SHA256 `00b37e4c4c54025b6a3458ffe3863ab4ae860199f315826b3ae5c48aa7d12491`
- `.ima/releases/full_pipeline/20260713_175007/FULL_RELEASE_STATUS.sha256` — SHA256 `1e5b8e3e3c8e1dc9c72a649c9117cfef1b1ea715817dcbd0f5dfb5d9a2893caf`
- `.ima/releases/service_contract/20260713_174825/SERVICE_CONTRACT.sha256` — SHA256 `af33f2b1c71cb827129dda2b333f881a2c11b29452a8424a48b0784b495461dc`
- `.ima/releases/production_environment/20260713_174656/PRODUCTION_ENVIRONMENT.sha256` — SHA256 `4f4af9ca00d72ecc202961f8cf643e2216ab75d5c381d1307df396b2734a58d8`
- `.ima/releases/production_archive/20260713_174401/RELEASE_HASHES.sha256` — SHA256 `8dc08ff5e359c81b411326f68886928fc80b32e0cedcd0fe2e2541196bfb3fdd`
- `.ima/releases/distribution_bundle/20260713_174152/BUILD_HASHES.sha256` — SHA256 `df0f7c01ad6cd390a2d9fb692e64bd95dfc8d6d6e850d4303ee72c95ec1a9665`
- `.ima/releases/distribution_bundle/20260713_174152/RELEASE_DISTRIBUTION_BUNDLE.sha256` — SHA256 `4dd7e79f7fa3e919973695eceefbe2bbe02ac38dcf00d7bb97bb2fcffdadb76b`
- `.ima/releases/build_artifacts/20260713_174117/BUILD_HASHES.sha256` — SHA256 `df0f7c01ad6cd390a2d9fb692e64bd95dfc8d6d6e850d4303ee72c95ec1a9665`
- `.ima/releases/distribution_targets/20260713_174047/TARGET_REGISTRY.sha256` — SHA256 `344f4da277bc2bedaa6a00384708a6e64b36da75d0da2e5c88888dc041787d2d`
- `.ima/releases/deployment_gateway/20260713_174002/DEPLOYMENT_GATEWAY.sha256` — SHA256 `3f27facccf83cb252e71227e567c18b6a666a556397622ad81c3ea5f7bbdb34c`
- `.ima/releases/snapshots/20260713_173919/SNAPSHOT.sha256` — SHA256 `78955d6ae90e66b676229538c4ad726cc52dcb2e71ee05f08afddef37ba5e9eb`
- `.ima/releases/artifacts/20260713_173650/ARTIFACT_REGISTRY.sha256` — SHA256 `0352cefba8f9bce7aa8af1835254238e60ecc72ea3a0b254471e41d65a08d9ca`
- `.ima/releases/packages/IMA_RC1_20260713_172508/IMA_RC_MANIFEST.sha256` — SHA256 `6b7fb6ab63341442d68bd73e1a7058082ac7e5ed709ebd27b434ca16460a141b`
- `.ima/releases/packages/IMA_RC1_20260713_172508/RELEASE_PACKAGE.sha256` — SHA256 `333f6cbbc9d5dfeeaf742c829a8814c2342f9593c2d1a6923df68a8eccfcb9b3`
- `.ima/releases/distribution/20260713_172230/DISTRIBUTION_HASH.sha256` — SHA256 `6e67d6a60a38cbe6cc1a2c1932efe9c04a3a118eb38b3f51303f39d6ad1dca13`
- `.ima/releases/integrity_seals/20260713_172053/core_hashes.sha256` — SHA256 `c2f1da26ba78c566de23528aae49368c02c8c006d9594a63f4a35a9b15cdcb70`
- `.ima/releases/integrity_seals/20260713_172053/product_hashes.sha256` — SHA256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `.ima/releases/integrity_seals/20260713_172130/core_hashes.sha256` — SHA256 `c2f1da26ba78c566de23528aae49368c02c8c006d9594a63f4a35a9b15cdcb70`
- `.ima/releases/integrity_seals/20260713_172130/product_hashes.sha256` — SHA256 `c23632a8fae7cb6d116d967733a9602be22b9d246895599f727ee4cffeb05dcd`
- `.ima/healthy_master_hashes.txt` — SHA256 `06405580edccc9c9afe76811f93b7125d70fdcd28f0f684e505dde45443dcd13`
- `.ima/master_integrity.json` — SHA256 `083201f387fb23d4176aa067b56e962603614d999de644f37fbf9a5477cee6a4`
- `.ima/runtime/boot_integrity_report.json` — SHA256 `651ebc73ab3b09e7e89b62c4a4738baa38757f9af75ce4c6718b03d611057575`
- `.ima/canonical_chain_audit.json` — SHA256 `3a372dc6b8d4f6dbe07c7fa0cc3a95375affc889942ee667b47be306d69b09ca`
- `.ima/CANONICAL_AUTHORITY/canonical_chain_audit.json` — SHA256 `6faea978b675a78096e94257485b52bcf42a52154a5526ac6663d639dceabbee`
- `.ima/CANONICAL_AUTHORITY/evolution/SELF_EVOLUTION/CANONICAL_CHAIN_ORCHESTRATOR/canonical_chain_audit_1784384204.json` — SHA256 `2d8eea5eade3eb48493647305a166811f1b33bca2a0d136c3693e9d08309294d`
- `.ima/CANONICAL_AUTHORITY/evolution/SELF_EVOLUTION/CANONICAL_CHAIN_ORCHESTRATOR/canonical_chain_audit_1784384287.json` — SHA256 `dfeacd5e8eb2ac329e94826d50029c3ce647464db5847ddd77d0f7a2117204c8`
- `.ima/CANONICAL_AUTHORITY/evolution/SELF_EVOLUTION/CANONICAL_CHAIN_ORCHESTRATOR/canonical_chain_audit_1784384323.json` — SHA256 `319544f844bc2b02ccdb39aefea0cb3d704512d217880aecb2988a27292cde61`
- `.ima/CANONICAL_AUTHORITY/evolution/SELF_EVOLUTION/CANONICAL_CHAIN_ORCHESTRATOR/canonical_chain_audit_1784384429.json` — SHA256 `1f6c8fbc42ea65a3a29ea318230096393f3fb1ee3d84041547aa7378c11a9cb7`
- `.ima/CANONICAL_AUTHORITY/evolution/SELF_EVOLUTION/CANONICAL_CHAIN_ORCHESTRATOR/canonical_chain_audit_1784384483.json` — SHA256 `cf1fcc2ed0648d9b77c37d57b10923eaa42b26ea49bd33ae7da7788ebba7d9e1`
- `.ima/CANONICAL_AUTHORITY/evolution/SELF_EVOLUTION/CANONICAL_CHAIN_ORCHESTRATOR/canonical_chain_audit_1784384694.json` — SHA256 `87b7f7f427ac110368afe778a97fb081ad924f2b602c239ec659e941333e7fe9`
- `.ima/CANONICAL_AUTHORITY/evolution/SELF_EVOLUTION/CANONICAL_CHAIN_ORCHESTRATOR/canonical_chain_audit_1784384948.json` — SHA256 `51410e1e4cb37e669dfe6e1e0297453afe72eaa6b823d23549b38c5eaffb945b`
- `.ima/CANONICAL_AUTHORITY/evolution/SELF_EVOLUTION/CANONICAL_CHAIN_ORCHESTRATOR/canonical_chain_audit_1784385012.json` — SHA256 `ff7874f992c6d833642210364e62b0293f84be358e6bd17b9474c35173f8018e`
- `.ima/CANONICAL_AUTHORITY/evolution/SELF_EVOLUTION/CANONICAL_CHAIN_ORCHESTRATOR/canonical_chain_audit_1784385318.json` — SHA256 `b30219cc0dd0b853e91e6589529fed1f41b3c4ab24298342aae8b83b0d48b3c9`
- `.ima/CANONICAL_AUTHORITY/evolution/SELF_EVOLUTION/CANONICAL_CHAIN_ORCHESTRATOR/canonical_chain_audit_1784385621.json` — SHA256 `3af1ae1c79448c744e8961a87410d9fb7737cc7a3cef3381cc90db091ca21a26`
- `.ima/CANONICAL_AUTHORITY/evolution/SELF_EVOLUTION/CANONICAL_CHAIN_ORCHESTRATOR/canonical_chain_audit_1784385927.json` — SHA256 `607f2ac9810695b323ab015514ad0f34fc267a25fe41c72597a263cfdd31e695`
- `.ima/CANONICAL_AUTHORITY/evolution/SELF_EVOLUTION/CANONICAL_CHAIN_ORCHESTRATOR/canonical_chain_audit_1784386237.json` — SHA256 `3b67ad3fcca7760cec2eb86ac55625e102c26ab05fdedeaa054e63118b0aee26`
- `.ima/CANONICAL_AUTHORITY/evolution/SELF_EVOLUTION/CANONICAL_CHAIN_ORCHESTRATOR/canonical_chain_audit_1784386538.json` — SHA256 `5266ec090ddecf24b3152ea29f447d2a81e42cf13eb369a6befacb8972f83774`
- `.ima/CANONICAL_AUTHORITY/evolution/SELF_EVOLUTION/CANONICAL_CHAIN_ORCHESTRATOR/canonical_chain_audit_1784386839.json` — SHA256 `708dba79270d44d400fe2eb578367c7d26336aa0046f89c2a70ccb6323abb09b`
- `.ima/CANONICAL_AUTHORITY/evolution/SELF_EVOLUTION/CANONICAL_CHAIN_ORCHESTRATOR/canonical_chain_audit_1784387157.json` — SHA256 `59054ee59cf5d4aa2c945b2a08fd0fdf7d214b4fc22f592d5a905a555aeaceda`
- `.ima/CANONICAL_AUTHORITY/evolution/SELF_EVOLUTION/CANONICAL_CHAIN_ORCHESTRATOR/canonical_chain_audit_1784387860.json` — SHA256 `8377c62ce1e3ac6a655cc2560a7c171bd514037a69ff2c19aa4f216b33ee00a1`
- `.ima/fusion_lock.json` — SHA256 `9f6acfe06e28aee562638844a86aa18debdfd746f04645da5dd3c5436cfde0b8`
- `.ima/final_fusion_lock.json` — SHA256 `de7feee62762607c6ae7caa92262c5d11f5d493a7758d703fd9c367e06774c6b`
- `.ima/governance/orchestrator_lock.json` — SHA256 `6ac4a75f946e478a70eba15af782b85a4f9da44b62542c9d39e707f38da11c2f`
- `.ima/governance/service_layer_lock.json` — SHA256 `06e19a6fbb0e93f3fe4c132b7122269307791336aff02f31d2cc088e587b473a`
- `.ima/governance/product_layer_lock.json` — SHA256 `e012cbcefeb058911576d7c3b26152bbad2c1643aa0b6043616ee9e60331855a`
- `.ima/governance/final_orchestrator_lock.json` — SHA256 `29fd2289a9f1a0263da22843261addfdab547ac612584369ddb9a7c634465abb`
- `.ima/governance/architecture_lock_report.json` — SHA256 `a339ed4137b12ac4217e9d567806c8059e27f9d032525b5e013015dfb6b398cf`
- `.ima/governance/entry_gate_lock.json` — SHA256 `2049cacccd25f100ab239ca67a1672a1416f35f6333c31aa20c697a1bf3c0ed1`
- `.ima/governance/architecture_lock.json` — SHA256 `7fa4eb72efb0dbba2f51f970be3c1e17551d0d44febff16ade88615205236246`
- `.ima/governance/final_audit_lock.json` — SHA256 `7e1137b751d15759933f053442779167870613e71a2dff981be1869c1a655573`
- `.ima/governance/final_governance_lock.json` — SHA256 `c219be53ee82c02e92e1319cc7c282b8ab32d7ae2282efc70ee54886cf0f2271`
- `.ima/legacy/ori_legacy.locked.json` — SHA256 `68edd94a6cf8f9d7aadc14000cf7f9dd3ed87526850e9b64f506e3a810047e02`
- `.ima/runtime/system_integration_lock.json` — SHA256 `ea0b15b38eaaea4d6f0112fb74713a63993e735f10f7066ac670294ae3a0afd3`
- `.ima/runtime/full_system_lock.json` — SHA256 `7ec22bc84c93471e32b8e882a6198bba676a547c416660b50c004a6e2ca49e4a`
- `.ima/runtime/api_boot_lock.json` — SHA256 `557292b6950415d86678e27ca47f5bd9ef57704ee06c822f63d3054b2eb79e95`
- `.ima/runtime/canonical_system_lock.json` — SHA256 `9294d92dff026fc80999ba9f3e95cc764e147bd4407bf502356826e31963cd73`
- `.ima/runtime/canonical_fusion_lock.json` — SHA256 `739c22ab5c4febfd485180212dc88a11fb3142db887b511ca2fa4a3191d17565`
- `.ima/runtime/baseline_lock.json` — SHA256 `d1f8fffb18ba13bd1fa983bf0178570107223e5f404e5b13efabc8617c56fdae`
- `.ima/vision_governance_backups/20260718_175920/.ima/governance/architecture_lock.json` — SHA256 `7fa4eb72efb0dbba2f51f970be3c1e17551d0d44febff16ade88615205236246`
- `.ima/archive_final/snapshots/IMA_BOOT_VERIFIED_2026_07_11/governance/orchestrator_lock.json` — SHA256 `6ac4a75f946e478a70eba15af782b85a4f9da44b62542c9d39e707f38da11c2f`
- `.ima/archive_final/snapshots/IMA_BOOT_VERIFIED_2026_07_11/governance/service_layer_lock.json` — SHA256 `06e19a6fbb0e93f3fe4c132b7122269307791336aff02f31d2cc088e587b473a`
- `.ima/archive_final/snapshots/IMA_BOOT_VERIFIED_2026_07_11/governance/product_layer_lock.json` — SHA256 `e012cbcefeb058911576d7c3b26152bbad2c1643aa0b6043616ee9e60331855a`
- `.ima/archive_final/snapshots/IMA_BOOT_VERIFIED_2026_07_11/governance/final_orchestrator_lock.json` — SHA256 `29fd2289a9f1a0263da22843261addfdab547ac612584369ddb9a7c634465abb`
- `.ima/archive_final/snapshots/IMA_BOOT_VERIFIED_2026_07_11/governance/architecture_lock_report.json` — SHA256 `a339ed4137b12ac4217e9d567806c8059e27f9d032525b5e013015dfb6b398cf`
- `.ima/archive_final/snapshots/IMA_BOOT_VERIFIED_2026_07_11/governance/entry_gate_lock.json` — SHA256 `2049cacccd25f100ab239ca67a1672a1416f35f6333c31aa20c697a1bf3c0ed1`
- `.ima/archive_final/snapshots/IMA_BOOT_VERIFIED_2026_07_11/governance/architecture_lock.json` — SHA256 `7fa4eb72efb0dbba2f51f970be3c1e17551d0d44febff16ade88615205236246`
- `.ima/archive_final/snapshots/IMA_BOOT_VERIFIED_2026_07_11/governance/final_audit_lock.json` — SHA256 `7e1137b751d15759933f053442779167870613e71a2dff981be1869c1a655573`
- `.ima/archive_final/snapshots/IMA_BOOT_VERIFIED_2026_07_11/governance/final_governance_lock.json` — SHA256 `c219be53ee82c02e92e1319cc7c282b8ab32d7ae2282efc70ee54886cf0f2271`
- `.ima/archive_final/ima_backup_1783804250/.ima/governance/orchestrator_lock.json` — SHA256 `6ac4a75f946e478a70eba15af782b85a4f9da44b62542c9d39e707f38da11c2f`
- `.ima/archive_final/ima_backup_1783804250/.ima/governance/service_layer_lock.json` — SHA256 `06e19a6fbb0e93f3fe4c132b7122269307791336aff02f31d2cc088e587b473a`
- `.ima/archive_final/ima_backup_1783804250/.ima/governance/product_layer_lock.json` — SHA256 `e012cbcefeb058911576d7c3b26152bbad2c1643aa0b6043616ee9e60331855a`
- `.ima/archive_final/ima_backup_1783804250/.ima/governance/final_orchestrator_lock.json` — SHA256 `29fd2289a9f1a0263da22843261addfdab547ac612584369ddb9a7c634465abb`
- `.ima/archive_final/ima_backup_1783804250/.ima/governance/architecture_lock_report.json` — SHA256 `a339ed4137b12ac4217e9d567806c8059e27f9d032525b5e013015dfb6b398cf`
- `.ima/archive_final/ima_backup_1783804250/.ima/governance/entry_gate_lock.json` — SHA256 `2049cacccd25f100ab239ca67a1672a1416f35f6333c31aa20c697a1bf3c0ed1`
- `.ima/archive_final/ima_backup_1783804250/.ima/governance/architecture_lock.json` — SHA256 `7fa4eb72efb0dbba2f51f970be3c1e17551d0d44febff16ade88615205236246`
- `.ima/archive_final/ima_backup_1783804250/.ima/governance/final_audit_lock.json` — SHA256 `7e1137b751d15759933f053442779167870613e71a2dff981be1869c1a655573`
- `.ima/archive_final/ima_backup_1783804250/.ima/governance/final_governance_lock.json` — SHA256 `c219be53ee82c02e92e1319cc7c282b8ab32d7ae2282efc70ee54886cf0f2271`
- `.ima/archive_final/ima_backup_1783804250/.ima/legacy/ori_legacy.locked.json` — SHA256 `68edd94a6cf8f9d7aadc14000cf7f9dd3ed87526850e9b64f506e3a810047e02`
- `.ima/archive_final/ima_backup_1783804250/.ima/snapshots/IMA_BOOT_VERIFIED_2026_07_11/governance/orchestrator_lock.json` — SHA256 `6ac4a75f946e478a70eba15af782b85a4f9da44b62542c9d39e707f38da11c2f`
- `.ima/archive_final/ima_backup_1783804250/.ima/snapshots/IMA_BOOT_VERIFIED_2026_07_11/governance/service_layer_lock.json` — SHA256 `06e19a6fbb0e93f3fe4c132b7122269307791336aff02f31d2cc088e587b473a`
- `.ima/archive_final/ima_backup_1783804250/.ima/snapshots/IMA_BOOT_VERIFIED_2026_07_11/governance/product_layer_lock.json` — SHA256 `e012cbcefeb058911576d7c3b26152bbad2c1643aa0b6043616ee9e60331855a`
- `.ima/archive_final/ima_backup_1783804250/.ima/snapshots/IMA_BOOT_VERIFIED_2026_07_11/governance/final_orchestrator_lock.json` — SHA256 `29fd2289a9f1a0263da22843261addfdab547ac612584369ddb9a7c634465abb`
- `.ima/archive_final/ima_backup_1783804250/.ima/snapshots/IMA_BOOT_VERIFIED_2026_07_11/governance/architecture_lock_report.json` — SHA256 `a339ed4137b12ac4217e9d567806c8059e27f9d032525b5e013015dfb6b398cf`
- `.ima/archive_final/ima_backup_1783804250/.ima/snapshots/IMA_BOOT_VERIFIED_2026_07_11/governance/entry_gate_lock.json` — SHA256 `2049cacccd25f100ab239ca67a1672a1416f35f6333c31aa20c697a1bf3c0ed1`
- `.ima/archive_final/ima_backup_1783804250/.ima/snapshots/IMA_BOOT_VERIFIED_2026_07_11/governance/architecture_lock.json` — SHA256 `7fa4eb72efb0dbba2f51f970be3c1e17551d0d44febff16ade88615205236246`
- `.ima/archive_final/ima_backup_1783804250/.ima/snapshots/IMA_BOOT_VERIFIED_2026_07_11/governance/final_audit_lock.json` — SHA256 `7e1137b751d15759933f053442779167870613e71a2dff981be1869c1a655573`
- `.ima/archive_final/ima_backup_1783804250/.ima/snapshots/IMA_BOOT_VERIFIED_2026_07_11/governance/final_governance_lock.json` — SHA256 `c219be53ee82c02e92e1319cc7c282b8ab32d7ae2282efc70ee54886cf0f2271`
- `.ima/archive_final/backups/ima_1783804993/governance/orchestrator_lock.json` — SHA256 `6ac4a75f946e478a70eba15af782b85a4f9da44b62542c9d39e707f38da11c2f`
- `.ima/archive_final/backups/ima_1783804993/governance/service_layer_lock.json` — SHA256 `06e19a6fbb0e93f3fe4c132b7122269307791336aff02f31d2cc088e587b473a`
- `.ima/archive_final/backups/ima_1783804993/governance/product_layer_lock.json` — SHA256 `e012cbcefeb058911576d7c3b26152bbad2c1643aa0b6043616ee9e60331855a`
- `.ima/archive_final/backups/ima_1783804993/governance/final_orchestrator_lock.json` — SHA256 `29fd2289a9f1a0263da22843261addfdab547ac612584369ddb9a7c634465abb`
- `.ima/archive_final/backups/ima_1783804993/governance/architecture_lock_report.json` — SHA256 `a339ed4137b12ac4217e9d567806c8059e27f9d032525b5e013015dfb6b398cf`
- `.ima/archive_final/backups/ima_1783804993/governance/entry_gate_lock.json` — SHA256 `2049cacccd25f100ab239ca67a1672a1416f35f6333c31aa20c697a1bf3c0ed1`

## Historical Evidence

Historical candidate files: **553**

- `.ima/agi_evolution/runtime/evolution_history.json`
- `.ima/evolution/learning_history.jsonl`
- `.ima/evolution/git_history_memory.jsonl`
- `.ima/guardian/history.jsonl`
- `.ima/guardian/intent_history.jsonl`
- `.ima/guardian/core_history.jsonl`
- `.ima/evolution_state.json`
- `.ima/ima_evolution_report.json`
- `.ima/governance/product_evolution_report.json`
- `.ima/evolution/evolution_map.json`
- `.ima/evolution/evolution_brain.json`
- `.ima/agi_evolution/runtime/evolution_os_registry.json`
- `.ima/agi_evolution/runtime/evolution_plan.json`
- `.ima/agi_evolution/runtime/evolution_result.json`
- `.ima/agi_evolution/runtime/evolution_memory.json`
- `.ima/agi_evolution/runtime/evolution_proposals.json`
- `.ima/archive_final/snapshots/IMA_BOOT_VERIFIED_2026_07_11/governance/product_evolution_report.json`
- `.ima/archive_final/ima_backup_1783804250/.ima/evolution_state.json`
- `.ima/archive_final/ima_backup_1783804250/.ima/governance/product_evolution_report.json`
- `.ima/archive_final/ima_backup_1783804250/.ima/snapshots/IMA_BOOT_VERIFIED_2026_07_11/governance/product_evolution_report.json`
- `.ima/archive_final/backups/ima_1783804993/evolution_state.json`
- `.ima/archive_final/backups/ima_1783804993/governance/product_evolution_report.json`
- `.ima/archive_final/backups/ima_1783804993/snapshots/IMA_BOOT_VERIFIED_2026_07_11/governance/product_evolution_report.json`
- `.ima/CANONICAL_AUTHORITY/evolution/SELF_EVOLUTION/logs/self_evolution_chronological.jsonl`
- `.ima/agi_evolution/runtime/evolution_log.jsonl`
- `.ima/memory_log.jsonl`
- `.ima/runtime_snapshots/20260713_memory_policy/memory_log.jsonl`
- `.ima/snapshots/pre_memory_bus/memory_log.jsonl`
- `.ima/snapshots/pre_memory_bus_v2/memory_log.jsonl`
- `.ima/archive_final/ima_backup_1783804250/.ima/memory_log.jsonl`
- `.ima/archive_final/backups/ima_1783804993/memory_log.jsonl`
- `node_modules/call-bind-apply-helpers/CHANGELOG.md`
- `node_modules/call-bound/CHANGELOG.md`
- `node_modules/dunder-proto/CHANGELOG.md`
- `node_modules/es-define-property/CHANGELOG.md`
- `node_modules/es-errors/CHANGELOG.md`
- `node_modules/es-object-atoms/CHANGELOG.md`
- `node_modules/function-bind/CHANGELOG.md`
- `node_modules/get-intrinsic/CHANGELOG.md`
- `node_modules/get-proto/CHANGELOG.md`
- `node_modules/gopd/CHANGELOG.md`
- `node_modules/has-symbols/CHANGELOG.md`
- `node_modules/hasown/CHANGELOG.md`
- `node_modules/math-intrinsics/CHANGELOG.md`
- `node_modules/object-inspect/CHANGELOG.md`
- `node_modules/qs/CHANGELOG.md`
- `node_modules/side-channel-list/CHANGELOG.md`
- `node_modules/side-channel-map/CHANGELOG.md`
- `node_modules/side-channel-weakmap/CHANGELOG.md`
- `node_modules/side-channel/CHANGELOG.md`
- `ima-ui/node_modules/optionator/CHANGELOG.md`
- `ima-ui/node_modules/color-convert/CHANGELOG.md`
- `ima-ui/node_modules/which/CHANGELOG.md`
- `ima-ui/node_modules/js-tokens/CHANGELOG.md`
- `ima-ui/node_modules/acorn/CHANGELOG.md`
- `ima-ui/node_modules/argparse/CHANGELOG.md`
- `ima-ui/node_modules/prelude-ls/CHANGELOG.md`
- `ima-ui/node_modules/cross-env/CHANGELOG.md`
- `ima-ui/node_modules/maath/CHANGELOG.md`
- `ima-ui/node_modules/troika-three-text/CHANGELOG.md`
- `ima-ui/node_modules/utility-types/CHANGELOG.md`
- `ima-ui/node_modules/fflate/CHANGELOG.md`
- `ima-ui/node_modules/troika-three-utils/CHANGELOG.md`
- `ima-ui/node_modules/troika-worker-utils/CHANGELOG.md`
- `ima-ui/node_modules/tunnel-rat/CHANGELOG.md`
- `ima-ui/node_modules/dotenv/CHANGELOG.md`
- `ima-ui/node_modules/es-set-tostringtag/CHANGELOG.md`
- `ima-ui/node_modules/hasown/CHANGELOG.md`
- `ima-ui/node_modules/es-errors/CHANGELOG.md`
- `ima-ui/node_modules/get-intrinsic/CHANGELOG.md`
- `ima-ui/node_modules/has-tostringtag/CHANGELOG.md`
- `ima-ui/node_modules/form-data/CHANGELOG.md`
- `ima-ui/node_modules/call-bind-apply-helpers/CHANGELOG.md`
- `ima-ui/node_modules/es-define-property/CHANGELOG.md`
- `ima-ui/node_modules/function-bind/CHANGELOG.md`
- `ima-ui/node_modules/es-object-atoms/CHANGELOG.md`
- `ima-ui/node_modules/get-proto/CHANGELOG.md`
- `ima-ui/node_modules/gopd/CHANGELOG.md`
- `ima-ui/node_modules/math-intrinsics/CHANGELOG.md`
- `ima-ui/node_modules/dunder-proto/CHANGELOG.md`
- `ima-ui/node_modules/has-symbols/CHANGELOG.md`
- `ima-ui/node_modules/axios/CHANGELOG.md`
- `ima-ui/node_modules/fraction.js/CHANGELOG.md`
- `ima-ui/node_modules/three-stdlib/node_modules/fflate/CHANGELOG.md`
- `ima-ui/node_modules/@monogrid/gainmap-js/CHANGELOG.md`
- `ima-ui/node_modules/@use-gesture/core/CHANGELOG.md`
- `ima-ui/node_modules/@use-gesture/react/CHANGELOG.md`
- `ima-ui/node_modules/@react-three/fiber/CHANGELOG.md`
- `ima-ui/node_modules/@babel/parser/CHANGELOG.md`
- `ima-ui/node_modules/@humanfs/types/CHANGELOG.md`
- `ima-ui/node_modules/@humanwhocodes/module-importer/CHANGELOG.md`
- `ima-ui.backup_1784029005/node_modules/acorn/CHANGELOG.md`
- `ima-ui.backup_1784029005/node_modules/argparse/CHANGELOG.md`
- `ima-ui.backup_1784029005/node_modules/color-convert/CHANGELOG.md`
- `ima-ui.backup_1784029005/node_modules/js-tokens/CHANGELOG.md`
- `ima-ui.backup_1784029005/node_modules/prelude-ls/CHANGELOG.md`
- `ima-ui.backup_1784029005/node_modules/which/CHANGELOG.md`
- `ima-ui.backup_1784029005/node_modules/optionator/CHANGELOG.md`
- `ima-ui.backup_1784029005/node_modules/@humanwhocodes/module-importer/CHANGELOG.md`
- `ima-ui.backup_1784029005/node_modules/@humanfs/types/CHANGELOG.md`
- `ima-ui.backup_1784029005/node_modules/@babel/parser/CHANGELOG.md`
- `node_modules/accepts/HISTORY.md`
- `node_modules/content-type/HISTORY.md`
- `node_modules/etag/HISTORY.md`
- `node_modules/finalhandler/HISTORY.md`
- `node_modules/forwarded/HISTORY.md`
- `node_modules/fresh/HISTORY.md`
- `node_modules/http-errors/HISTORY.md`
- `node_modules/media-typer/HISTORY.md`
- `node_modules/mime-db/HISTORY.md`
- `node_modules/mime-types/HISTORY.md`
- `node_modules/negotiator/HISTORY.md`
- `node_modules/on-finished/HISTORY.md`
- `node_modules/parseurl/HISTORY.md`
- `node_modules/proxy-addr/HISTORY.md`
- `node_modules/range-parser/HISTORY.md`
- `node_modules/router/HISTORY.md`
- `node_modules/statuses/HISTORY.md`
- `node_modules/toidentifier/HISTORY.md`
- `node_modules/type-is/HISTORY.md`
- `node_modules/unpipe/HISTORY.md`
- `node_modules/vary/HISTORY.md`
- `ima-ui/node_modules/mime-types/HISTORY.md`
- `ima-ui/node_modules/mime-db/HISTORY.md`
- `web/README.md`
- `mobile/README.md`
- `plugins/README.md`
- `modules/README.md`
- `marketplace/README.md`
- `auth/README.md`
- `database/README.md`
- `docs/README.md`
- `tests/README.md`
- `investor_package/README_INVESTOR.md`
- `ima-ui.backup_1784029005/README.md`
- `ima-ui/README.md`
- `safety/README.md`
- `deployment/README.md`
- `product/README.md`
- `users/README.md`
- `memory/README.md`
- `devices/README.md`
- `product/runtime/README.md`
- `product/mobile/README.md`
- `product/web/README.md`
- `product/android/README.md`
- `node_modules/accepts/README.md`
- `node_modules/body-parser/README.md`
- `node_modules/call-bind-apply-helpers/README.md`
- `node_modules/call-bound/README.md`
- `node_modules/content-disposition/README.md`
- `node_modules/content-type/README.md`
- `node_modules/cookie/README.md`
- `node_modules/cors/README.md`
- `node_modules/debug/README.md`
- `node_modules/dunder-proto/README.md`
- `node_modules/ee-first/README.md`
- `node_modules/encodeurl/README.md`
- `node_modules/es-define-property/README.md`
- `node_modules/es-errors/README.md`
- `node_modules/es-object-atoms/README.md`
- `node_modules/etag/README.md`
- `node_modules/finalhandler/README.md`
- `node_modules/forwarded/README.md`
- `node_modules/fresh/README.md`
- `node_modules/function-bind/README.md`
- `node_modules/get-intrinsic/README.md`
- `node_modules/get-proto/README.md`
- `node_modules/gopd/README.md`
- `node_modules/has-symbols/README.md`
- `node_modules/hasown/README.md`
- `node_modules/http-errors/README.md`
- `node_modules/iconv-lite/README.md`
- `node_modules/inherits/README.md`
- `node_modules/ipaddr.js/README.md`
- `node_modules/math-intrinsics/README.md`
- `node_modules/media-typer/README.md`
- `node_modules/mime-db/README.md`
- `node_modules/mime-types/README.md`
- `node_modules/negotiator/README.md`
- `node_modules/on-finished/README.md`
- `node_modules/once/README.md`
- `node_modules/parseurl/README.md`
- `node_modules/proxy-addr/README.md`
- `node_modules/qs/README.md`
- `node_modules/range-parser/README.md`
- `node_modules/raw-body/README.md`
- `node_modules/router/README.md`
- `node_modules/send/README.md`
- `node_modules/serve-static/README.md`
- `node_modules/setprototypeof/README.md`
- `node_modules/side-channel-list/README.md`
- `node_modules/side-channel-map/README.md`
- `node_modules/side-channel-weakmap/README.md`
- `node_modules/side-channel/README.md`
- `node_modules/statuses/README.md`
- `node_modules/toidentifier/README.md`
- `node_modules/type-is/README.md`
- `node_modules/unpipe/README.md`
- `node_modules/vary/README.md`

## Consistency

- Ori Cohen mentions: 15
- אורי כהן mentions: 0
- IMA mentions in identity material: 147

## Important Interpretation

This audit does not decide legal ownership or prove that every historical claim is true. It verifies what evidence is currently present inside the IMA project and whether the project contains a traceable provenance structure.

The audit itself is a new evidence artifact. Its SHA-256 is printed below.