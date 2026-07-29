# v0.5 Beta Mermaid Rendering Baseline

Status: Baseline renderer capability verified; not closure candidate approval

Renderer version: `@mermaid-js/mermaid-cli@11.16.0`

Operational Node version: `22.23.1`

Render contract schema: `esaf-mermaid-render-contract-v1`

Render configuration: `tools/mermaid-render-config.json`

Canonical render configuration SHA-256: `2a144e5017e94d7e563d4573daa714ed5ca6608b05d4f1202a479b6f0a9c9e31`

## Scope and method

- Mermaid source baseline: `ebe050c2f21b900c75dfe3ad4e1a77fcb71ff957`
- Reviewer: Codex agent `/root/v05_task4_implementer`
- Inventory SHA-256: `7224aa1a517e0392f0777d90c92f2aace9bad143cbcabacb65d6d13806600a88`

The inventory was regenerated outside the repository from every Mermaid block in
tracked Markdown. The pinned renderer produced 23 scale-3 PNG files. The reviewer
inspected every render at full resolution and reconciled the path, block number,
source digest, labels, contrast, and diagram structure. The inventory contains
17 `flowchart`, 4 `sequenceDiagram`, and 2 `stateDiagram-v2` blocks.

Each render-contract digest is SHA-256 over the domain
`ESAF-MERMAID-RENDER-CONTRACT-V1\0` followed by canonical JSON encoded as UTF-8
without a byte-order mark or trailing newline. Canonical JSON uses sorted keys
and no insignificant whitespace. Its payload includes the exact Mermaid source,
source SHA-256, path, block ordinal, diagram type, renderer, Node version,
render options, and complete checked-in render configuration.

The render contract binds the inputs and requires the operational validator to
render every block successfully. It does not digest PNG bytes. Browser
rasterization can change antialiased pixels without changing the source or
review result, so PNG byte hashes are intentionally not a durable repository
invariant. `Visual Review` and the named Codex agent record the separate agent
visual inspection of the temporary scale-3 PNGs. This baseline is not human
review or approval.

This record proves renderer capability and establishes a baseline inventory.
It is not v0.5-beta closure-candidate approval. The exact closure head requires
fresh rendering, digest comparison, and visual review evidence.

## Disposition

All 23 blocks passed rendering and readability review. No clipped or obscured
label, unreadable density, unsafe contrast, missing node or edge, or semantic
mismatch was found. Critical: 0; Important: 0; Minor: 0.

| Path | Block | Source SHA-256 | Render Contract SHA-256 | Renderer | Profile | Visual Review | Reviewer |
|---|---:|---|---|---|---|---|---|
| `architectures/patterns/ARC-P110.md` | 1 | `c0806f3c6906762383359c293f8eaf34ef4f8c3b13950bc1addbc20a2b670322` | `803fd5421c0b3a000f18c453fd1ec59dc0b5da4bce928cca5cae0f47191f28b8` | `@mermaid-js/mermaid-cli@11.16.0` | `esaf-mermaid-review-v1` | Pass | /root/v05_task4_implementer |
| `architectures/patterns/ARC-P110.md` | 2 | `cee1ee91f40582eada11b7257fa434fc14ca7aa2c80b31f4d822cb78a44f6ab0` | `c69a2400510e17f14d503b24547de0b4799da2c8a336fd206bf34c2349755ad1` | `@mermaid-js/mermaid-cli@11.16.0` | `esaf-mermaid-review-v1` | Pass | /root/v05_task4_implementer |
| `architectures/patterns/ARC-P110.md` | 3 | `fec4b9368060f4502a53776c4f735a2e98075be2fab499a7e9fa7cc305f2ec02` | `36b87f5e9926960a7a885604767e1cefa198215e7c80ec41eb886b522a4c89d7` | `@mermaid-js/mermaid-cli@11.16.0` | `esaf-mermaid-review-v1` | Pass | /root/v05_task4_implementer |
| `architectures/patterns/ARC-P110.md` | 4 | `1c29810df4c8dc03d0eabab4a6f073f4b6f047c70e3ea4e566e1a249581ecb68` | `d24b9a391606f592bf9f43f71abd2fe9208de00c1d671a8e8381687e342da4ed` | `@mermaid-js/mermaid-cli@11.16.0` | `esaf-mermaid-review-v1` | Pass | /root/v05_task4_implementer |
| `architectures/patterns/ARC-P110.md` | 5 | `e625b81cb9beb16f59f0b382ce114454a057ac4957422dfc22183616f8f67f82` | `68e0f9b79f633bfa9c79b2c271f2ed0cdc743920d67a4e4b81dce37cb03dbaa7` | `@mermaid-js/mermaid-cli@11.16.0` | `esaf-mermaid-review-v1` | Pass | /root/v05_task4_implementer |
| `architectures/patterns/ARC-P140.md` | 1 | `7457863529be8e5c1c470b87007284c23c139208cf9ea450758a31def9caf961` | `c60bbf427bb5432c65051626761a3a07ccae8b1d590f64adf7ba04590c9de47d` | `@mermaid-js/mermaid-cli@11.16.0` | `esaf-mermaid-review-v1` | Pass | /root/v05_task4_implementer |
| `architectures/patterns/ARC-P140.md` | 2 | `2b7ea3425e5e35603960b7ce8bd098f0d07a6eb54cac4838282964e3096e2002` | `c3fd111cd1dee97ab228af67140ef55d16a73e62adbdf0dfcc1dd90f42fdd521` | `@mermaid-js/mermaid-cli@11.16.0` | `esaf-mermaid-review-v1` | Pass | /root/v05_task4_implementer |
| `architectures/patterns/ARC-P140.md` | 3 | `f39885cb4fe54bd69f0a62fec210e067bbee64d6d17d771ba972d212a8314f10` | `dffbf24ae59d4f65224a43776bf32317bbbdd51f532658a598edabc5482ba724` | `@mermaid-js/mermaid-cli@11.16.0` | `esaf-mermaid-review-v1` | Pass | /root/v05_task4_implementer |
| `architectures/patterns/ARC-P140.md` | 4 | `b1694418476cf1681cc20f602f23da781e890b218c6ffec6c9541621b6ef9b73` | `74f9d1a7dd82dcc11d850bed26cf69a145ec44b35c399c8b66383eed4e45cbc0` | `@mermaid-js/mermaid-cli@11.16.0` | `esaf-mermaid-review-v1` | Pass | /root/v05_task4_implementer |
| `architectures/patterns/ARC-P140.md` | 5 | `3fe61a8087715064b2f312821d916bbad4b228685fc24bb757ce6c782e573b2d` | `d755c1bb4d807015c945b618fa93d6a3575200c9573d6d1bb21633cef062c615` | `@mermaid-js/mermaid-cli@11.16.0` | `esaf-mermaid-review-v1` | Pass | /root/v05_task4_implementer |
| `architectures/patterns/ARC-P140.md` | 6 | `25615ca70a74e719055bd7c9f98f003dd0cd188c62b1e973efce17d87728f50e` | `3257c053db5e0fd7381a19d2eddbfe32da7df369c82d5ac466383f1181c6cc4c` | `@mermaid-js/mermaid-cli@11.16.0` | `esaf-mermaid-review-v1` | Pass | /root/v05_task4_implementer |
| `architectures/patterns/ARC-P140.md` | 7 | `5cc7576a5287849e2721965bc076b2f8f4bdbc4e137448fdc4ed0e836652da27` | `325c83d6843e1d4035a242b68bbbb7332a16f1341962f0490541e48a5b95f631` | `@mermaid-js/mermaid-cli@11.16.0` | `esaf-mermaid-review-v1` | Pass | /root/v05_task4_implementer |
| `architectures/patterns/ARC-P150.md` | 1 | `080130e0b53696fe980021ee64ce8637e49d7476c0a0e94c35de959a12df117b` | `06f85c085047f3e2a03198cb7cd93b18fd0d3d337face12822e687c96b7c6f64` | `@mermaid-js/mermaid-cli@11.16.0` | `esaf-mermaid-review-v1` | Pass | /root/v05_task4_implementer |
| `architectures/patterns/ARC-P150.md` | 2 | `0f8e3138187e49467e8cca2d2aaab1827377c01458dfe78e53899da9045605fc` | `7784bad65ee3babb5924f987e56b61226eefade25341efdfd549d3a0b94f159c` | `@mermaid-js/mermaid-cli@11.16.0` | `esaf-mermaid-review-v1` | Pass | /root/v05_task4_implementer |
| `architectures/patterns/ARC-P150.md` | 3 | `70899c758bad6726f22971732228372edeb3416e9e8637909b0f5a897bc5acc9` | `ba187deb51c0a43a0ba2e95fe18b3fde40d899072f556c6d3cf1af9aa4a25ada` | `@mermaid-js/mermaid-cli@11.16.0` | `esaf-mermaid-review-v1` | Pass | /root/v05_task4_implementer |
| `architectures/patterns/ARC-P150.md` | 4 | `d5608c90f9de9a5134367da22879e9d6514086c4d8b76da0c401a7fe86b005b0` | `360d3d64f9b0b6afbc4698ec4b2ae05475652384eebb2b0df97d019c79080e3f` | `@mermaid-js/mermaid-cli@11.16.0` | `esaf-mermaid-review-v1` | Pass | /root/v05_task4_implementer |
| `architectures/patterns/ARC-P150.md` | 5 | `311653b595cf65f99eebd0511db65f67aef044b732a2c53beeaebad115fb69f5` | `77280bffbdbd127fb4f0b75baff55973b6a916cda4d2a1800297959e802ee17c` | `@mermaid-js/mermaid-cli@11.16.0` | `esaf-mermaid-review-v1` | Pass | /root/v05_task4_implementer |
| `architectures/patterns/ARC-P150.md` | 6 | `01c302dff5110de5d4d034a621272db1239c85e41e2f2923fd83884ca93d28db` | `c4779e929c187326c7e7b93b1d49a46fa58da4b83810dca3b0da9aaa9985cd0b` | `@mermaid-js/mermaid-cli@11.16.0` | `esaf-mermaid-review-v1` | Pass | /root/v05_task4_implementer |
| `architectures/patterns/ARC-P150.md` | 7 | `ea59ac316fdeb90a2efc645f18f802e56a2c11a80d6ce86fac617b4b69b9f353` | `c25c79f20ac67de86200d8e1ddb0d9995e35b53b8eb15342f2aa1a3b7f66fa69` | `@mermaid-js/mermaid-cli@11.16.0` | `esaf-mermaid-review-v1` | Pass | /root/v05_task4_implementer |
| `architectures/patterns/ARC-P160.md` | 1 | `770e85f6e5e29cf31e09da24911f287e8b419bb54c43be9908f0d51b0516596e` | `30ccc7cf799555d2e48fa3123677b2e782b3b22edef4638f61fa01914ec02542` | `@mermaid-js/mermaid-cli@11.16.0` | `esaf-mermaid-review-v1` | Pass | /root/v05_task4_implementer |
| `architectures/patterns/ARC-P160.md` | 2 | `bc5894d1fef8daf3569b56025caeee0877a41068e00d5959d9dc5ec7e32bd140` | `907738b0d4d90f7551d999a0371e274401ec4cbdf3268a688f58bf6c04cc3c73` | `@mermaid-js/mermaid-cli@11.16.0` | `esaf-mermaid-review-v1` | Pass | /root/v05_task4_implementer |
| `architectures/patterns/ARC-P160.md` | 3 | `2a9934615a189b47a9a4d9dc3478397af6119efd81f9a25c1e96f2cd5394e7c0` | `d4b2d65a541dcf803f7d4407414d5b0cb06802bebf7b0b2afff3cb4c9c4efc2e` | `@mermaid-js/mermaid-cli@11.16.0` | `esaf-mermaid-review-v1` | Pass | /root/v05_task4_implementer |
| `architectures/patterns/ARC-P160.md` | 4 | `479a43198c3f0e1d32b35d44350507a77c5f3a6726c479e97c6ac4f968acebb3` | `c7af2e91c586f5539b633ff629e94ce8242368f45330858d006ed46bccdfe012` | `@mermaid-js/mermaid-cli@11.16.0` | `esaf-mermaid-review-v1` | Pass | /root/v05_task4_implementer |

## Limitations

This baseline does not constitute technical, governance, release-scope,
qualified mapping, publication, closure-candidate, or tag approval.
