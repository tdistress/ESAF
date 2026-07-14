from __future__ import annotations

import hashlib
import json
import re
import subprocess
import unittest
from collections import Counter
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ORACLE = ROOT / "docs/superpowers/specs/2026-07-14-uk-cyber-essentials-plus-v3.2-provision-oracle.json"
RIGHTS_REVIEW = ROOT / "docs/superpowers/reviews/2026-07-14-uk-cyber-essentials-plus-v3.2-rights-review.md"
SOURCE_TITLE = "Cyber Essentials Plus Test Specification"
SOURCE_AUTHORITY = "UK National Cyber Security Centre"
PUBLICATION_IDENTIFIER = "cyber-essentials-plus-test-specification"
DISPLAY_DATE = "April 2025"
RESOURCE_PAGE = "https://www.ncsc.gov.uk/cyberessentials/resources"
RESOURCE_PAGE_DATE = "2025-04-28"
CANONICAL_URL = "https://www.ncsc.gov.uk/sites/default/files/2026-05/cyber-essentials-plus-test-specification-v3-2%20english.pdf"
CANONICAL_BYTES = 424226
CANONICAL_SHA256 = "2adf2703dec3b581e13e39c6a1de230bb1bce6d85f1158bb1eb53108e28596e8"
LEGACY_URL = "https://www.ncsc.gov.uk/files/cyber-essentials-plus-test-specification-v3-2.pdf"
LEGACY_BYTES = 419191
LEGACY_SHA256 = "d334c717597a01fab7a362377b7b04c8449568052ed1c4cf48837f6fb3aca694"
GROUPS = ("M", "T1", "S", "T2", "T3", "T4", "T5", "C", "A", "B")
EXPECTED_COUNT = 144
EXPECTED_GROUP_COUNTS = {
    "M": 24, "T1": 16, "S": 11, "T2": 9, "T3": 37,
    "T4": 9, "T5": 7, "C": 13, "A": 4, "B": 14,
}
EXPECTED_SECTION_OCCURRENCES = (('sec-m-cover', None, 'Cover', 'M', 1, 1, None, None, 'context_only'), ('sec-m-contents', None, 'Contents', 'M', 2, 3, 1, 2, 'context_only'), ('sec-m-whats-new', None, "What's new", 'M', 4, 4, 3, 3, 'context_only'), ('sec-m-audience', None, 'Audience', 'M', 4, 4, 3, 3, 'context_only'), ('sec-m-purpose', None, 'Purpose', 'M', 4, 5, 3, 4, 'included'), ('sec-m-before-you-begin', None, 'Before you begin', 'M', 5, 5, 4, 4, 'included'), ('sec-m-general-prerequisites', None, 'General prerequisites for testing', 'M', 6, 6, 5, 5, 'included'), ('sec-m-success-criteria', None, 'Success criteria', 'M', 6, 7, 5, 6, 'context_only'), ('sec-m-test-results', 'sec-m-success-criteria', 'Test results', 'M', 6, 6, 5, 5, 'included'), ('sec-m-pass', 'sec-m-test-results', 'Pass', 'M', 6, 6, 5, 5, 'included'), ('sec-m-fail', 'sec-m-test-results', 'Fail', 'M', 6, 7, 5, 6, 'included'), ('sec-m-advisory-notes', 'sec-m-success-criteria', 'Advisory notes', 'M', 7, 7, 6, 6, 'included'), ('sec-t1-test-case', None, 'Test case 1: Remote vulnerability assessment', 'T1', 8, 10, 7, 9, 'context_only'), ('sec-t1-purpose', 'sec-t1-test-case', 'Test purpose', 'T1', 8, 8, 7, 7, 'context_only'), ('sec-t1-description', 'sec-t1-test-case', 'Test description', 'T1', 8, 9, 7, 8, 'context_only'), ('sec-t1-prerequisites', 'sec-t1-description', 'Prerequisites', 'T1', 8, 8, 7, 7, 'included'), ('sec-t1-subtest-1-1', 'sec-t1-description', 'Sub-test 1.1', 'T1', 8, 9, 7, 8, 'included'), ('sec-t1-figure-1', 'sec-t1-subtest-1-1', 'Figure 1: Sub-test flow diagram for assessing services accessible through the firewall', 'T1', 9, 9, 8, 8, 'included'), ('sec-t1-interpretation', 'sec-t1-test-case', 'Interpreting the test case results', 'T1', 10, 10, 9, 9, 'included'), ('sec-s-sample-testing', None, 'Sample testing', 'S', 10, 10, 9, 9, 'included'), ('sec-t2-test-case', None, 'Test case 2: Check patching, by authenticated vulnerability scan of devices', 'T2', 11, 12, 10, 11, 'included'), ('sec-t2-purpose', 'sec-t2-test-case', 'Test purpose', 'T2', 11, 11, 10, 10, 'context_only'), ('sec-t2-description', 'sec-t2-test-case', 'Test description', 'T2', 11, 12, 10, 11, 'context_only'), ('sec-t2-prerequisites', 'sec-t2-description', 'Prerequisites', 'T2', 11, 11, 10, 10, 'included'), ('sec-t2-subtest-2-1', 'sec-t2-description', 'Sub-test 2.1', 'T2', 11, 12, 10, 11, 'included'), ('sec-t2-interpretation', 'sec-t2-test-case', 'Interpreting the test case results', 'T2', 12, 12, 11, 11, 'included'), ('sec-t3-test-case', None, 'Test case 3: Check malware protection', 'T3', 13, 16, 12, 15, 'included'), ('sec-t3-purpose', 'sec-t3-test-case', 'Test purpose', 'T3', 13, 13, 12, 12, 'context_only'), ('sec-t3-description', 'sec-t3-test-case', 'Test description', 'T3', 13, 16, 12, 15, 'context_only'), ('sec-t3-prerequisites', 'sec-t3-description', 'Prerequisites', 'T3', 13, 13, 12, 12, 'included'), ('sec-t3-select-subtests', 'sec-t3-description', 'Selecting appropriate sub-tests', 'T3', 13, 13, 12, 12, 'included'), ('sec-t3-subtest-3-1', 'sec-t3-description', 'Sub-test 3.1 (for devices that use anti-malware software)', 'T3', 13, 13, 12, 12, 'included'), ('sec-t3-subtest-3-1-1', 'sec-t3-subtest-3-1', 'Sub-test 3.1.1 (Check effectiveness of defences against malware delivered by email)', 'T3', 14, 14, 13, 13, 'included'), ('sec-t3-subtest-3-1-2', 'sec-t3-subtest-3-1', 'Sub-test 3.1.2 (Check effectiveness of defences against malware delivered by browser)', 'T3', 14, 15, 13, 14, 'included'), ('sec-t3-subtest-3-1-3', 'sec-t3-subtest-3-1', 'Sub-test 3.1.3 (Manual Checks for devices that use anti-malware software)', 'T3', 15, 15, 14, 14, 'included'), ('sec-t3-subtest-3-2', 'sec-t3-description', 'Sub-test 3.2 (for devices that use certificate-based application allow listing)', 'T3', 16, 16, 15, 15, 'included'), ('sec-t3-interpretation', 'sec-t3-test-case', 'Interpreting the test case results', 'T3', 16, 16, 15, 15, 'included'), ('sec-t4-test-case', None, 'Test case 4: Check multi-factor authentication configuration', 'T4', 17, 18, 16, 17, 'included'), ('sec-t4-purpose', 'sec-t4-test-case', 'Test purpose', 'T4', 17, 17, 16, 16, 'context_only'), ('sec-t4-description', 'sec-t4-test-case', 'Test description', 'T4', 17, 17, 16, 16, 'included'), ('sec-t4-case-4-1', 'sec-t4-test-case', 'Test case 4.1', 'T4', 17, 17, 16, 16, 'included'), ('sec-t4-interpretation', 'sec-t4-test-case', 'Interpreting the test case results', 'T4', 18, 18, 17, 17, 'included'), ('sec-t5-test-case', None, 'Test case 5: Check account separation', 'T5', 19, 19, 18, 18, 'included'), ('sec-t5-purpose', 'sec-t5-test-case', 'Test purpose', 'T5', 19, 19, 18, 18, 'context_only'), ('sec-t5-description', 'sec-t5-test-case', 'Test description', 'T5', 19, 19, 18, 18, 'included'), ('sec-t5-case-5-1', 'sec-t5-test-case', 'Test case 5.1', 'T5', 19, 19, 18, 18, 'included'), ('sec-t5-interpretation', 'sec-t5-test-case', 'Interpreting the test case results', 'T5', 19, 19, 18, 18, 'included'), ('sec-c-conclude', None, 'Conclude the assessment', 'C', 20, 20, 19, 19, 'included'), ('sec-c-note-deferral', 'sec-c-conclude', 'Note for Delivery Partner', 'C', 20, 20, 19, 19, 'included'), ('sec-c-note-exception', 'sec-c-conclude', 'Note for Delivery Partner', 'C', 20, 20, 19, 19, 'included'), ('sec-a-appendix', None, 'Appendix A: Vulnerability scanning', 'A', 21, 21, 20, 20, 'included'), ('sec-a-note-delivery-partner', 'sec-a-appendix', 'Note for Delivery Partner', 'A', 21, 21, 20, 20, 'included'), ('sec-b-appendix', None, 'Appendix B: Types of test file', 'B', 22, 23, 21, 22, 'included'), ('sec-b-note-delivery-partner', 'sec-b-appendix', 'Note for Delivery Partner', 'B', 22, 22, 21, 21, 'included'), ('sec-m-rights-notice', None, 'Rights and attribution notice', 'M', 24, 24, None, None, 'context_only'))
EXPECTED_SECTION_IDS = tuple(item[0] for item in EXPECTED_SECTION_OCCURRENCES)
SOURCE_PASSAGE_DIGESTS = frozenset(('00b01f4a4292528833b30cf08688aad9090b69bf967b76c902569a0ceee977e7', '01afdc00db8780b762fbbc5d365739bfd7e4b5e7660e6c4bc335513e24bbd137', '037e610c93358fc2f9b689dd444cfc3ebe9a04c5951fb44008f400061e117a46', '0394b18f508fd1f2b9d8829d071bd4785d1d13fe1f6ec7e6f9bcce670f822a8d', '03a38f410de85d8e2aa04196fc89682ec473bbda5a23bcd4e4a61368b8d3beeb', '051bfcd5fe53e9ddbafefd63b20e12647c805569556a7b815dfa15be1e8e2da1', '05974d7ecba57ec02f941a9b8c154ad0d61fff66febea409cf8e972c1121a979', '059d44f75eac8ad4af5c713b7332b062163eb48257e76930b078fcfe7e07f168', '05c6ea70c345e376a2951963c7905e4a5c5e04fe86d520a5df1f14de14ac5b0f', '0686b35975c34bfc741406e83ea867947ae56d1571ccec073729c5923d25b05c', '06e24d5df45c8702d2820c2c6b7f69f7301ccf9cfc8803c778f961f34166f7af', '07eb2b61c60345f94056241d87336e3bc69e8a6bfd7512d4a8778ba5694040ac', '09acab4744872f3270b67f65481cf5bd295af6dff4325080d6c43f696d1e08e4', '0b782af3dc42cc977ef9ca1a306ed9a68d7c247edae8c4b21e450addb584ad41', '0b96fa7837a64af4a348a504f15c1dec916ec6cda3a145295926368e437593d9', '0be32a9defd043b277de625e0b30bc2ab74136084d767682bb2c45458d2b98dd', '0d2217b35170c80def4fdf599f666fc6985c39231ddbaaa79b18a0c6473e099f', '0dfb25b7a07d2c266234fac9abf2a19392f2a223c2eb226dda8cf6f8da06718f', '0e6a9b101de846319163f60c343a50f4dc0c7c328322d5031080ff850cf78559', '0e9988e08053b46df4045a473a3e36d8faceadb8a3e6086f17bd52d915698f5c', '0e9bd9e0a372f324b8d34f23b21507acb6cded5950c14d0f2cebc739286872e9', '10863ba0b93229c14f295279f86264bf5f53363b6559b38dc9bc799ddb4e9bca', '109203790fda90ab19f769b1c8458fe25e4619c97dc0bbb3f899d631e03d60aa', '1345359ae5e4bbfa5642989998767c8d27c16f6dfb54005ecc35e9ca56be333c', '14e62cb08ea7c03b9e7dbdceada741225605df328cb9732d34e551325b1a52d6', '15a8669aabb00b2f1c410ee59b329efd5aa8318c44c0c8fab11fb45b3ebf65e8', '15c5400e65f15727d878b30b30d419aa9a776c198dc785e316547c0b93dc2908', '1733e93e44000458ba2a93409ccd5cdb26355cdbb12ffd3c2a1e7e92a79a26a6', '18b11f3ebf9057660da17c2d0fab7d2263a50669d8d55ac0b65833e5db0092bb', '1bc217da0d8bc1c9ec110f3a66042ea83c07d8cd8f4a555ba89e00cbd4d30f84', '1d05444218f10ba3b23c48ad0f23c65fbecc79467755df596ab6849a05fc0fb6', '1fd234338a31e460bb0138575f2a6fe59a1bf46981d71f68a277d42949bd3210', '20a2495078f98bc6dfc1960cb4fc325b8eaad683d97a720683dd7327118a7f9c', '24f3f35189e5fb37bb7ca1b8dd16bab1536183d21cb82ccc083f09a58217e4e0', '26eb570f6a8230a2c1b0bf34b0c2fbfd118813d42a94e86c2b517df892515c3d', '29e5d0770db032ac728ebde0927cd811d6e9c2af0a6742df59cfc5929898b6b4', '2ad3271b7b9bcb30612fb23e4511d40216ee4f2529da7fcee75ac45592b42b2e', '2c8785a5441a6d0dffb555c31f69c034d71959c0fff55404e4b3aeaf299cb2de', '2e37c413de65fd7c5f888bf73f72966016c79d2937ffe31f8cbe7492c440f840', '2e56b1745cde7cf995428bed12e6b93016acf6e756479c8f0b08c5f7d93aa8f8', '2e9e867445f2df0af0d3758f17a787db92b285b6db65d036b8a4518d599734ff', '309cc4c411730c38da47bd68489afaaf80c8b8a36a16ff7d9e5aca80fecfdcdc', '30f8b1d0421c9f4eb5c719574b847b49b234ac380c7d74c30a911d251ec87226', '330bc8ac1662da47c9f762daa87932db1e85d10765755023e46b903ca4ed6fa6', '332b3bfd2d0016191db18468e6bae6473a109e0dea99b7ed763e85a5a5bdeae2', '340ad0a48fdc1b4f9c78c7860e767562968c486c9b9b807c8b440c76d1c14c34', '363270634ab07fbe452dbd950d247e07fb75daabebabc52f5b11d5c9d950fb51', '36fdf7498604a47b6deb809c02104209dfe66f6d6d609f64c8d8813b84e177ce', '3838cb7e913dfc7ba1ad2e16072de4fe2a03d054ba71b2016129cf58f389d8b2', '384767c82ede583f5ae6a6375ddde36bc01c37ec48a683f98068d87605b4486b', '386f9a9130e995c6503126952676fc2bf4058ae185762a03fb4730c4f96a7952', '3c054fdd7784a5eb5598bc994848abdc4325f00a2432b723657bbe53fe1d6560', '3d24eac25f3b269e78b215656550679e97f7419d60fbca107896930858ebb42e', '3d9110d3fde3bc8dd1f2064a70d0503f02297df36578746e4fe45a0318d8c540', '3e21fd9100213f1daf0f165aede375ceb2355caba1af052ea48c55e7984343fc', '3fc7fb3adc438ff915b3a2770bb9c8f27c9cc1692388a8fe0eac117b1ed1d303', '42ae8c8599218e302a03e7ed00cfe60870ec81a53c6d57ff33777a9f42a175d8', '42ebe97af6016f5789b2c95f56f16d9adfc6a941556ca8911bb62b461dffdb58', '432e831b8f66976616d5a6f268b3bc4dcb46dedcde4e62692f9d101cc16518d1', '434f578dd19d7a2ff842987ba711020f4cdb4f04beb6b3f8bb5e7c5afc921f64', '45183c5405a7b007784210853f5b642e82deed0945e1135dcfb735938d60e828', '457f51ccd95bb607575f7c9f158a856abab28dac78b4632f72ca6f2ca02d767a', '467b3029ac2e9915a55e27444d803f3105efb30b15945c49acdfc76df7d709a1', '46c09a74272d8932d2cb5c0c1270a9580d858cd56afb217caddb97477a186c78', '470a913ce8c82b50a5b0fae459f6d3a72ee09ebb6d7910ab3b636bf094ea0cf9', '49a50c8b3000d8e7dc4f3cc8154d03d96ead9160078df4def9aadb16072fd825', '49d00c8e9b4b4ad8b8e326779d0fe098c5ec6e336ec4f8a78c50684d67230958', '4bb2316e31956f13b5e90724e765966974e29760a9347514f2034e123b987018', '4dff2523e792e9c624d7b8a4b82eb9e2e8a9bd61fda43281672cd46bf23bc151', '4e233d408bcea0636c9c78bbd035117d27a36d3425f5449dcf1aa4c43c64e9f0', '4efba36def3ec897bd237ab63f4f01662a32cfca5db61786b28029b501a31aaf', '50c0c8f113b6161af694fb8684a8906941e65dcd9bdde138574bfd789a9a745b', '5170422fcb9287aa5b90457e1744018f651e9420577a3e0705ff76154ac311f3', '51b776fb0c61db9382c8b7298e19456a5c454025e304d4d3015baad0200f6b21', '545ddcdda3bd5851ce39323de9e2d7df191610362284877657fb62088bea56ee', '54965a1d480efb0460788337fab86dede76c1ab15d592c1082391d0992c2e80d', '549fcc089164bdc9c31fa8334067ea9b756c1e6ca66f2afa69af2bf4995e7321', '55105a8f3c890f70c021d6c339d894c907be9802d93f1cbc4cfdf0ec6428e42f', '55fb6428f401d80ae092618532ddb35314d7f22ab497cfefead7de2d4026da8b', '5ac5ac0f43c9c3f6cea68f97407ce97de285125af7a98d44b52cd387360e0ad1', '5dd20ed547f4c64bfc77be13ea40c79367f99f9282f650a6f5b07d1a169a47ab', '5f75c8d65f261249fde6848c11176da33a6cace9b62b378750e71d603339798a', '6092d8e0e0bb537a14d328409e5bdeaf690336a09c880265ade03036a2a802f8', '60a689f1198fb61dd371752597503e099ce5f6e639a3867f039d63f1afd1c69e', '613e0e46cc502ffdab4dc7023c1b0aa482d56b4d3745657c9aaac6cf47d6f4ef', '61d8d7c0d5dadcb98c09f6b3f7396a166321f3b47a1039a572b625d61b3d7f8e', '61e8bd7e080fd7cc1cef57fe6fd14772d4da4a6ff76854c27f1a5f6f3d915e7e', '62305cc558690591f8602df32a524e2d25b5bffa1a18ff2361255b05b63fa0a4', '6379bfc69ca5845c3656b5228c5283e911a3ae5a10d2f22e45c673e667c6c2bc', '6437a3090f9b65e48b7f1b8eab7b036909264e8d45c8a7549dfdbafd98eda202', '64f1e91625f12f625dd72a0f59449023dd71dd54ca230baddc7c914b66db83bd', '657cf710751e10a6816cae8195269190c2da867be6d2ecb3c7ce59edfc821242', '67dfca1a7d93ea735dab8139002449f20587690cda0d96d9182ba0da961b383a', '69d105e07cac284089860abac8ff72245e91c5af6180d4ab882a0018c894c870', '6ae62f7ec97963aad0275580760b1e403857f1a3581da4f100ed7c789775ca1e', '6b1bf6efb660c1b4e0006e44d48acc59efa5d2f7d40c2578865e177786365ce5', '6c24b40d8aa2492b81db9223497c4a2f28fe85b37ffebc6977d43d82d9f55139', '6c9cc8672ee1c2ed8a58f8c9a75533a7ec2f28e0e3390909538cbac07b03016d', '6d8752f758d4edf9bff2c64dab0d1307843e0cb911885bc6dffce26425c1ca3e', '713f9b8f2bfefe8f4960179430ee4dcfe7d22da99ea61851adab44412b0a7f83', '73ced56b69a9a2ac2067362ee47a03d86bc98d7947d3ba6c9340cf312004223c', '7466f2da450c0867acc4cca6c30cc67e2c63e2b13d86cdfa2efb8871f83d0f30', '760338565fa82503b78e0baea4b59a6928c4045d9fcdcb365c351ba3b5801b34', '7750ebd072ad4e16d3dfeae3a3b4fe6ecfa10eec7707d8a6fbe6c9194ab0d5e8', '78517c4da2eafa473605a419773b9a52894c11ceaeb630d360382de6c2094fd5', '79c7746a6a1863a5612737a0f00177dd132135b259288a4bb097ed166bbb0427', '7bd8ccc8f11af8b60211c5891b37708ff4b26aa32874969891f983c77babfda2', '7f481d029c36c9c293427df6146a7101451041e9c6d57c212c974d40735b1d41', '7fd49330c453101c0b1985650da9255bcd9e01e7699f448242ccb40b6ad03aeb', '83dec27a4a9999ebd51fd4bd216147e8f1042279cf96ac838781c1327c0abbe4', '84010ff08bb3bc4715bd61ce0d5b033b33f05e63d6050fca7059ac451f0dcc03', '84988cdf5446a1e3e229ee9553c3405c398d0007071fc79854034ca39c778861', '854ee2093e1c22ae88162c323941ebde883513e95e36ba1833770043c6032b98', '86570ec899f560a3e2dcc142d69cac7941becf36967fb11390cad3cda3c53902', '86b012d3b2d4c3f6ddc6d812f6ec053aa94d6ae7b66b2725f96137c300b5c11c', '8705ce588e68a16e2977490198495b95ad0a534811b68970bb67905b7e3c206a', '88984e4d4a522043571bf4b715b76eb086217f74ea5d6bca5f6deb32cd811683', '89bab068be33369a7a1d5707ddd5f6053f761a33716bb260cca030bf106e1606', '8a98090935c4b61f337d348e2e37e51abf6878bbb3161c6ca3aa1bf784844857', '8b9897ac303b32e375ab8f217e131c5b6b66540278e11116e1f49f71683b648c', '8bbeb1cf822c2ef6878fe6174370561ac812e9d10419cb2325d7d8d6a667a41a', '8c5add51b3366ad12d1a598867cddf786bf7ac5c230e5b47cdeb6f39ba3d5961', '8cf7cc428f3376c6374cf315feea397a28c92267fa28e2de99f844ef21201d59', '8d496b77b18b04fde5fdd49f52253673349baf61b1b323f3e95df62d760f4778', '91cfd991719efb403731375c916c4fcb6c3c547cd6a76ddf0392e563260cfa14', '92b95e4fd5f963ddcf43217ff8a37ec8ac33f1919b5b61b0e848cd33d9ae5360', '931217790a21f56edd5952dbd1d4d156830b5d6e5915f1a69fb1cb30c55c4f13', '96103e33a0e8126e6b1e572fd9cd717d12838a9d03e132ed098e8a3c7213d5d4', '96642430f2bfcc2927d9ea727361e40770dea18a0c88cd36d9a6ebefce825c1f', '96df1b41eacd1cf7d93b08292e4167645f9113cc8b1e95d63441e958e7b055cd', '977b057b6ae9348ccefcd8002b0fd4aa276cfb3b70f438359a76b191909b2c7a', '99d6ebf8d3d9ae459b03d820fd3b4ac0bb7fc7c9fb2c04d8aed6030f45f7204d', '9c5aa97b305b8079433bfc3ece5e1875518de4f8999e3269ea62ea76ea6910ca', '9c957755fe597a8ff8faf4389412ce893c763aa4fc96c37751e1780b4ea54f61', '9cd6b79352837c011e91607875b1d476ea8aecaeb5b661ec52e510e6a386324c', '9d9808056fb807e77d2f7d93bafbba1a615b681a3479de2b750d15de16bf5de8', '9ef43c2575d20da0edb98e0c11ac4edb3a8af3b8c0f5ce9bbe098bb533a75ee1', '9f29c4b9b4e617e7294d4521fbf3c2e0f721ae86f3995da47aa74565a67cccc7', '9f7313a538f94bad8c6054fd3e2c73e19e886e7c2aad8a3b8437d90e5ed55b10', 'a0030b6f3a799248d38a701eb32c79124007dd739be0ad9bd4c361c98edef1bf', 'a06763dd3738835a032fadd7f6a7c957a4de371627bfaa378a7cda4eb9f4ed88', 'a0c6b19ae90f4ff0737f073127dcedbc53ef5415ef6caa0ad8d77083316fe0ca', 'a1f8bdb8613687b40799641b2a365e4982fd5e629a3d73ee29cc4d30c110db3d', 'a29a5d86e40bcd47829ed69f57c20ad02a2571181972c1ec9b2da61c30ac9f61', 'a419fc766902b1d43bc8e2a506f2b951fb1ba777526c3457082e338a64c47f60', 'a439d474e63c5818dce6efa073057af81d958d0fa806f328073e1fae711a68f4', 'a50b68af47893ed99fdf890582d98b70993d3bc307e4327c8b9390ee67af0d32', 'a72434b8b755581439bc65fafebb3fa0afb1a17db1fc567d43c7a1c41e4d503b', 'a7df3e267bf7e8f3c1f2fd05ce917cc8bda5787db77191310294e4d3ef67fceb', 'a8b1006df0a51526b09955b5edffea80aea5817b18c40141fb69e0b01186a4b3', 'ab710b9dca0630898362e4c7c4df50e9bc4b0346c056fe8d432172afd1c48a9b', 'ad0714260320ae9ec15f5dd637858ea2dfb3a76cd7e97116a7cf1486df22cefb', 'ad6d3f1ced88c04515f328b31aa1e34fa03113fd81ddb31572d731efa34b80c9', 'ad9c4151a53bd0361e1247f3ab55e268416cb739e6912d73e71fda0dd5e32937', 'ae20cd8817bd67113a499c70c2a53d26a58ca38d72652aa4d67fe1a242fd5589', 'ae31df4f80a73748c236a7963f1512d56bf720fe14f4a94a06c05e61e6951e59', 'b068eb78f000209379cae4edc86ae9425c97c52fc79e9562adc790091aa2bad6', 'b2ef930e52b4a7a885b1a3285e0eee1e6110313b20025a0491b7a10207b35c0b', 'b43fe012cd751907afead034cdb271f0d8b6829748e8aac7a1239bbf3b2c4830', 'b4b97513010fb8b8d3e6204275874b2970b3cb83810ce1f009f1491e80c2fa8e', 'b50cd5bfed76231ccf7b1c5346966b35517d8aa58bfcddd42e5fdb1d4d43bc3a', 'b86847edaeb042ec4062beb0514c0e647568163b9d2575da64a5ce8c512cb426', 'ba5831a9717e1226787a8f065383083b04d3804509039097b4ef129939a76257', 'baf7ade94d318719f4146cec1db81594895b9a8720bcaf72f5bdc3bdf49ddb25', 'bc7ab2175d06faa7df53a538d2639770abf4c50ea1112b6f95ec7748961e63e2', 'bd11ed6084f938835c9cf6fa06f505bfc5db109fdf9741a3a9c99997f3fe2e5a', 'bd23dca947ecf11a50dafa9d62a0999999cd25f985f5b0056773036aac4da1c9', 'be42c963eeb37c0e0643332c5b08a5000e17600d94c393026b010dd44c0f7833', 'be7b5c618ba5261c04a08772b7d72c69788e0d6e0df3ae9ed44189fe07e538f8', 'c01f75bb5a6cfda5600d89afad9a7960cd4fc989c7f21c8d41097049418b91b6', 'c0313f96cd78b64674d614a4df81927d499c4902791ad556308571e86b5e6d37', 'c114c96499c1a0b7978066e83f29b21cd0e222ef48d315dde973e515863a1e3f', 'c2bd6f8c26618e3f10fd2e4d76bf1ac6210afaee22d06f8981ed5f68b4a368c3', 'c34956061f86678e18cacb20e7cca52cb772f74cdeeff1e311e4972b36827730', 'c58c72539f7a69f038b292d0ed777eddcb7c4830f7917097c8963f263ae4f4a0', 'c6762b5e6cb5f1e1b41a872e143e6fde6199d706bf8b98bb885799662f54c7a1', 'c6909ae29b14b44a2dd609441009321195cf79e6d087b7451abb93bd354178e2', 'c7e52c41341ae1027f9e94515ab91f7ed79af2b4521a4ccf51f5dcc6fd4ad043', 'c9c615edcbb61122290a58564db19e72974e5c0d48b794c3ae19e5f93785e7bb', 'c9e966084e665c05c3ec038b06e1e46d7538b8c0fb2e82d0deca0209fb239385', 'cabd3d56282a57106537c28ab05ab2020e04a94994191fcac098ba9977701a20', 'ccc4c03bbc83c99d8115be694b560ba2d76d4e2d5534b97acacd7b0db203550a', 'cccdd694b93d4da88f761f6179c24373f8bde2178e60e8b1cad63076ca517e32', 'cd04d4442da47c00e88eff44af1102664adf48793fed25247902af307775ad8e', 'd046161e11424e695c1b552915abc8add9b13654cecb9f012f117d1897e80e8d', 'd329faf4769df443d6282cd82dba65943862014b96f800f39a0e1f5dc2f34a5a', 'd4d66ea0f0f314f86ef7e70ffe32e20dc4e72be4c78039938b16588dee613eed', 'd605030de1d60317e7249fb9254cc5d27eeb2f6a67645fb144bf86d71c8708bb', 'd6484cf149b1caef9279820dd468fb8758deb4a142d16f6150b352990353bbef', 'd6acefb9ee95160151b9826f9cd616e2afaa7326ad1f1660b21f197aba2c2b6c', 'd6b50cdcad713aa3b8b1f4fa6390797c676abc253ac50bb9658112d4a8d10643', 'd7b9bb968df19ce0df815fc477a75a1665f4ff98543394e74b15d42bdbb20897', 'd924285cfff54eb232ef4634256c5fc48f3af9cdda5db665ab0f5366e2a7119e', 'daeb6681f81050f694c61197ba29faaf178fea8006d934a55dc229ce257e91ec', 'db7fae02daa1991eec8a90f9871488428cec6f3751d90b19d37c0455204cdfe3', 'dc3e5f78a38f0d449ecdc0f25007dc2dd8e636cc7ae17224374c2a5b52c89ea4', 'dc8314e95e93c6ad1af1380ac985d34a661362ccc0c4fc4a16c31ad456327432', 'dd7d1d2ccf0e3e9f9c6f97488de52763ea4360c839b1b86c39460893febdebbb', 'dd9df4269f123a3cf56b9b1a0c278278ac70b2595d9fba6f32e58eda03862192', 'de4261c33497443f14a6bd765194f04b4f8ffd2ff224d28b9108b047307e3162', 'df8fe6c519fce145a4eb8685379862f3c0a430f30400bb0bf013d9016696a5d8', 'e2492e24929618aa65205a54b8f7702a951a8d3fd4165cf624d2a2729dc66a8f', 'e3319713c696fa11fae8c9eaafacc5d06f67371965eb16989a21e735e84cdba4', 'e40ce7b69cda25565c7ea255d46f4f96f2838dbe5e72e615c094fcb9e1701c09', 'e4b0ef1d0b58fbed49d061ab92ef2fbfcbce631190e73c1a63bf7f851d71ad19', 'e56a021e003833b9a0ef1fbfa0f7f3a570a36983ed52b362871d1aa5f08121ed', 'e5ec68f3c1b43fb98e4dd25989c57f4f194a490728d316d043399ea70d3a0f0b', 'e6652fb9fd79798aeb91b54088bbff77df7749b7728eda737122d4753fc42bfe', 'e67528e932d4ee2b034305bcf13e4772ff93476905bf13d3f002006592bd958a', 'e6a00c2148f51c00d58d976ec1dff0b2340964a037d6d459470468dc77020468', 'e7bc45f84776f46c9237863b893bc36ffb2086643adfd88dbef3318e6c1c3951', 'e90235a52b45aca3be8b91213405452c497c989d1f27882b5bba2e873070f4d8', 'ea033dfd7862141cb938354a178593fac64de04cf30afda3742ebc0dcfeb89ce', 'ea4e70c6368982d5458688bb97512f00a53a938cbcbb900166e261d402c63866', 'eac4f7cfc12fc80076bf01b061e16174ae843fc94014cff3e737a4f6288f55fa', 'ec013c289b3dab92f9d31641608ba8e25160ca6d3575b87edbaad336dab0cb59', 'ecd42fccacc6ae03cc3866c48243ad008a921782adaae194b450968d5ba2cc9d', 'ef1d91ea9fe92e69cde3838ad8a6387bf5fa9e0dc03838ef88a1a6988ede27e2', 'f13fe86e5398aa1bc8a57dea2cfc0e34d9f36a5cfa1d4f83d65d37c96bde2edc', 'f236df26a25a40d790bec3e91db328b72ea48c51abc8fb1efe7be92a8195eb67', 'f24ab4aaac51ab543a189da8d9b6a951d363a17f4235ee0d11328fc3f4e93976', 'f2594e9a72d6993c1003179e2022c18bccf6dbcab53347b4c8863d9a22fb7853', 'f3b41ced450186c84536711e1236fd1a410fad8dc02102792a2b1c0f65566844', 'f42615343da2b9dc1e6e72769d10df1aa308eae9253b9b3e024f396b0000d425', 'f451873aee2eb7fa6fc4ab2f604f6bc6ca73fac694b57fbbcaf4caaba1c2e24c', 'f49773f53300aa4691353a4d70972aedcc6fd5de04f7419b16a5d48cfb8f4069', 'f52ba65605cd750af2247a7f113b4d447e1f3aec52d501f5bd93eb199742294a', 'f82c292cc2b0f27664a22281db1136eb8d54104db2728c4d8097d943a3d4d1f0', 'f914eec3b47885921bd9bba471a984f3484e6a7fb3a936ef42b8260454b02477', 'f9da97cb8f613d2b4e327a33b4e955dea379ed13be87b5adceb1eda5d0b575da', 'fa75c78d9cfe904afe7291231678124b578061f256dfbfebecf1ec2570ceabad', 'fcb8110e7fb5564fdb2e7fb609e9a3122bc63fa06356b54e616c8c8e82405dd6', 'fccc5e89fe8465de507f129c177387d3ee5d61d033240481dc77a026b1e4f35b', 'fd6426373555ce7649372ccebe634fe9a1fa94784ae722c1d0d31e61e5b71792', 'fe3a4b993e313f93d1bb735e3cc35ca8dfde70ec9203d673e6b0cac1de0a4314'))
KINDS = {
    "applicability", "prerequisite", "procedure_step", "decision_rule",
    "result_rule", "evidence_retention", "recommendation",
}
RIGHTS_ELEMENTS = (
    "identifiers", "titles", "structural_inventory", "paraphrases",
    "derivative_mapping_analysis", "official_links",
)
PROHIBITED_INFERENCES = (
    "certification", "compliance", "equivalence", "endorsement",
    "predictive_sufficiency", "full_population_assurance",
    "continuous_assurance", "current_scheme_completeness",
)

ACTORS = {
    "Assessor", "Applicant", "Certification Body", "Certifying Body",
    "Delivery Partner",
}
TOP_LEVEL_KEYS = {
    "schema_version", "atomization_rule_version", "scope", "source", "rights",
    "inventory_provenance", "direction_boundary", "operational_context",
    "known_anomalies", "groups", "section_ledger", "counts",
    "assurance_limits", "provisions",
}
LOCATOR_KEYS = {"pdf_page", "printed_page", "section", "detail"}
LANDING_PAGE = ROOT / "crosswalks/uk-cyber-essentials.md"
SCOPE_STATEMENT = (
    "This complete-publication oracle inventories the public NCSC Cyber Essentials "
    "Plus Test Specification v3.2. It is not a complete inventory of the current "
    "operational Cyber Essentials Plus scheme, Delivery Partner methodology, or "
    "certification process."
)
ORIGINAL_FREE_TEXT_PATHS = (
    re.compile(r"^scope\.statement$"),
    re.compile(r"^rights\.publication_basis$"),
    re.compile(r"^rights\.restrictions\[\d+\]$"),
    re.compile(r"^rights\.iasme_partition\.(?:permitted_facts|prohibited_source_derived_elements)\[\d+\]$"),
    re.compile(r"^operational_context\[\d+\]\.relevance$"),
    re.compile(r"^known_anomalies\[\d+\]\.treatment$"),
    re.compile(r"^section_ledger\[\d+\]\.rationale$"),
    re.compile(r"^provisions\[\d+\]\.(?:actor_basis|summary)$"),
    re.compile(r"^provisions\[\d+\]\.locator\.detail$"),
    re.compile(
        r"^assurance_limits\.(?:scope_boundary|population_and_sample_boundary|"
        r"assessment_date_boundary|evidence_date_boundary|tool_and_provenance_boundary|"
        r"point_in_time_boundary)$"
    ),
)
AFFIRMATIVE_PROHIBITED_CLAIMS = {
    "certification": (
        r"\b(?:provides|confers|establishes|demonstrates|proves|guarantees) (?:a )?certification\b",
        r"\bcertifies (?:the|an|any)\b",
    ),
    "compliance": (
        r"\b(?:provides|establishes|demonstrates|proves|guarantees) compliance\b",
        r"\b(?:is|are) compliant with\b",
    ),
    "equivalence": (
        r"\b(?:provides|establishes|demonstrates|proves|guarantees) equivalence\b",
        r"\b(?:is|are) equivalent to\b",
    ),
    "endorsement": (
        r"\b(?:provides|establishes|demonstrates|proves|guarantees) endorsement\b",
        r"\b(?:is|are) endorsed by\b",
        r"\b(?:has|carries|receives) (?:NCSC |IASME |government )?endorsement\b",
        r"\b(?:NCSC|IASME) endorses\b",
    ),
    "predictive_sufficiency": (
        r"\b(?:provides|establishes|demonstrates|proves|guarantees) predictive sufficiency\b",
        r"\b(?:is|are) sufficient to predict\b",
        r"\bpredicts future (?:security|compliance|performance|outcomes?)\b",
    ),
    "full_population_assurance": (
        r"\b(?:provides|establishes|demonstrates|proves|guarantees) full[- ]population assurance\b",
        r"\bassures (?:the )?(?:entire|full) population\b",
    ),
    "continuous_assurance": (
        r"\b(?:provides|establishes|demonstrates|proves|guarantees) continuous assurance\b",
    ),
    "current_scheme_completeness": (
        r"\b(?:is|provides|establishes) (?:a )?complete inventory of the current operational\b",
        r"\bfully describes the current (?:operational )?scheme\b",
    ),
}


class CyberEssentialsPlusV32InventoryTests(unittest.TestCase):
    def oracle(self) -> dict:
        return json.loads(ORACLE.read_text(encoding="utf-8"))

    def assert_exact_keys(self, value: object, expected: set[str]) -> dict:
        self.assertIsInstance(value, dict)
        assert isinstance(value, dict)
        self.assertEqual(expected, set(value))
        return value

    def assert_nonempty_string(self, value: object) -> str:
        self.assertIsInstance(value, str)
        assert isinstance(value, str)
        self.assertEqual(value, value.strip())
        self.assertTrue(value)
        return value

    def assert_nonnegative_integer(self, value: object) -> int:
        self.assertIs(type(value), int)
        assert isinstance(value, int)
        self.assertGreaterEqual(value, 0)
        return value

    def assert_positive_integer(self, value: object) -> int:
        number = self.assert_nonnegative_integer(value)
        self.assertGreater(number, 0)
        return number

    def assert_date(self, value: object) -> str:
        text = self.assert_nonempty_string(value)
        self.assertRegex(text, r"^\d{4}-(?:0[1-9]|1[0-2])-(?:0[1-9]|[12]\d|3[01])$")
        try:
            date.fromisoformat(text)
        except ValueError:
            self.fail(f"invalid calendar date: {text}")
        return text

    def assert_uri(self, value: object) -> str:
        text = self.assert_nonempty_string(value)
        self.assertRegex(text, r"^https://[^\s]+$")
        return text

    def assert_sha256(self, value: object) -> str:
        text = self.assert_nonempty_string(value)
        self.assertRegex(text, r"^[0-9a-f]{64}$")
        return text

    def assert_unique_strings(self, value: object, *, nonempty: bool = False) -> list[str]:
        self.assertIsInstance(value, list)
        assert isinstance(value, list)
        if nonempty:
            self.assertTrue(value)
        for item in value:
            self.assert_nonempty_string(item)
        self.assertEqual(len(value), len(set(value)))
        return value

    def assert_locator(self, value: object) -> dict:
        locator = self.assert_exact_keys(value, LOCATOR_KEYS)
        self.assert_positive_integer(locator["pdf_page"])
        if locator["printed_page"] is not None:
            self.assert_positive_integer(locator["printed_page"])
        self.assert_nonempty_string(locator["section"])
        self.assert_nonempty_string(locator["detail"])
        return locator

    def assert_page_range(self, value: object) -> dict:
        page_range = self.assert_exact_keys(value, {"start", "end"})
        start = self.assert_positive_integer(page_range["start"])
        end = self.assert_positive_integer(page_range["end"])
        self.assertLessEqual(start, end)
        return page_range

    def walk(self, value: object, path: str = "") -> list[tuple[str, object]]:
        found = [(path, value)]
        if isinstance(value, dict):
            for key, child in value.items():
                child_path = f"{path}.{key}" if path else key
                found.extend(self.walk(child, child_path))
        elif isinstance(value, list):
            for index, child in enumerate(value):
                found.extend(self.walk(child, f"{path}[{index}]"))
        return found

    def original_free_text(self, oracle: object) -> list[tuple[str, str]]:
        return [
            (path, value)
            for path, value in self.walk(oracle)
            if isinstance(value, str)
            and any(pattern.fullmatch(path) for pattern in ORIGINAL_FREE_TEXT_PATHS)
        ]

    def normalized_prose(self, value: str) -> str:
        return " ".join(re.findall(r"[a-z0-9%]+", value.lower()))

    def assert_no_copied_source_passages(
        self, oracle: object, source_passages: list[str], *, minimum_words: int = 5,
    ) -> None:
        normalized_passages = [
            self.normalized_prose(passage) for passage in source_passages
        ]
        for path, value in self.original_free_text(oracle):
            normalized_value = self.normalized_prose(value)
            if len(normalized_value.split()) < minimum_words:
                continue
            for passage in normalized_passages:
                if normalized_value in passage or passage in normalized_value:
                    self.fail(f"copied source passage found at {path}: {value!r}")

    def assert_no_copied_source_passage_digests(self, oracle: object) -> None:
        for path, value in self.original_free_text(oracle):
            normalized_value = self.normalized_prose(value)
            if len(normalized_value.split()) < 5:
                continue
            digest = hashlib.sha256(normalized_value.encode("utf-8")).hexdigest()
            self.assertNotIn(
                digest, SOURCE_PASSAGE_DIGESTS,
                f"normalized source passage digest reproduced at {path}",
            )

    def assert_no_affirmative_prohibited_claims(self, text: str) -> None:
        for category, claims in AFFIRMATIVE_PROHIBITED_CLAIMS.items():
            for claim in claims:
                self.assertIsNone(
                    re.search(claim, text, flags=re.IGNORECASE),
                    f"affirmative {category} claim matched {claim!r}",
                )

    def git(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["git", *args], cwd=ROOT, text=True, capture_output=True, check=False,
        )

    def test_locked_oracle_exists(self) -> None:
        self.assertTrue(ORACLE.is_file())

    def test_copied_source_text_detector_covers_all_original_free_text(self) -> None:
        source_passages = [
            "The assessor must preserve every relevant evidence record for the assessment.",
            "A complete scheme description includes all current operational methods and rules.",
        ]
        copied_summary = {
            "provisions": [{
                "summary": "The assessor must preserve every relevant evidence record for the assessment",
            }],
        }
        copied_scope = {
            "scope": {
                "statement": "A complete scheme description includes all current operational methods and rules",
            },
        }
        for candidate, path in (
            (copied_summary, "provisions[0].summary"),
            (copied_scope, "scope.statement"),
        ):
            with self.assertRaisesRegex(AssertionError, re.escape(path)):
                self.assert_no_copied_source_passages(candidate, source_passages)

    def test_prohibited_claim_detector_covers_all_eight_categories(self) -> None:
        affirmative_examples = {
            "certification": "The oracle provides certification for the Applicant.",
            "compliance": "The Applicant is compliant with ESAF.",
            "equivalence": "The assessment establishes equivalence with ESAF.",
            "endorsement": "The publication is endorsed by NCSC.",
            "predictive_sufficiency": "The result is sufficient to predict future security.",
            "full_population_assurance": "The sample provides full population assurance.",
            "continuous_assurance": "The certificate guarantees continuous assurance.",
            "current_scheme_completeness": (
                "The oracle is a complete inventory of the current operational scheme."
            ),
        }
        self.assertEqual(set(PROHIBITED_INFERENCES), set(affirmative_examples))
        for category, example in affirmative_examples.items():
            with self.assertRaisesRegex(AssertionError, category):
                self.assert_no_affirmative_prohibited_claims(example)
        self.assert_no_affirmative_prohibited_claims(
            "The oracle does not provide certification, demonstrate compliance, "
            "or establish continuous assurance."
        )

    def test_date_parser_rejects_impossible_calendar_dates(self) -> None:
        self.assertEqual("2026-07-14", self.assert_date("2026-07-14"))
        with self.assertRaisesRegex(AssertionError, "invalid calendar date"):
            self.assert_date("2026-02-31")

    @unittest.skipUnless(ORACLE.is_file(), "locked oracle is intentionally absent")
    def test_source_identity_is_exact(self) -> None:
        oracle = self.oracle()
        source = oracle["source"]
        self.assertEqual(SOURCE_TITLE, source["title"])
        self.assertEqual(SOURCE_AUTHORITY, source["authority"])
        self.assertEqual(PUBLICATION_IDENTIFIER, source["publication_identifier"])
        self.assertEqual("3.2", source["version"])
        self.assertEqual(DISPLAY_DATE, source["display_date"])
        self.assertEqual(RESOURCE_PAGE, source["resource_page_url"])
        self.assertEqual(RESOURCE_PAGE_DATE, source["resource_page_date"])
        self.assertEqual(24, source["pdf_page_count"])
        self.assertEqual(
            [("canonical", CANONICAL_URL, CANONICAL_BYTES, CANONICAL_SHA256),
             ("legacy", LEGACY_URL, LEGACY_BYTES, LEGACY_SHA256)],
            [(v["role"], v["url"], v["byte_length"], v["sha256"])
             for v in source["variants"]],
        )

    @unittest.skipUnless(ORACLE.is_file(), "locked oracle is intentionally absent")
    def test_closed_contract_versions_scope_source_and_groups(self) -> None:
        oracle = self.assert_exact_keys(self.oracle(), TOP_LEVEL_KEYS)
        self.assertEqual("1.0.0", oracle["schema_version"])
        self.assertEqual("1.0.0", oracle["atomization_rule_version"])

        scope = self.assert_exact_keys(oracle["scope"], {"type", "statement"})
        self.assertEqual("complete_publication", scope["type"])
        self.assertEqual(SCOPE_STATEMENT, scope["statement"])

        source = self.assert_exact_keys(
            oracle["source"],
            {"title", "authority", "publication_identifier", "version",
             "display_date", "resource_page_url", "resource_page_date",
             "access_date", "media_type", "pdf_page_count", "variants"},
        )
        for key in ("title", "authority", "publication_identifier", "version",
                    "display_date", "media_type"):
            self.assert_nonempty_string(source[key])
        self.assert_uri(source["resource_page_url"])
        self.assert_date(source["resource_page_date"])
        self.assertEqual("2026-07-14", self.assert_date(source["access_date"]))
        self.assertEqual("application/pdf", source["media_type"])
        self.assert_positive_integer(source["pdf_page_count"])
        self.assertIsInstance(source["variants"], list)
        self.assertEqual(2, len(source["variants"]))
        for variant in source["variants"]:
            item = self.assert_exact_keys(
                variant, {"role", "url", "byte_length", "sha256"},
            )
            self.assertIn(item["role"], {"canonical", "legacy"})
            self.assert_uri(item["url"])
            self.assert_positive_integer(item["byte_length"])
            self.assert_sha256(item["sha256"])
        self.assertEqual(list(GROUPS), oracle["groups"])

    @unittest.skipUnless(ORACLE.is_file(), "locked oracle is intentionally absent")
    def test_rights_contract_is_exact_and_separates_iasme(self) -> None:
        rights = self.assert_exact_keys(
            self.oracle()["rights"],
            {"copyright", "licence_name", "licence_url", "attribution",
             "publication_basis", "permitted_elements", "prohibited_elements",
             "copied_requirement_or_passage_text_prohibited",
             "allowed_verbatim_locations", "restrictions", "iasme_partition",
             "review"},
        )
        self.assertEqual("Crown copyright", rights["copyright"])
        self.assertEqual("Open Government Licence v3.0", rights["licence_name"])
        self.assertEqual(
            "https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/",
            self.assert_uri(rights["licence_url"]),
        )
        self.assertEqual(SOURCE_AUTHORITY, rights["attribution"])
        publication_basis = self.assert_nonempty_string(rights["publication_basis"])
        self.assertIn("Open Government Licence v3.0", publication_basis)
        permitted = self.assert_unique_strings(rights["permitted_elements"])
        prohibited = self.assert_unique_strings(rights["prohibited_elements"])
        self.assertEqual(list(RIGHTS_ELEMENTS), permitted)
        self.assertEqual([], prohibited)
        self.assertFalse(set(permitted) & set(prohibited))
        self.assertEqual(set(RIGHTS_ELEMENTS), set(permitted) | set(prohibited))
        self.assertIs(rights["copied_requirement_or_passage_text_prohibited"], True)
        self.assertEqual(
            ["known_anomalies[0].source_literal"],
            rights["allowed_verbatim_locations"],
        )
        restrictions = " ".join(
            self.assert_unique_strings(rights["restrictions"], nonempty=True)
        ).lower()
        for restricted in ("logo", "mark", "imag", "third-party", "endorsement"):
            self.assertIn(restricted, restrictions)

        iasme = self.assert_exact_keys(
            rights["iasme_partition"],
            {"owner", "licence", "permitted_facts",
             "prohibited_source_derived_elements"},
        )
        self.assertIn("IASME", self.assert_nonempty_string(iasme["owner"]))
        self.assertIsNone(iasme["licence"])
        self.assert_unique_strings(iasme["permitted_facts"], nonempty=True)
        self.assert_unique_strings(
            iasme["prohibited_source_derived_elements"], nonempty=True,
        )

        review = self.assert_exact_keys(
            rights["review"],
            {"reviewer", "review_date", "independent_of_inventory_authors",
             "canonical_sha256", "legacy_sha256", "publication_basis_verified",
             "disposition"},
        )
        self.assert_nonempty_string(review["reviewer"])
        self.assert_date(review["review_date"])
        self.assertIs(review["independent_of_inventory_authors"], True)
        self.assertEqual(CANONICAL_SHA256, self.assert_sha256(review["canonical_sha256"]))
        self.assertEqual(LEGACY_SHA256, self.assert_sha256(review["legacy_sha256"]))
        self.assertIs(review["publication_basis_verified"], True)
        self.assertEqual("approved", review["disposition"])

    @unittest.skipUnless(ORACLE.is_file(), "locked oracle is intentionally absent")
    def test_inventory_provenance_and_rights_commit_precedence(self) -> None:
        oracle = self.oracle()
        provenance = self.assert_exact_keys(
            oracle["inventory_provenance"],
            {"authors", "reconciler", "rights_record_commit",
             "inventories_started_after_rights_commit"},
        )
        authors = self.assert_unique_strings(provenance["authors"], nonempty=True)
        self.assertEqual(2, len(authors))
        self.assert_nonempty_string(provenance["reconciler"])
        rights_sha = self.assert_nonempty_string(provenance["rights_record_commit"])
        self.assertRegex(rights_sha, r"^[0-9a-f]{40}$")
        self.assertIs(provenance["inventories_started_after_rights_commit"], True)
        reviewer = oracle["rights"]["review"]["reviewer"]
        self.assertNotIn(reviewer, authors)

        commit_check = self.git("cat-file", "-e", f"{rights_sha}^{{commit}}")
        self.assertEqual(0, commit_check.returncode, commit_check.stderr)
        relative_rights_review = RIGHTS_REVIEW.relative_to(ROOT).as_posix()
        rights_history = self.git(
            "log", "--diff-filter=A", "--format=%H", "--", relative_rights_review,
        )
        self.assertEqual(0, rights_history.returncode, rights_history.stderr)
        self.assertEqual([rights_sha], rights_history.stdout.splitlines())
        rights_introduction = self.git(
            "diff-tree", "--root", "--no-commit-id", "--name-status", "-r",
            rights_sha,
        )
        self.assertEqual(0, rights_introduction.returncode, rights_introduction.stderr)
        self.assertEqual(
            f"A\t{relative_rights_review}", rights_introduction.stdout.strip(),
        )
        relative_oracle = ORACLE.relative_to(ROOT).as_posix()
        history = self.git(
            "log", "--diff-filter=A", "--format=%H", "--", relative_oracle,
        )
        self.assertEqual(0, history.returncode, history.stderr)
        inventory_commits = history.stdout.splitlines()
        self.assertLessEqual(len(inventory_commits), 1)
        first_inventory_commit = inventory_commits[0] if inventory_commits else "HEAD"
        candidate_parent = f"{first_inventory_commit}^" if inventory_commits else first_inventory_commit
        precedence = self.git(
            "merge-base", "--is-ancestor", rights_sha, candidate_parent,
        )
        self.assertEqual(
            0, precedence.returncode,
            "rights approval must precede the first source-derived inventory commit",
        )

    @unittest.skipUnless(ORACLE.is_file(), "locked oracle is intentionally absent")
    def test_direction_context_and_anomaly_objects_are_closed(self) -> None:
        oracle = self.oracle()
        direction = self.assert_exact_keys(
            oracle["direction_boundary"],
            {"oracle_establishes_mapping_direction", "future_directions",
             "assessed_independently"},
        )
        self.assertIs(direction["oracle_establishes_mapping_direction"], False)
        self.assertEqual(
            ["esaf_to_external", "external_to_esaf"],
            direction["future_directions"],
        )
        self.assertIs(direction["assessed_independently"], True)

        self.assertIsInstance(oracle["operational_context"], list)
        for context_value in oracle["operational_context"]:
            context = self.assert_exact_keys(
                context_value,
                {"owner", "title", "url", "publication_date", "access_date",
                 "relevance", "rights_partition"},
            )
            for key in ("owner", "title", "relevance"):
                self.assert_nonempty_string(context[key])
            self.assert_uri(context["url"])
            self.assert_date(context["publication_date"])
            self.assert_date(context["access_date"])
            self.assertEqual(
                "bibliographic_facts_and_original_context_only",
                context["rights_partition"],
            )

        self.assertIsInstance(oracle["known_anomalies"], list)
        self.assertEqual(1, len(oracle["known_anomalies"]))
        anomaly = self.assert_exact_keys(
            oracle["known_anomalies"][0],
            {"anomaly_id", "source_literal", "locator", "treatment"},
        )
        self.assert_nonempty_string(anomaly["anomaly_id"])
        self.assertEqual("tests 2 to 7", anomaly["source_literal"])
        self.assert_locator(anomaly["locator"])
        treatment = self.assert_nonempty_string(anomaly["treatment"]).lower()
        self.assertIn("without", treatment)
        self.assertRegex(treatment, r"correct|expand|interpret")

    @unittest.skipUnless(ORACLE.is_file(), "locked oracle is intentionally absent")
    def test_section_ledger_is_closed_and_link_counts_are_derived(self) -> None:
        oracle = self.oracle()
        ledger = oracle["section_ledger"]
        self.assertIsInstance(ledger, list)
        self.assertTrue(ledger)
        section_ids: list[str] = []
        ledger_by_id: dict[str, dict] = {}
        for occurrence_value in ledger:
            occurrence = self.assert_exact_keys(
                occurrence_value,
                {"section_id", "parent_section_id", "heading", "group",
                 "pdf_pages", "printed_pages", "decision", "rationale",
                 "atom_count"},
            )
            section_id = self.assert_nonempty_string(occurrence["section_id"])
            self.assertRegex(section_id, r"^sec-[a-z0-9]+(?:-[a-z0-9]+)*$")
            section_ids.append(section_id)
            ledger_by_id[section_id] = occurrence
            if occurrence["parent_section_id"] is not None:
                self.assert_nonempty_string(occurrence["parent_section_id"])
            self.assert_nonempty_string(occurrence["heading"])
            self.assertIn(occurrence["group"], GROUPS)
            self.assert_page_range(occurrence["pdf_pages"])
            if occurrence["printed_pages"] is not None:
                self.assert_page_range(occurrence["printed_pages"])
            self.assertIn(occurrence["decision"], {"included", "context_only"})
            self.assert_nonempty_string(occurrence["rationale"])
            self.assert_nonnegative_integer(occurrence["atom_count"])
        self.assertEqual(len(section_ids), len(set(section_ids)))
        for occurrence in ledger:
            parent = occurrence["parent_section_id"]
            if parent is not None:
                self.assertIn(parent, ledger_by_id)

        actual_occurrences = tuple(
            (
                item["section_id"], item["parent_section_id"], item["heading"],
                item["group"], item["pdf_pages"]["start"], item["pdf_pages"]["end"],
                None if item["printed_pages"] is None else item["printed_pages"]["start"],
                None if item["printed_pages"] is None else item["printed_pages"]["end"],
                item["decision"],
            )
            for item in ledger
        )
        self.assertEqual(EXPECTED_SECTION_OCCURRENCES, actual_occurrences)
        self.assertEqual(EXPECTED_SECTION_IDS, tuple(section_ids))

        links = Counter(item["section_id"] for item in oracle["provisions"])
        for section_id, occurrence in ledger_by_id.items():
            self.assertEqual(links[section_id], occurrence["atom_count"])
            if occurrence["decision"] == "context_only":
                self.assertEqual(0, links[section_id])

    @unittest.skipUnless(ORACLE.is_file(), "locked oracle is intentionally absent")
    def test_provisions_are_closed_controlled_linked_and_ordered(self) -> None:
        oracle = self.oracle()
        provisions = oracle["provisions"]
        self.assertIsInstance(provisions, list)
        self.assertTrue(provisions)
        ledger = {item["section_id"]: item for item in oracle["section_ledger"]}
        record_ids: list[str] = []
        external_ids: list[str] = []
        order_keys: list[tuple[int, int]] = []
        for provision_value in provisions:
            provision = self.assert_exact_keys(
                provision_value,
                {"record_id", "external_provision_id", "section_id", "group",
                 "kind", "actors", "actor_basis", "source_assigned_label",
                 "summary", "locator"},
            )
            group = provision["group"]
            self.assertIn(group, GROUPS)
            record_id = self.assert_nonempty_string(provision["record_id"])
            external_id = self.assert_nonempty_string(
                provision["external_provision_id"],
            )
            self.assertRegex(record_id, rf"^cepts32-{group.lower()}-\d{{3}}$")
            self.assertRegex(external_id, rf"^CEPTS3\.2-{group}-\d{{3}}$")
            self.assertEqual(record_id.rsplit("-", 1)[1], external_id.rsplit("-", 1)[1])
            record_ids.append(record_id)
            external_ids.append(external_id)
            order_keys.append((GROUPS.index(group), int(record_id.rsplit("-", 1)[1])))
            section_id = self.assert_nonempty_string(provision["section_id"])
            self.assertIn(section_id, ledger)
            self.assertEqual("included", ledger[section_id]["decision"])
            self.assertEqual(group, ledger[section_id]["group"])
            self.assertIn(provision["kind"], KINDS)
            actors = self.assert_unique_strings(provision["actors"], nonempty=True)
            self.assertLessEqual(set(actors), ACTORS)
            actor_basis = self.assert_nonempty_string(provision["actor_basis"])
            locator = self.assert_locator(provision["locator"])
            if len(actors) > 1:
                for actor in actors:
                    self.assertIn(actor, actor_basis)
                self.assertTrue(locator["detail"])
            if provision["source_assigned_label"] is not None:
                self.assert_nonempty_string(provision["source_assigned_label"])
                self.assertNotIn(provision["source_assigned_label"], locator.values())
            self.assert_nonempty_string(provision["summary"])
        self.assertEqual(len(record_ids), len(set(record_ids)))
        self.assertEqual(len(external_ids), len(set(external_ids)))
        self.assertEqual(sorted(order_keys), order_keys)
        for group in GROUPS:
            group_numbers = [
                number for group_index, number in order_keys
                if group_index == GROUPS.index(group)
            ]
            self.assertEqual(list(range(1, len(group_numbers) + 1)), group_numbers)

    @unittest.skipUnless(ORACLE.is_file(), "locked oracle is intentionally absent")
    def test_counts_are_derived_and_equal_reconciled_constants(self) -> None:
        oracle = self.oracle()
        counts = self.assert_exact_keys(oracle["counts"], {"total", "by_group"})
        by_group = self.assert_exact_keys(counts["by_group"], set(GROUPS))
        for value in by_group.values():
            self.assert_nonnegative_integer(value)
        self.assert_nonnegative_integer(counts["total"])
        derived = Counter(item["group"] for item in oracle["provisions"])
        self.assertEqual(
            {group: derived[group] for group in GROUPS},
            by_group,
        )
        self.assertEqual(len(oracle["provisions"]), counts["total"])
        self.assertEqual(counts["total"], sum(by_group.values()))
        self.assertEqual(
            counts["total"],
            sum(item["atom_count"] for item in oracle["section_ledger"]),
        )
        self.assertEqual(EXPECTED_COUNT, counts["total"])
        self.assertEqual(EXPECTED_GROUP_COUNTS, by_group)

    @unittest.skipUnless(ORACLE.is_file(), "locked oracle is intentionally absent")
    def test_assurance_limits_and_discretionary_exception_are_exact(self) -> None:
        limits = self.assert_exact_keys(
            self.oracle()["assurance_limits"],
            {"scope_boundary", "population_and_sample_boundary",
             "assessment_date_boundary", "evidence_date_boundary",
             "tool_and_provenance_boundary", "point_in_time_boundary",
             "discretion_owner", "discretionary_exception",
             "prohibited_inferences"},
        )
        for key in (
            "scope_boundary", "population_and_sample_boundary",
            "assessment_date_boundary", "evidence_date_boundary",
            "tool_and_provenance_boundary", "point_in_time_boundary",
        ):
            self.assert_nonempty_string(limits[key])
        self.assertEqual("Delivery Partner", limits["discretion_owner"])
        exception = self.assert_exact_keys(
            limits["discretionary_exception"],
            {"owner", "predicates", "all_predicates_required", "locator",
             "automatic_pass", "is_95_percent_score"},
        )
        self.assertEqual("Delivery Partner", exception["owner"])
        self.assertIs(exception["all_predicates_required"], True)
        self.assertIs(exception["automatic_pass"], False)
        self.assertIs(exception["is_95_percent_score"], False)
        self.assert_locator(exception["locator"])
        predicates = exception["predicates"]
        self.assertIsInstance(predicates, list)
        self.assertEqual(2, len(predicates))
        for predicate in predicates:
            self.assert_exact_keys(predicate, {"predicate_id", "meaning"})
        self.assertEqual(
            [
                ("marginal-deviation-under-five-percent",
                 "a marginal deviation in less than 5% of performed tests"),
                ("no-wider-process-failure-evidence",
                 "no evidence of wider failure of Applicant cybersecurity processes"),
            ],
            [(item["predicate_id"], item["meaning"]) for item in predicates],
        )
        self.assertEqual(list(PROHIBITED_INFERENCES), limits["prohibited_inferences"])

    @unittest.skipUnless(ORACLE.is_file(), "locked oracle is intentionally absent")
    def test_visual_decisions_and_anomaly_literal_are_complete(self) -> None:
        oracle = self.oracle()
        figure_labels = {
            item["source_assigned_label"]
            for item in oracle["provisions"]
            if isinstance(item["source_assigned_label"], str)
            and "Figure 1" in item["source_assigned_label"]
        }
        self.assertEqual(
            {f"Figure 1 decision {number}" for number in range(1, 8)},
            figure_labels,
        )
        literal_occurrences = [
            path for path, value in self.walk(oracle) if value == "tests 2 to 7"
        ]
        self.assertEqual(["known_anomalies[0].source_literal"], literal_occurrences)
        self.assertEqual(
            ["known_anomalies[0].source_literal"],
            oracle["rights"]["allowed_verbatim_locations"],
        )
        for provision in oracle["provisions"]:
            self.assertNotEqual("tests 2 to 7", provision["summary"])

    @unittest.skipUnless(ORACLE.is_file(), "locked oracle is intentionally absent")
    def test_original_free_text_excludes_source_copy_markers(self) -> None:
        free_text = self.original_free_text(self.oracle())
        self.assertTrue(free_text)
        for path, value in free_text:
            self.assertNotRegex(value, r"[\r\n•]", path)
            self.assertNotRegex(value, r"[\"“”]", path)
            self.assertNotRegex(value, r"\b(?:shall|must|should)\b", path)

    @unittest.skipUnless(ORACLE.is_file(), "locked oracle is intentionally absent")
    def test_original_free_text_does_not_reproduce_normalized_source_passages(self) -> None:
        self.assertTrue(SOURCE_PASSAGE_DIGESTS)
        self.assert_no_copied_source_passage_digests(self.oracle())

    @unittest.skipUnless(ORACLE.is_file(), "locked oracle is intentionally absent")
    def test_oracle_has_no_mapping_fields_or_prohibited_claim_phrases(self) -> None:
        oracle = self.oracle()
        prohibited_fields = {
            "mapping_disposition", "disposition_rationale", "relationships",
            "relationship", "esaf_control_id", "compliance_statistics",
            "mapping_statistics",
        }
        object_keys = {
            key
            for _, value in self.walk(oracle)
            if isinstance(value, dict)
            for key in value
        }
        self.assertFalse(prohibited_fields & object_keys)

        serialized = json.dumps(oracle, ensure_ascii=False)
        landing = LANDING_PAGE.read_text(encoding="utf-8")
        for text in (serialized, landing):
            self.assert_no_affirmative_prohibited_claims(text)

    @unittest.skipUnless(ORACLE.is_file(), "locked oracle is intentionally absent")
    def test_landing_page_publishes_plus_source_inventory_boundary(self) -> None:
        oracle = self.oracle()
        landing = LANDING_PAGE.read_text(encoding="utf-8")
        oracle_link = (
            "../docs/superpowers/specs/"
            "2026-07-14-uk-cyber-essentials-plus-v3.2-provision-oracle.json"
        )

        required_text = (
            oracle_link,
            oracle["source"]["resource_page_url"],
            oracle["source"]["variants"][0]["url"],
            oracle["source"]["variants"][1]["url"],
            f'{oracle["source"]["variants"][0]["byte_length"]:,} bytes',
            f'{oracle["source"]["variants"][1]["byte_length"]:,} bytes',
            f'{oracle["counts"]["total"]} provisions',
            "Cyber Essentials core v3.3",
            "Cyber Essentials Plus v3.2",
            "complete only for the pinned public v3.2 specification",
            "2026 operational context",
            "not consolidated into the public v3.2 PDF",
            "No Cyber Essentials Plus mapping snapshot exists",
            "not a complete inventory of the current operational Cyber Essentials Plus scheme",
            "does not establish certification",
        )
        for expected in required_text:
            with self.subTest(expected=expected):
                self.assertIn(expected, landing)

        self.assert_no_affirmative_prohibited_claims(landing)


if __name__ == "__main__":
    unittest.main()
