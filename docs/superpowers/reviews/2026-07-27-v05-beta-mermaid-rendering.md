# v0.5 Beta Mermaid Rendering Baseline

Status: Baseline renderer capability verified; not closure candidate approval

Renderer version: `@mermaid-js/mermaid-cli@11.16.0`

## Scope and method

- Mermaid source baseline: `ebe050c2f21b900c75dfe3ad4e1a77fcb71ff957`
- Reviewer: `/root/v05_task4_implementer`
- Inventory SHA-256: `7224aa1a517e0392f0777d90c92f2aace9bad143cbcabacb65d6d13806600a88`

The inventory was regenerated outside the repository from every Mermaid block in
tracked Markdown. The pinned renderer produced 23 scale-3 PNG files. The reviewer
inspected every render at full resolution and reconciled the path, block number,
source digest, output digest, labels, contrast, and diagram structure. The
inventory contains 17 `flowchart`, 4 `sequenceDiagram`, and 2
`stateDiagram-v2` blocks.

This record proves renderer capability and establishes a baseline inventory.
It is not v0.5-beta closure-candidate approval. The exact closure head requires
fresh rendering, digest comparison, and visual review evidence.

## Disposition

All 23 blocks passed rendering and readability review. No clipped or obscured
label, unreadable density, unsafe contrast, missing node or edge, or semantic
mismatch was found. Critical: 0; Important: 0; Minor: 0.

| Path | Block | Source SHA-256 | Output SHA-256 | Renderer | Result | Reviewer |
|---|---:|---|---|---|---|---|
| `architectures/patterns/ARC-P110.md` | 1 | `c0806f3c6906762383359c293f8eaf34ef4f8c3b13950bc1addbc20a2b670322` | `925b2c8f8cad6ab11fd93964125452d4821ba7a49482ef8472776e8cc6173f20` | `@mermaid-js/mermaid-cli@11.16.0` | Pass | /root/v05_task4_implementer |
| `architectures/patterns/ARC-P110.md` | 2 | `cee1ee91f40582eada11b7257fa434fc14ca7aa2c80b31f4d822cb78a44f6ab0` | `f65c6556211835dcc619e951a7e299d7cacad3bc1c1852c3f54a04a123320ea5` | `@mermaid-js/mermaid-cli@11.16.0` | Pass | /root/v05_task4_implementer |
| `architectures/patterns/ARC-P110.md` | 3 | `fec4b9368060f4502a53776c4f735a2e98075be2fab499a7e9fa7cc305f2ec02` | `ce16ec8615f95d17301054db0d35f7da88ac411ed95bb851a526abae456f26bc` | `@mermaid-js/mermaid-cli@11.16.0` | Pass | /root/v05_task4_implementer |
| `architectures/patterns/ARC-P110.md` | 4 | `1c29810df4c8dc03d0eabab4a6f073f4b6f047c70e3ea4e566e1a249581ecb68` | `000889f784f332995be747ae452a5972acb168155a30b14843cf7b329ebbdbee` | `@mermaid-js/mermaid-cli@11.16.0` | Pass | /root/v05_task4_implementer |
| `architectures/patterns/ARC-P110.md` | 5 | `e625b81cb9beb16f59f0b382ce114454a057ac4957422dfc22183616f8f67f82` | `7a87685250fdd6708229a32c2084b3d7b3d82235023a3ed698ab7d05ede7a2be` | `@mermaid-js/mermaid-cli@11.16.0` | Pass | /root/v05_task4_implementer |
| `architectures/patterns/ARC-P140.md` | 1 | `7457863529be8e5c1c470b87007284c23c139208cf9ea450758a31def9caf961` | `3652b9ad209f8adb63e27438550c365238ee0f97a7fcd30ab1426fd58c52786a` | `@mermaid-js/mermaid-cli@11.16.0` | Pass | /root/v05_task4_implementer |
| `architectures/patterns/ARC-P140.md` | 2 | `2b7ea3425e5e35603960b7ce8bd098f0d07a6eb54cac4838282964e3096e2002` | `29778e76c95257ba521d566ac228c1b5c07ebe35c31940b2845036d92fceee04` | `@mermaid-js/mermaid-cli@11.16.0` | Pass | /root/v05_task4_implementer |
| `architectures/patterns/ARC-P140.md` | 3 | `f39885cb4fe54bd69f0a62fec210e067bbee64d6d17d771ba972d212a8314f10` | `f132384b186770410e7bf0746aba28019a41ac57b6cd460cca08946dabf6de9c` | `@mermaid-js/mermaid-cli@11.16.0` | Pass | /root/v05_task4_implementer |
| `architectures/patterns/ARC-P140.md` | 4 | `b1694418476cf1681cc20f602f23da781e890b218c6ffec6c9541621b6ef9b73` | `111a460b47ec9e6079115d49d317f1bc947de8cdb7fdb2caec621e7dc54a9cea` | `@mermaid-js/mermaid-cli@11.16.0` | Pass | /root/v05_task4_implementer |
| `architectures/patterns/ARC-P140.md` | 5 | `3fe61a8087715064b2f312821d916bbad4b228685fc24bb757ce6c782e573b2d` | `5fca34b1f8339409827e7adccc1b30c04116156ee30d7295a4c0563af7476986` | `@mermaid-js/mermaid-cli@11.16.0` | Pass | /root/v05_task4_implementer |
| `architectures/patterns/ARC-P140.md` | 6 | `25615ca70a74e719055bd7c9f98f003dd0cd188c62b1e973efce17d87728f50e` | `0776c885d7ac92b40f9bc62b92dc3cd1deb1c12f4c5bee7631a00a60412bfcaa` | `@mermaid-js/mermaid-cli@11.16.0` | Pass | /root/v05_task4_implementer |
| `architectures/patterns/ARC-P140.md` | 7 | `5cc7576a5287849e2721965bc076b2f8f4bdbc4e137448fdc4ed0e836652da27` | `8d01e0dc2d5834e985033a659653f82a456f0543a2105c47374b51143b48ef93` | `@mermaid-js/mermaid-cli@11.16.0` | Pass | /root/v05_task4_implementer |
| `architectures/patterns/ARC-P150.md` | 1 | `080130e0b53696fe980021ee64ce8637e49d7476c0a0e94c35de959a12df117b` | `7f7418054034cf7b47114414b3a0ce1567ab83696651910241d98efffef10f30` | `@mermaid-js/mermaid-cli@11.16.0` | Pass | /root/v05_task4_implementer |
| `architectures/patterns/ARC-P150.md` | 2 | `0f8e3138187e49467e8cca2d2aaab1827377c01458dfe78e53899da9045605fc` | `7150907cdcb0c374a87c906d92fad8dd4930ed1036a5e6bf65b60e0c943198bb` | `@mermaid-js/mermaid-cli@11.16.0` | Pass | /root/v05_task4_implementer |
| `architectures/patterns/ARC-P150.md` | 3 | `70899c758bad6726f22971732228372edeb3416e9e8637909b0f5a897bc5acc9` | `65e402d2f9ef517934c63041e4f52f09ff7a70fc32695209000ad6bdb9693302` | `@mermaid-js/mermaid-cli@11.16.0` | Pass | /root/v05_task4_implementer |
| `architectures/patterns/ARC-P150.md` | 4 | `d5608c90f9de9a5134367da22879e9d6514086c4d8b76da0c401a7fe86b005b0` | `05d657ea7a6a641be2c038644607017a8d82ef2f770ba7138cf8f0a896a66d32` | `@mermaid-js/mermaid-cli@11.16.0` | Pass | /root/v05_task4_implementer |
| `architectures/patterns/ARC-P150.md` | 5 | `311653b595cf65f99eebd0511db65f67aef044b732a2c53beeaebad115fb69f5` | `b4fb42d0d754660b6fd996f36ee544cc65013021636a9fd7f32de89b4536b5a5` | `@mermaid-js/mermaid-cli@11.16.0` | Pass | /root/v05_task4_implementer |
| `architectures/patterns/ARC-P150.md` | 6 | `01c302dff5110de5d4d034a621272db1239c85e41e2f2923fd83884ca93d28db` | `049e7c9adcf5ffabd6d0c7f108b4417621ae6ca2c208e8f23baeb93df0012934` | `@mermaid-js/mermaid-cli@11.16.0` | Pass | /root/v05_task4_implementer |
| `architectures/patterns/ARC-P150.md` | 7 | `ea59ac316fdeb90a2efc645f18f802e56a2c11a80d6ce86fac617b4b69b9f353` | `a0b0a479ccec81381cfbadc20889b0ac9b44af20b4788cc6922b1fefabed6070` | `@mermaid-js/mermaid-cli@11.16.0` | Pass | /root/v05_task4_implementer |
| `architectures/patterns/ARC-P160.md` | 1 | `770e85f6e5e29cf31e09da24911f287e8b419bb54c43be9908f0d51b0516596e` | `df3fe49e66d16f0ca544f22e37134bd281ac390a4a372123026e3666e187eb68` | `@mermaid-js/mermaid-cli@11.16.0` | Pass | /root/v05_task4_implementer |
| `architectures/patterns/ARC-P160.md` | 2 | `bc5894d1fef8daf3569b56025caeee0877a41068e00d5959d9dc5ec7e32bd140` | `6bf1ade3488830b438ab0cfa1c34d825fb2413cbfcc940518d2df85ccf054721` | `@mermaid-js/mermaid-cli@11.16.0` | Pass | /root/v05_task4_implementer |
| `architectures/patterns/ARC-P160.md` | 3 | `2a9934615a189b47a9a4d9dc3478397af6119efd81f9a25c1e96f2cd5394e7c0` | `2e5a979c028e42d78c79e80c28c70a7ab3faccc043521bf0c53cf2e0fffc3e95` | `@mermaid-js/mermaid-cli@11.16.0` | Pass | /root/v05_task4_implementer |
| `architectures/patterns/ARC-P160.md` | 4 | `479a43198c3f0e1d32b35d44350507a77c5f3a6726c479e97c6ac4f968acebb3` | `8e9deae3ebf3b0ba3eb805824acc7eaad7115fac77c62dafc43a9a9494fd3147` | `@mermaid-js/mermaid-cli@11.16.0` | Pass | /root/v05_task4_implementer |

## Limitations

This baseline does not constitute technical, governance, release-scope,
qualified mapping, publication, closure-candidate, or tag approval.
