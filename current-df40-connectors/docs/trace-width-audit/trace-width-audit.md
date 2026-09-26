# Trace-width triage

Board SHA-256: `a0ff38390075833beac6046379897b9fefbec22a8d634a2b91211595034d99cc`

**164 width-changing contacts at 129 locations.** Coordinates are millimetres relative to the drill/auxiliary origin.

## Categories

- constrained_run_review: **6**
- terminal_escape_review: **15**
- branch_review: **42**
- overlap_topology_review: **101**

Contact types: {'endpoint': 45, 'interior_join': 18, 'copper_overlap': 101}. Overlapping-copper pairs are reported separately from centerline width transitions.

## First-pass priorities

1. Review high-priority wide islands: these have narrower connections and no attached pad or via. Choose a suitable continuous width; do not blindly shrink power traces.
2. Review whole-run widening candidates, then refill zones and run KiCad DRC.
3. Reroute constrained runs before deciding which neck-downs are necessary.
4. Inspect branches and overlap contacts for redundant segments; geometry alone cannot decide the intended topology.

## Width islands

Found 30 constant-width runs bounded by narrower or wider copper.

- **review** — narrow_neck: +3.3V / F.Cu, 0.250 mm × 0.838 mm; contacts W121, W122; attached pads/vias: 1.
- **review** — wide_island: +3.3V / F.Cu, 0.300 mm × 1.427 mm; contacts W011, W028, W089, W090, W091, W092, W093; attached pads/vias: 2.
- **review** — wide_island: +3.3V / F.Cu, 0.200 mm × 2.163 mm; contacts W094, W095, W096; attached pads/vias: 2.
- **review** — wide_island: +3.3V / F.Cu, 0.400 mm × 0.677 mm; contacts W016, W053, W054, W127, W128, W129, W130; attached pads/vias: 3.
- **review** — narrow_neck: +3.3V / F.Cu, 0.300 mm × 1.286 mm; contacts W013, W014, W043, W044, W045, W046, W047, W048, W099, W100, W101, W102, W103, W104, W105, W106, W107, W108, W109, W110, W111, W112, W113, W114, W115, W116, W117, W118, W119, W120; attached pads/vias: 2.
- **review** — narrow_neck: +3.3V / F.Cu, 0.150 mm × 2.162 mm; contacts W012, W069, W089, W093; attached pads/vias: 1.
- **review** — narrow_neck: +3.3V / F.Cu, 0.100 mm × 1.325 mm; contacts W030, W094, W095, W096; attached pads/vias: 1.
- **review** — wide_island: +3.3V / F.Cu, 0.400 mm × 0.156 mm; contacts W009, W070, W071, W072; attached pads/vias: 1.
- **review** — wide_island: +3.3V / F.Cu, 0.400 mm × 0.625 mm; contacts W015, W050, W124; attached pads/vias: 1.
- **review** — wide_island: +3.3V / F.Cu, 0.300 mm × 5.460 mm; contacts W031, W032, W097, W098; attached pads/vias: 3.
- **review** — wide_island: +3.3V / F.Cu, 0.400 mm × 0.441 mm; contacts W026, W027, W073, W074, W075, W076, W077, W078, W079, W080, W081, W082, W083, W084, W086, W087; attached pads/vias: 2.
- **review** — wide_island: +3.3V / F.Cu, 0.200 mm × 2.301 mm; contacts W051, W052, W125, W126; attached pads/vias: 3.
- **review** — wide_island: +3.3V / F.Cu, 0.400 mm × 0.206 mm; contacts W013, W014, W043, W044, W045, W046, W047, W048, W099, W100, W101, W102, W103, W104, W105, W106, W107, W108, W109, W110, W111, W112, W113, W114, W115, W116, W117, W118, W119, W120; attached pads/vias: 1.
- **review** — narrow_neck: +3.3V / F.Cu, 0.100 mm × 3.302 mm; contacts W051, W052, W125, W126; attached pads/vias: 3.
- **review** — wide_island: ESP_VDD3P3 / F.Cu, 0.250 mm × 3.310 mm; contacts W017, W131; attached pads/vias: 3.
- **review** — narrow_neck: ESP_VDD3P3 / F.Cu, 0.100 mm × 1.150 mm; contacts W017, W055, W131; attached pads/vias: 1.
- **review** — wide_island: GND / F.Cu, 0.250 mm × 1.156 mm; contacts W019, W147, W148, W149, W150; attached pads/vias: 1.
- **review** — wide_island: GND / F.Cu, 0.250 mm × 4.549 mm; contacts W005, W061, W151, W152, W153, W154, W155, W156, W157, W158, W159; attached pads/vias: 2.
- **review** — narrow_neck: GND / F.Cu, 0.150 mm × 2.166 mm; contacts W020, W160, W161, W162; attached pads/vias: 3.
- **review** — narrow_neck: GND / F.Cu, 0.200 mm × 6.429 mm; contacts W005, W061, W062, W063, W151, W152, W153, W154, W155, W156, W157, W158, W159; attached pads/vias: 2.
- **review** — wide_island: GND / F.Cu, 0.250 mm × 1.690 mm; contacts W020, W160, W161, W162; attached pads/vias: 3.
- **review** — narrow_neck: GND / B.Cu, 0.100 mm × 0.944 mm; contacts W059, W060, W142, W143, W144, W145; attached pads/vias: 0.
- **review** — wide_island: GND / B.Cu, 0.150 mm × 0.499 mm; contacts W059, W060, W142, W143, W144, W145; attached pads/vias: 1.
- **review** — wide_island: VIN_5V / B.Cu, 0.400 mm × 6.647 mm; contacts W021, W163, W164; attached pads/vias: 3.
- **review** — narrow_neck: +1.2V / F.Cu, 0.100 mm × 7.232 mm; contacts W001, W024, W025, W064; attached pads/vias: 1.
- **review** — wide_island: +1.2V / F.Cu, 0.250 mm × 0.660 mm; contacts W023, W024, W025, W064; attached pads/vias: 1.
- **review** — wide_island: +1.2V / F.Cu, 0.250 mm × 4.629 mm; contacts W001, W007, W066; attached pads/vias: 1.
- **review** — wide_island: FPGA_VCCIO0 / F.Cu, 0.200 mm × 2.498 mm; contacts W018, W056, W057, W058, W134, W135, W136, W137, W138, W139; attached pads/vias: 2.
- **review** — narrow_neck: FPGA_VCCIO0 / F.Cu, 0.100 mm × 3.114 mm; contacts W018, W056, W057, W058, W133, W134, W135, W136, W137, W138, W139; attached pads/vias: 1.
- **review** — wide_island: +1.2V_PLL / F.Cu, 0.250 mm × 3.946 mm; contacts W067, W068; attached pads/vias: 2.

## Every transition

### W001 — +1.2V / F.Cu

(12.3000, 36.8000) mm; **0.100 ↔ 0.250 mm**; `constrained_run_review` / `endpoint`.

Widening is blocked on this path. Reroute or choose one electrically adequate width for the complete run; do not retain isolated wide islands by default.

Blockers: track 729e23b8-afd5-410c-8521-c8af22931740; pad U2.29; pad U2.PAD; track 49a96588-e8ee-41e5-829b-05e823518f82.

Zone refill required; verify plane continuity after widening.

Track UUIDs: `6cf4e8b5-4f66-46f2-ab77-b527f596a957`, `d2c4a19b-6da7-42ee-ab85-efbf2c569a64`.

### W002 — +3.3V / B.Cu

(13.8250, 33.2000) mm; **0.300 ↔ 0.400 mm**; `constrained_run_review` / `endpoint`.

Widening is blocked on this path. Reroute or choose one electrically adequate width for the complete run; do not retain isolated wide islands by default.

Blockers: via 4b386c5b-0373-492b-9162-66a3ff590934; track 1ecce5c9-4d40-4c57-8dc0-2f80cc7abc0c.

Zone refill required; verify plane continuity after widening.

Track UUIDs: `1bbd210e-6eb4-4768-816b-38577a7d6c0b`, `d7e573cb-19f4-4d87-969a-f936e12e4a3c`.

### W003 — ESP_VDD3P3 / F.Cu

(11.2750, 9.5000) mm; **0.100 ↔ 0.200 mm**; `constrained_run_review` / `endpoint`.

Widening is blocked on this path. Reroute or choose one electrically adequate width for the complete run; do not retain isolated wide islands by default.

Blockers: via 267e8e29-9a74-4c01-b199-530bfe46a171; via 6ac4b4ae-69e2-43d9-8980-581769faa357; via dd281fcd-4c4a-4f7d-a13f-8e46207de680.

Zone refill required; verify plane continuity after widening.

Track UUIDs: `60d92169-7814-4fc0-a0ab-07b7ca83dc7c`, `74988ef6-b7a3-48da-a4a8-4b8ec9b1698d`.

### W004 — ESP_VDD3P3 / F.Cu

(18.1000, 10.9250) mm; **0.200 ↔ 0.250 mm**; `constrained_run_review` / `endpoint`.

Widening is blocked on this path. Reroute or choose one electrically adequate width for the complete run; do not retain isolated wide islands by default.

Blockers: pad R22.1; via e128b6fe-f854-4b47-82fe-e2759cc05e3f; pad L1.1; pad L3.2; pad L3.1; track a85e8c30-1f3d-4fa0-8348-ff209ff313b7; via 32141843-2452-4ebb-820d-46620f78dfbb.

Zone refill required; verify plane continuity after widening.

Track UUIDs: `1733a48f-7bf7-42a6-ab6c-9e53b7e274f6`, `256f3b3a-cc1a-435f-8d06-86ffe984f329`.

### W005 — GND / F.Cu

(19.4750, 16.1750) mm; **0.200 ↔ 0.250 mm**; `constrained_run_review` / `endpoint`.

Widening is blocked on this path. Reroute or choose one electrically adequate width for the complete run; do not retain isolated wide islands by default.

Blockers: pad Y1.OUT/IN.

Track UUIDs: `8c848de0-1d0f-4b9e-badd-dd60c30c383b`, `a25ed502-f7c0-4d65-ae1e-7e2351a2ce4f`.

### W006 — GND / In2.Cu

(6.4250, 20.5000) mm; **0.100 ↔ 0.250 mm**; `constrained_run_review` / `endpoint`.

Widening is blocked on this path. Reroute or choose one electrically adequate width for the complete run; do not retain isolated wide islands by default.

Blockers: via 18bd0995-5a97-444d-9f99-f1e875330816; track keepout a53b2312-e6d3-4f2e-a685-df5c12e4ef61; track a87a90c4-4483-4501-b9ca-d5123db4856b; track b7e0f6bc-c8d0-4e21-99bd-ebc44e495eed; track 7a491250-119b-4f8a-b8ce-4d03cfeda7d6; track d1c3a54d-2c24-41bf-86e4-e6b743925d0e; track ddebf737-a750-48e9-83c0-b288bd971fd3; track 36c5349e-49b7-4d54-8fc9-4a1dff227fec; track fca8b75e-05b0-4f44-9e7f-eaa8af0ca6be; track 1bda408a-6503-47d0-b8d4-599815219d9e; track 42dcccd5-1455-4e57-b00b-8e400b16773d; track bb3faa1d-0b33-4b46-909c-16cbdf23a4f9; via ba5e78cc-ce14-4cc4-a5ad-8b4ef0b113a0; track 6e74a70b-e087-47d5-adb2-e7b18bdf97b7; track 2497a1ad-27c8-47f0-8abc-c4b9cfa3be49; track 5eb3f8e3-8bbb-4faf-8368-330c6d9d8712; track 83dec2ff-7a5a-4f30-879e-d273df5f9320; track 856fe363-71a3-49a3-be0b-f8dc1d0c5a73; track 10b58ddd-2e1e-48f7-babb-b094242be24d; track 2bc556c8-6798-4561-a438-94e5a1c014a1; track a5b47ff9-a709-4a6e-808e-2cbcd530fe4e; track 72c02cdc-779c-4be1-a59d-2ea473cdbc0f; track 8fc37bf1-75f2-4a43-bcd7-71ecd34c9bca; track af434614-8dc3-43b2-aab7-a1c75a23d679; track 489288ce-eb11-4328-b77b-6a62c91a4f56; track 5dbdd725-b0fb-4fde-adcd-cdb51db9972b; track 2fee8e7e-42e8-485a-88fa-0ec066391138; track 0d90317b-5d83-4a06-aaed-aa8182a1656f; track 9fd39d53-8ed4-4d87-a493-6fa13aca5803; track 909062e2-8244-4349-9984-6c05225dfbb6.

Zone refill required; verify plane continuity after widening.

Track UUIDs: `28835c0b-ff44-4333-812a-0f735a3bf2e2`, `6a7573e1-8358-4054-85fc-779d24ad42bf`.

### W007 — +1.2V / F.Cu

(13.7000, 40.2500) mm; **0.100 ↔ 0.250 mm**; `terminal_escape_review` / `endpoint`.

Check pad/via escape: keep only the length that needs neck-down; review the listed blockers.

Blockers: pad U2.6; via 5f708ed0-0066-4230-a2aa-650d1afc7c01; via 736c27fa-6fe8-4048-86bc-26dcda1d0aa0.

Zone refill required; verify plane continuity after widening.

Track UUIDs: `05ab9db0-bbc0-4cac-a2cc-8b5a7b12892f`, `19426f11-6879-408b-bfc9-4b209ef87ed7`.

### W008 — +3.3V / B.Cu

(17.2000, 18.6000) mm; **0.300 ↔ 0.400 mm**; `terminal_escape_review` / `endpoint`.

Check pad/via escape: keep only the length that needs neck-down; review the listed blockers.

Blockers: via e5ddc26c-e590-4630-a477-6ba12ef36689; track af273911-293d-46af-932d-4921fc5bfca5.

Track UUIDs: `3b179bd4-994c-4128-a721-b65bd27220dd`, `b1876b3c-45c2-4a03-84e7-a15abe143725`.

### W009 — +3.3V / F.Cu

(17.3500, 11.3750) mm; **0.250 ↔ 0.400 mm**; `terminal_escape_review` / `endpoint`.

Check pad/via escape: keep only the length that needs neck-down; review the listed blockers.

Blockers: pad C6.1.

Track UUIDs: `99d354d9-9fa5-41ef-ad8a-8a2bfca6ad27`, `c9cf75ae-708a-479c-96e6-e32bd06e13e1`.

### W010 — +3.3V / F.Cu

(18.0250, 11.8500) mm; **0.150 ↔ 0.250 mm**; `terminal_escape_review` / `endpoint`.

Check pad/via escape: keep only the length that needs neck-down; review the listed blockers.

Blockers: pad C32.2; pad C32.1; pad L1.2; pad C6.1; track d5c323b5-baa1-4d8b-b50e-89b6d36698ba; via d81329fa-92a2-4473-a6d5-78d427db4f3d.

Zone refill required; verify plane continuity after widening.

Track UUIDs: `5f627183-a6db-4b9c-9cdb-c5dd1ab91efd`, `dfdcfb27-b5bd-44b0-83b2-19473435e667`.

### W011 — +3.3V / F.Cu

(12.7000, 11.9250) mm; **0.200 ↔ 0.300 mm**; `terminal_escape_review` / `endpoint`.

Check pad/via escape: keep only the length that needs neck-down; review the listed blockers.

Blockers: via 218d243f-bfd6-45a3-ae83-5646a368d189.

Zone refill required; verify plane continuity after widening.

Track UUIDs: `21c3c957-cf90-4575-85a1-82972fd7c0bc`, `cdde7750-576b-42e0-be42-d92723c68cf7`.

### W012 — +3.3V / F.Cu

(13.8125, 11.9250) mm; **0.150 ↔ 0.200 mm**; `terminal_escape_review` / `endpoint`.

Check pad/via escape: keep only the length that needs neck-down; review the listed blockers.

Blockers: pad C37.2.

Zone refill required; verify plane continuity after widening.

Track UUIDs: `cdde7750-576b-42e0-be42-d92723c68cf7`, `d79ff3c6-ab71-4244-a054-da7a54e96a4d`.

### W013 — +3.3V / F.Cu

(15.6750, 24.7750) mm; **0.300 ↔ 0.400 mm**; `terminal_escape_review` / `endpoint`.

Check pad/via escape: keep only the length that needs neck-down; review the listed blockers.

Blockers: pad U3.5.

Zone refill required; verify plane continuity after widening.

Track UUIDs: `21895ce1-2009-4c4e-82d5-ead25a05dbb4`, `fbcbc6ff-a856-411d-bb3e-18851b0dfb59`.

### W014 — +3.3V / F.Cu

(15.7500, 24.9500) mm; **0.300 ↔ 0.400 mm**; `terminal_escape_review` / `endpoint`.

Check pad/via escape: keep only the length that needs neck-down; review the listed blockers.

Blockers: track a8e4a2d1-7a14-42b3-aab1-644181c94a78; pad U3.5.

Zone refill required; verify plane continuity after widening.

Track UUIDs: `830dac8a-1cbd-4119-875b-aa3b249119ca`, `f2ba0ebc-b89f-4fa3-ae6d-051e850ec4fe`.

### W015 — +3.3V / F.Cu

(8.2250, 36.3250) mm; **0.100 ↔ 0.400 mm**; `terminal_escape_review` / `endpoint`.

Check pad/via escape: keep only the length that needs neck-down; review the listed blockers.

Blockers: pad U2.23; track 6cf4e8b5-4f66-46f2-ab77-b527f596a957; track 00a58d13-5480-4411-8f9d-fe6cb53df2b3; track 47299f60-cd60-48c8-b250-37138a606504.

Track UUIDs: `41030a01-68e5-436c-9bf4-823283f24c89`, `49a96588-e8ee-41e5-829b-05e823518f82`.

### W016 — +3.3V / F.Cu

(14.1500, 43.7500) mm; **0.150 ↔ 0.400 mm**; `terminal_escape_review` / `endpoint`.

Check pad/via escape: keep only the length that needs neck-down; review the listed blockers.

Blockers: pad D1.P$4; pad D1.P$3.

Track UUIDs: `492e69cf-01c1-480c-a9de-903b97d7f160`, `710f5547-603a-47dd-adad-0a1a31b92567`.

### W017 — ESP_VDD3P3 / F.Cu

(11.6500, 10.6500) mm; **0.100 ↔ 0.250 mm**; `terminal_escape_review` / `endpoint`.

Check pad/via escape: keep only the length that needs neck-down; review the listed blockers.

Blockers: pad L3.1.

Zone refill required; verify plane continuity after widening.

Track UUIDs: `2b9e829c-ba18-4618-ba0b-115e21e84012`, `7d46c5ae-fe9e-4c05-a0d9-1092f72f3e50`.

### W018 — FPGA_VCCIO0 / F.Cu

(6.5202, 40.7500) mm; **0.100 ↔ 0.200 mm**; `terminal_escape_review` / `endpoint`.

Check pad/via escape: keep only the length that needs neck-down; review the listed blockers.

Blockers: track d1dc0a1e-b56e-45d5-9233-0c47b4bce818; via 3b18a63f-68e8-4fc7-af82-358083e0bcf0; pad C46.2.

Zone refill required; verify plane continuity after widening.

Track UUIDs: `478beb42-7aa8-47af-936a-acdc2dd0bab1`, `4d70c820-c2bf-4c9e-9814-675329155028`.

### W019 — GND / F.Cu

(17.2250, 15.7250) mm; **0.150 ↔ 0.250 mm**; `terminal_escape_review` / `endpoint`.

Check pad/via escape: keep only the length that needs neck-down; review the listed blockers.

Blockers: track 593dcb02-9008-4763-8d34-e989d22f4f8e.

Track UUIDs: `0894003a-6897-4a78-934d-cec2be879c9a`, `98b34a5a-662e-44df-be00-9853f149c122`.

### W020 — GND / F.Cu

(16.6500, 22.9000) mm; **0.150 ↔ 0.250 mm**; `terminal_escape_review` / `endpoint`.

Check pad/via escape: keep only the length that needs neck-down; review the listed blockers.

Blockers: track f3b4c344-aba7-4f78-bb5a-d8f7c18674c0.

Track UUIDs: `32990613-fb35-4ec0-ab27-38a3e34e4cf0`, `f803cf5a-7e9f-4232-af82-0d925307aaf5`.

### W021 — VIN_5V / B.Cu

(13.0000, 15.1750) mm; **0.300 ↔ 0.400 mm**; `terminal_escape_review` / `endpoint`.

Check pad/via escape: keep only the length that needs neck-down; review the listed blockers.

Blockers: track b262dd2b-d54a-4a15-85c5-399fbe2cf63e.

Zone refill required; verify plane continuity after widening.

Track UUIDs: `226259e1-0627-4110-a7eb-ef2edef884d3`, `563eb6b8-804b-40e3-a1d7-198f066af081`.

### W022 — +1.2V / F.Cu

(0.8000, 33.9500) mm; **0.100 ↔ 0.250 mm**; `branch_review` / `interior_join`.

Review branch currents and topology; different branch widths can be intentional.

Blockers: track 147f4fff-f8f0-4bac-9985-c9f7d01299b7; via ce248f0b-45d0-4cfc-aa4a-10b63fe1acc5; track e4c42d14-9055-4d38-9433-6efd45867658; pad TP1.1.

Zone refill required; verify plane continuity after widening.

Track UUIDs: `a00ccec3-2fc0-4486-bcce-6033cb5f201e`, `e4c0778b-3d70-40d4-8b04-40d21c217265`.

### W023 — +1.2V / F.Cu

(6.5202, 39.2500) mm; **0.200 ↔ 0.250 mm**; `branch_review` / `interior_join`.

Review branch currents and topology; different branch widths can be intentional.

Blockers: track 6d849674-33a6-492e-a030-5e8164ddcb87; track 7d7e8e82-3d5f-4f64-aa7f-f95e196949b7; via 32c02b57-e877-482c-aa81-f00c39727b34; track bf7feab6-5822-451f-a36e-30bcf9051ef4.

Track UUIDs: `0cda2b96-0ea1-426b-8b93-3c0231d8c1fd`, `9f816685-fefb-4042-9bf3-86525428d754`.

### W024 — +1.2V / F.Cu

(6.8000, 39.2500) mm; **0.100 ↔ 0.250 mm**; `branch_review` / `endpoint`.

Review branch currents and topology; different branch widths can be intentional.

Blockers: track 729e23b8-afd5-410c-8521-c8af22931740; pad U2.29; pad U2.PAD; track 49a96588-e8ee-41e5-829b-05e823518f82.

Zone refill required; verify plane continuity after widening.

Track UUIDs: `0cda2b96-0ea1-426b-8b93-3c0231d8c1fd`, `4cc56bae-9f65-4aef-a8ca-ff8e74e23188`.

### W025 — +1.2V / F.Cu

(6.8000, 39.2500) mm; **0.100 ↔ 0.250 mm**; `branch_review` / `endpoint`.

Review branch currents and topology; different branch widths can be intentional.

Blockers: track 729e23b8-afd5-410c-8521-c8af22931740; pad U2.29; pad U2.PAD; track 49a96588-e8ee-41e5-829b-05e823518f82.

Zone refill required; verify plane continuity after widening.

Track UUIDs: `4cc56bae-9f65-4aef-a8ca-ff8e74e23188`, `50f5b57c-ed3c-4f60-8130-82b934ae22d5`.

### W026 — +3.3V / F.Cu

(17.9000, 11.7750) mm; **0.250 ↔ 0.400 mm**; `branch_review` / `endpoint`.

Review branch currents and topology; different branch widths can be intentional.

Blockers: pad C6.1.

Track UUIDs: `50475509-9c76-4027-b991-b6be077c2b8f`, `583e3fda-aac3-4326-9b0c-dff5b83dbe15`.

### W027 — +3.3V / F.Cu

(17.9000, 11.7750) mm; **0.250 ↔ 0.400 mm**; `branch_review` / `endpoint`.

Review branch currents and topology; different branch widths can be intentional.

Blockers: pad C6.1.

Track UUIDs: `50475509-9c76-4027-b991-b6be077c2b8f`, `b66e5382-ca95-4347-8215-c204ac2068f4`.

### W028 — +3.3V / F.Cu

(13.6904, 11.9250) mm; **0.200 ↔ 0.300 mm**; `branch_review` / `interior_join`.

Review branch currents and topology; different branch widths can be intentional.

Blockers: via 218d243f-bfd6-45a3-ae83-5646a368d189.

Zone refill required; verify plane continuity after widening.

Track UUIDs: `8a8bd08b-bc03-4c00-bf93-66940244275c`, `cdde7750-576b-42e0-be42-d92723c68cf7`.

### W029 — +3.3V / F.Cu

(13.9000, 13.7000) mm; **0.150 ↔ 0.200 mm**; `branch_review` / `interior_join`.

Review branch currents and topology; different branch widths can be intentional.

Blockers: pad U1.50; pad U1.53; pad U1.52.

Zone refill required; verify plane continuity after widening.

Track UUIDs: `b1781588-a94d-4d28-a17c-4ea2d2577e8d`, `bed3ed1b-917e-4ccc-9360-e9995d52ed69`.

### W030 — +3.3V / F.Cu

(12.2000, 17.3000) mm; **0.100 ↔ 0.150 mm**; `branch_review` / `interior_join`.

Review branch currents and topology; different branch widths can be intentional.

Blockers: pad U1.57.

Zone refill required; verify plane continuity after widening.

Track UUIDs: `1adad6c3-aba9-4009-a9e5-5ff19c8395a2`, `a3e468cc-30e9-400d-ba2a-4f86d50a16af`.

### W031 — +3.3V / F.Cu

(7.3000, 17.7250) mm; **0.150 ↔ 0.300 mm**; `branch_review` / `endpoint`.

Review branch currents and topology; different branch widths can be intentional.

Blockers: pad U1.31.

Zone refill required; verify plane continuity after widening.

Track UUIDs: `17cf48cc-1d86-4a27-92d2-2652f048bc78`, `c99995bd-3096-4bfa-a1de-755e638ccf12`.

### W032 — +3.3V / F.Cu

(7.3000, 17.7250) mm; **0.150 ↔ 0.300 mm**; `branch_review` / `endpoint`.

Review branch currents and topology; different branch widths can be intentional.

Blockers: pad U1.31.

Zone refill required; verify plane continuity after widening.

Track UUIDs: `17cf48cc-1d86-4a27-92d2-2652f048bc78`, `fb42a986-2fe9-4f71-8cf1-d7b61486b58b`.

### W033 — +3.3V / F.Cu

(17.2000, 18.6000) mm; **0.300 ↔ 0.400 mm**; `branch_review` / `endpoint`.

Review branch currents and topology; different branch widths can be intentional.

Blockers: via e5ddc26c-e590-4630-a477-6ba12ef36689.

Zone refill required; verify plane continuity after widening.

Track UUIDs: `2369d6e5-c004-4837-9db6-00008f5c65e1`, `62a08f72-8e26-4ab6-b9d5-242dcc525fc9`.

### W034 — +3.3V / F.Cu

(17.2000, 18.6000) mm; **0.300 ↔ 0.400 mm**; `branch_review` / `endpoint`.

Review branch currents and topology; different branch widths can be intentional.

Blockers: via e5ddc26c-e590-4630-a477-6ba12ef36689.

Zone refill required; verify plane continuity after widening.

Track UUIDs: `2369d6e5-c004-4837-9db6-00008f5c65e1`, `8627418d-e901-40b7-b1da-1891b864986f`.

### W035 — +3.3V / F.Cu

(17.2000, 18.6000) mm; **0.300 ↔ 0.400 mm**; `branch_review` / `endpoint`.

Review branch currents and topology; different branch widths can be intentional.

Blockers: via e5ddc26c-e590-4630-a477-6ba12ef36689.

Zone refill required; verify plane continuity after widening.

Track UUIDs: `2369d6e5-c004-4837-9db6-00008f5c65e1`, `aaa43691-c4db-4a6a-9fce-c3473aa695af`.

### W036 — +3.3V / F.Cu

(17.2000, 18.6000) mm; **0.300 ↔ 0.400 mm**; `branch_review` / `endpoint`.

Review branch currents and topology; different branch widths can be intentional.

Blockers: via e5ddc26c-e590-4630-a477-6ba12ef36689.

Zone refill required; verify plane continuity after widening.

Track UUIDs: `62a08f72-8e26-4ab6-b9d5-242dcc525fc9`, `9fceb7ec-08a1-43e1-9e6f-37e5b026c783`.

### W037 — +3.3V / F.Cu

(17.2000, 18.6000) mm; **0.300 ↔ 0.400 mm**; `branch_review` / `endpoint`.

Review branch currents and topology; different branch widths can be intentional.

Blockers: via e5ddc26c-e590-4630-a477-6ba12ef36689.

Zone refill required; verify plane continuity after widening.

Track UUIDs: `62a08f72-8e26-4ab6-b9d5-242dcc525fc9`, `cea6a8b5-18fd-482f-ab20-32e302871baf`.

### W038 — +3.3V / F.Cu

(17.2000, 18.6000) mm; **0.300 ↔ 0.400 mm**; `branch_review` / `endpoint`.

Review branch currents and topology; different branch widths can be intentional.

Blockers: via e5ddc26c-e590-4630-a477-6ba12ef36689.

Zone refill required; verify plane continuity after widening.

Track UUIDs: `8627418d-e901-40b7-b1da-1891b864986f`, `9fceb7ec-08a1-43e1-9e6f-37e5b026c783`.

### W039 — +3.3V / F.Cu

(17.2000, 18.6000) mm; **0.300 ↔ 0.400 mm**; `branch_review` / `endpoint`.

Review branch currents and topology; different branch widths can be intentional.

Blockers: via e5ddc26c-e590-4630-a477-6ba12ef36689.

Zone refill required; verify plane continuity after widening.

Track UUIDs: `8627418d-e901-40b7-b1da-1891b864986f`, `cea6a8b5-18fd-482f-ab20-32e302871baf`.

### W040 — +3.3V / F.Cu

(17.2000, 18.6000) mm; **0.300 ↔ 0.400 mm**; `branch_review` / `endpoint`.

Review branch currents and topology; different branch widths can be intentional.

Blockers: via e5ddc26c-e590-4630-a477-6ba12ef36689.

Zone refill required; verify plane continuity after widening.

Track UUIDs: `9fceb7ec-08a1-43e1-9e6f-37e5b026c783`, `aaa43691-c4db-4a6a-9fce-c3473aa695af`.

### W041 — +3.3V / F.Cu

(17.2000, 18.6000) mm; **0.300 ↔ 0.400 mm**; `branch_review` / `endpoint`.

Review branch currents and topology; different branch widths can be intentional.

Blockers: via e5ddc26c-e590-4630-a477-6ba12ef36689.

Zone refill required; verify plane continuity after widening.

Track UUIDs: `aaa43691-c4db-4a6a-9fce-c3473aa695af`, `cea6a8b5-18fd-482f-ab20-32e302871baf`.

### W042 — +3.3V / F.Cu

(7.8000, 19.4000) mm; **0.150 ↔ 0.200 mm**; `branch_review` / `interior_join`.

Review branch currents and topology; different branch widths can be intentional.

Blockers: pad U1.31.

Track UUIDs: `a4f4c7d3-565a-4023-8fd8-ba144b8bb516`, `b43654a9-0c3b-4bfb-a2bb-a5b1f8d3f845`.

### W043 — +3.3V / F.Cu

(15.6750, 24.8500) mm; **0.300 ↔ 0.400 mm**; `branch_review` / `interior_join`.

Review branch currents and topology; different branch widths can be intentional.

Blockers: track a8e4a2d1-7a14-42b3-aab1-644181c94a78; pad U3.5.

Zone refill required; verify plane continuity after widening.

Track UUIDs: `0358ecbd-b91b-4207-8cee-1d18262dea0b`, `fbcbc6ff-a856-411d-bb3e-18851b0dfb59`.

### W044 — +3.3V / F.Cu

(15.7000, 24.8750) mm; **0.300 ↔ 0.400 mm**; `branch_review` / `endpoint`.

Review branch currents and topology; different branch widths can be intentional.

Blockers: track a8e4a2d1-7a14-42b3-aab1-644181c94a78; pad U3.5.

Zone refill required; verify plane continuity after widening.

Track UUIDs: `0358ecbd-b91b-4207-8cee-1d18262dea0b`, `c4ecb65e-2675-444f-a251-519c177fb4d7`.

### W045 — +3.3V / F.Cu

(15.7000, 24.8750) mm; **0.300 ↔ 0.400 mm**; `branch_review` / `endpoint`.

Review branch currents and topology; different branch widths can be intentional.

Blockers: track a8e4a2d1-7a14-42b3-aab1-644181c94a78; pad U3.5.

Zone refill required; verify plane continuity after widening.

Track UUIDs: `0358ecbd-b91b-4207-8cee-1d18262dea0b`, `dbf2ae00-ad1d-4299-a8d6-47c03ff1044c`.

### W046 — +3.3V / F.Cu

(15.7000, 24.9000) mm; **0.300 ↔ 0.400 mm**; `branch_review` / `endpoint`.

Review branch currents and topology; different branch widths can be intentional.

Blockers: track a8e4a2d1-7a14-42b3-aab1-644181c94a78; pad U3.5.

Zone refill required; verify plane continuity after widening.

Track UUIDs: `0bf0f774-4caa-4a64-bfc3-3e81eb402d14`, `830dac8a-1cbd-4119-875b-aa3b249119ca`.

### W047 — +3.3V / F.Cu

(15.7000, 24.9000) mm; **0.300 ↔ 0.400 mm**; `branch_review` / `endpoint`.

Review branch currents and topology; different branch widths can be intentional.

Blockers: track a8e4a2d1-7a14-42b3-aab1-644181c94a78; pad U3.5.

Zone refill required; verify plane continuity after widening.

Track UUIDs: `0bf0f774-4caa-4a64-bfc3-3e81eb402d14`, `dbf2ae00-ad1d-4299-a8d6-47c03ff1044c`.

### W048 — +3.3V / F.Cu

(15.7000, 24.9000) mm; **0.300 ↔ 0.400 mm**; `branch_review` / `interior_join`.

Review branch currents and topology; different branch widths can be intentional.

Blockers: track a8e4a2d1-7a14-42b3-aab1-644181c94a78; pad U3.5.

Zone refill required; verify plane continuity after widening.

Track UUIDs: `dbf2ae00-ad1d-4299-a8d6-47c03ff1044c`, `f2ba0ebc-b89f-4fa3-ae6d-051e850ec4fe`.

### W049 — +3.3V / F.Cu

(7.6798, 34.4952) mm; **0.100 ↔ 0.200 mm**; `branch_review` / `interior_join`.

Review branch currents and topology; different branch widths can be intentional.

Blockers: pad SJ1.2; pad SJ1.3; via 73571995-cbf2-4ce4-b487-be077b9cc435.

Track UUIDs: `390ef521-138c-482e-a9f7-8f8e3ec6d593`, `e63f0d0f-c1a3-4b68-9be0-5ec10494f67a`.

### W050 — +3.3V / F.Cu

(8.2500, 35.7250) mm; **0.200 ↔ 0.400 mm**; `branch_review` / `interior_join`.

Review branch currents and topology; different branch widths can be intentional.

Blockers: via c33d5851-0f79-47ae-b924-32b15d4ad8ce; via 545c620b-2297-4f9a-ba87-154d9d092aab.

Track UUIDs: `a0d69b42-9a8a-4c3a-a33b-2b389e0273b6`, `eead542b-573e-4a3c-b490-6cc3f37f126e`.

### W051 — +3.3V / F.Cu

(14.1000, 42.0500) mm; **0.100 ↔ 0.200 mm**; `branch_review` / `interior_join`.

Review branch currents and topology; different branch widths can be intentional.

Blockers: via a3159c4a-d259-486d-9a24-dbcd1a0c1255; track a7d53fc6-860b-4fa2-b9d4-fc7afc42f54c; track 8a68faa2-e40b-481e-88a3-3b98fea640fe.

Zone refill required; verify plane continuity after widening.

Track UUIDs: `987b2137-9f15-4460-acb8-23b115eecaf7`, `ca1f97b2-e964-493e-900f-fca5dd8f328a`.

### W052 — +3.3V / F.Cu

(14.3500, 42.0500) mm; **0.100 ↔ 0.200 mm**; `branch_review` / `interior_join`.

Review branch currents and topology; different branch widths can be intentional.

Blockers: via a3159c4a-d259-486d-9a24-dbcd1a0c1255; track a7d53fc6-860b-4fa2-b9d4-fc7afc42f54c; track 8a68faa2-e40b-481e-88a3-3b98fea640fe.

Zone refill required; verify plane continuity after widening.

Track UUIDs: `8c884e80-0d17-4522-b2a6-4567b0ef688f`, `ca1f97b2-e964-493e-900f-fca5dd8f328a`.

### W053 — +3.3V / F.Cu

(14.7250, 43.6750) mm; **0.250 ↔ 0.400 mm**; `branch_review` / `endpoint`.

Review branch currents and topology; different branch widths can be intentional.

Blockers: track 8a68faa2-e40b-481e-88a3-3b98fea640fe; via 647536ef-eef0-4c2d-82ac-a8528c439123; track b41acb09-e01c-49e6-8d4a-6fdf48b26528.

Zone refill required; verify plane continuity after widening.

Track UUIDs: `0930d80e-73f2-4ead-81e9-18db86a6eeff`, `b71a5795-8966-4bcc-8724-7215ec90b5a6`.

### W054 — +3.3V / F.Cu

(14.7250, 43.6750) mm; **0.250 ↔ 0.400 mm**; `branch_review` / `endpoint`.

Review branch currents and topology; different branch widths can be intentional.

Blockers: track 8a68faa2-e40b-481e-88a3-3b98fea640fe; via 647536ef-eef0-4c2d-82ac-a8528c439123; track b41acb09-e01c-49e6-8d4a-6fdf48b26528.

Zone refill required; verify plane continuity after widening.

Track UUIDs: `0930d80e-73f2-4ead-81e9-18db86a6eeff`, `beb0a547-3e5d-496d-88d8-a33bb560269f`.

### W055 — ESP_VDD3P3 / F.Cu

(11.6500, 9.5000) mm; **0.100 ↔ 0.200 mm**; `branch_review` / `interior_join`.

Review branch currents and topology; different branch widths can be intentional.

Blockers: pad L3.1.

Zone refill required; verify plane continuity after widening.

Track UUIDs: `2b9e829c-ba18-4618-ba0b-115e21e84012`, `60d92169-7814-4fc0-a0ab-07b7ca83dc7c`.

### W056 — FPGA_VCCIO0 / F.Cu

(6.4250, 40.7500) mm; **0.100 ↔ 0.200 mm**; `branch_review` / `interior_join`.

Review branch currents and topology; different branch widths can be intentional.

Blockers: track d1dc0a1e-b56e-45d5-9233-0c47b4bce818; via 3b18a63f-68e8-4fc7-af82-358083e0bcf0; pad C46.2.

Zone refill required; verify plane continuity after widening.

Track UUIDs: `4d70c820-c2bf-4c9e-9814-675329155028`, `cf5750ad-6045-4888-863a-983258caba32`.

### W057 — FPGA_VCCIO0 / F.Cu

(5.4250, 40.8000) mm; **0.100 ↔ 0.200 mm**; `branch_review` / `interior_join`.

Review branch currents and topology; different branch widths can be intentional.

Blockers: track d1dc0a1e-b56e-45d5-9233-0c47b4bce818; via 3b18a63f-68e8-4fc7-af82-358083e0bcf0; pad C46.2.

Zone refill required; verify plane continuity after widening.

Track UUIDs: `5eaf5e92-0f1b-4fd5-be96-4007bf2ce4fd`, `ce49a44b-41ba-47b7-8747-bba1065628f8`.

### W058 — FPGA_VCCIO0 / F.Cu

(5.9702, 40.8500) mm; **0.100 ↔ 0.200 mm**; `branch_review` / `interior_join`.

Review branch currents and topology; different branch widths can be intentional.

Blockers: track d1dc0a1e-b56e-45d5-9233-0c47b4bce818; via 3b18a63f-68e8-4fc7-af82-358083e0bcf0; pad C46.2.

Zone refill required; verify plane continuity after widening.

Track UUIDs: `04d7849b-7f2d-42da-be96-8edd8f0e28f6`, `42da7d6c-d89f-44d2-8d3a-f73f83295a9d`.

### W059 — GND / B.Cu

(10.7250, 39.3750) mm; **0.100 ↔ 0.150 mm**; `branch_review` / `endpoint`.

Review branch currents and topology; different branch widths can be intentional.

Blockers: track e6f2f6da-31a9-4c69-9d78-e7353ef60b48.

Track UUIDs: `6a132136-311d-4c2d-9313-7af69219d9ad`, `99b6ede0-ef80-4916-b40c-457a2596a6fa`.

### W060 — GND / B.Cu

(10.7250, 39.3750) mm; **0.100 ↔ 0.150 mm**; `branch_review` / `endpoint`.

Review branch currents and topology; different branch widths can be intentional.

Blockers: track ad4a5e25-3ae6-446e-a1ad-9c9199be8ba1; track fb8bd343-ea94-4aca-b160-b1038518e06c; track 7837d937-d90d-4240-aabf-b84394e38619.

Track UUIDs: `99b6ede0-ef80-4916-b40c-457a2596a6fa`, `9fbcb8a6-fad1-4ddc-b1ba-17b22a6ba05d`.

### W061 — GND / F.Cu

(19.4500, 16.2500) mm; **0.200 ↔ 0.250 mm**; `branch_review` / `interior_join`.

Review branch currents and topology; different branch widths can be intentional.

Blockers: pad Y1.OUT/IN.

Track UUIDs: `3cd6e990-1d4b-4d85-b81c-510ef47cb569`, `54f9072c-a614-4565-8c5c-b2f7f760fa69`.

### W062 — GND / F.Cu

(19.1250, 17.2750) mm; **0.200 ↔ 0.250 mm**; `branch_review` / `interior_join`.

Review branch currents and topology; different branch widths can be intentional.

Blockers: pad Y1.OUT/IN.

Track UUIDs: `924f1d9c-62ce-4de0-afdb-63b40c6fc113`, `b66cd0fc-ff1d-4cdb-992e-3e93aabb11cd`.

### W063 — GND / F.Cu

(19.1250, 17.2750) mm; **0.200 ↔ 0.250 mm**; `branch_review` / `endpoint`.

Review branch currents and topology; different branch widths can be intentional.

Blockers: pad Y1.OUT/IN.

Track UUIDs: `b66cd0fc-ff1d-4cdb-992e-3e93aabb11cd`, `eb2b3a44-64ad-471b-8c0f-9bc62e2de0dd`.

### W064 — +1.2V / F.Cu

(6.8125, 39.2625) mm; **0.100 ↔ 0.250 mm**; `overlap_topology_review` / `copper_overlap`.

Inspect the overlapping copper join before editing widths; this is not a simple endpoint transition.

Blockers: track 729e23b8-afd5-410c-8521-c8af22931740; pad U2.29; pad U2.PAD; track 49a96588-e8ee-41e5-829b-05e823518f82.

Zone refill required; verify plane continuity after widening.

Track UUIDs: `4cc56bae-9f65-4aef-a8ca-ff8e74e23188`, `eaf0f51c-399d-49db-bd30-29069d2f50e7`.

### W065 — +1.2V / F.Cu

(5.0798, 39.9500) mm; **0.100 ↔ 0.200 mm**; `overlap_topology_review` / `copper_overlap`.

Inspect the overlapping copper join before editing widths; this is not a simple endpoint transition.

Blockers: pad C44.2.

Zone refill required; verify plane continuity after widening.

Track UUIDs: `7586f53f-5853-499f-843f-3f29f0b63a56`, `b5ce97dc-ba7b-44d5-958b-3e4cb65a3693`.

### W066 — +1.2V / F.Cu

(13.6250, 40.2125) mm; **0.100 ↔ 0.250 mm**; `overlap_topology_review` / `copper_overlap`.

Inspect the overlapping copper join before editing widths; this is not a simple endpoint transition.

Blockers: pad U2.6; via 5f708ed0-0066-4230-a2aa-650d1afc7c01; via 736c27fa-6fe8-4048-86bc-26dcda1d0aa0.

Zone refill required; verify plane continuity after widening.

Track UUIDs: `05ab9db0-bbc0-4cac-a2cc-8b5a7b12892f`, `6130d203-0944-46b7-a301-1337e49ad11b`.

### W067 — +1.2V_PLL / F.Cu

(3.1750, 37.6500) mm; **0.100 ↔ 0.250 mm**; `overlap_topology_review` / `copper_overlap`.

Inspect the overlapping copper join before editing widths; this is not a simple endpoint transition.

Blockers: via 0de7c275-bc9d-4670-b542-7004b8d91d1d; track 09abd77d-ba13-47de-ae32-4329777a5a41.

Zone refill required; verify plane continuity after widening.

Track UUIDs: `7b8752b0-1287-4d1b-8ac9-4370b250cdc1`, `fd0f5a19-6c47-401c-91cc-f34218e92c8d`.

### W068 — +1.2V_PLL / F.Cu

(3.1500, 37.6750) mm; **0.100 ↔ 0.250 mm**; `overlap_topology_review` / `copper_overlap`.

Inspect the overlapping copper join before editing widths; this is not a simple endpoint transition.

Blockers: via 0de7c275-bc9d-4670-b542-7004b8d91d1d; track 09abd77d-ba13-47de-ae32-4329777a5a41.

Zone refill required; verify plane continuity after widening.

Track UUIDs: `7971bb5a-fe32-4816-9c7f-a8942ef758a1`, `fd0f5a19-6c47-401c-91cc-f34218e92c8d`.

### W069 — +3.3V / F.Cu

(14.7000, 10.0250) mm; **0.150 ↔ 0.300 mm**; `overlap_topology_review` / `copper_overlap`.

Inspect the overlapping copper join before editing widths; this is not a simple endpoint transition.

Blockers: pad C37.2; pad C1.1.

Zone refill required; verify plane continuity after widening.

Track UUIDs: `0b7aaf44-6ff6-42af-aad5-c2ad38c51d0b`, `8a9b17ca-1383-4d82-9c44-d5487033b0df`.

### W070 — +3.3V / F.Cu

(17.3125, 11.3625) mm; **0.250 ↔ 0.400 mm**; `overlap_topology_review` / `copper_overlap`.

Inspect the overlapping copper join before editing widths; this is not a simple endpoint transition.

Blockers: pad C6.1.

Track UUIDs: `76f6a90c-5e3c-4dc2-9a90-391dacc183ed`, `c9cf75ae-708a-479c-96e6-e32bd06e13e1`.

### W071 — +3.3V / F.Cu

(17.3250, 11.3625) mm; **0.250 ↔ 0.400 mm**; `overlap_topology_review` / `copper_overlap`.

Inspect the overlapping copper join before editing widths; this is not a simple endpoint transition.

Blockers: pad C6.1.

Track UUIDs: `232efeb9-cc5c-4a53-8259-a754deada378`, `c9cf75ae-708a-479c-96e6-e32bd06e13e1`.

### W072 — +3.3V / F.Cu

(17.3375, 11.3750) mm; **0.250 ↔ 0.400 mm**; `overlap_topology_review` / `copper_overlap`.

Inspect the overlapping copper join before editing widths; this is not a simple endpoint transition.

Blockers: pad C6.1.

Track UUIDs: `9ba529fc-d42e-4070-9e40-3e3c7663cbad`, `c9cf75ae-708a-479c-96e6-e32bd06e13e1`.

### W073 — +3.3V / F.Cu

(17.7000, 11.7250) mm; **0.250 ↔ 0.400 mm**; `overlap_topology_review` / `copper_overlap`.

Inspect the overlapping copper join before editing widths; this is not a simple endpoint transition.

Blockers: pad C6.1.

Track UUIDs: `49a99554-c1ae-426a-819b-25b4830c1abd`, `c9cf75ae-708a-479c-96e6-e32bd06e13e1`.

### W074 — +3.3V / F.Cu

(17.7000, 11.7250) mm; **0.250 ↔ 0.400 mm**; `overlap_topology_review` / `copper_overlap`.

Inspect the overlapping copper join before editing widths; this is not a simple endpoint transition.

Blockers: pad C6.1.

Track UUIDs: `839e3ae7-ee40-4c6b-8761-9665e29d799e`, `c9cf75ae-708a-479c-96e6-e32bd06e13e1`.

### W075 — +3.3V / F.Cu

(17.8750, 11.7500) mm; **0.250 ↔ 0.400 mm**; `overlap_topology_review` / `copper_overlap`.

Inspect the overlapping copper join before editing widths; this is not a simple endpoint transition.

Blockers: pad C6.1.

Track UUIDs: `49a99554-c1ae-426a-819b-25b4830c1abd`, `50475509-9c76-4027-b991-b6be077c2b8f`.

### W076 — +3.3V / F.Cu

(17.8750, 11.7500) mm; **0.250 ↔ 0.400 mm**; `overlap_topology_review` / `copper_overlap`.

Inspect the overlapping copper join before editing widths; this is not a simple endpoint transition.

Blockers: pad C6.1.

Track UUIDs: `50475509-9c76-4027-b991-b6be077c2b8f`, `839e3ae7-ee40-4c6b-8761-9665e29d799e`.

### W077 — +3.3V / F.Cu

(17.8250, 11.7875) mm; **0.250 ↔ 0.400 mm**; `overlap_topology_review` / `copper_overlap`.

Inspect the overlapping copper join before editing widths; this is not a simple endpoint transition.

Blockers: pad C6.1.

Track UUIDs: `49a99554-c1ae-426a-819b-25b4830c1abd`, `5f627183-a6db-4b9c-9cdb-c5dd1ab91efd`.

### W078 — +3.3V / F.Cu

(17.8500, 11.7875) mm; **0.250 ↔ 0.400 mm**; `overlap_topology_review` / `copper_overlap`.

Inspect the overlapping copper join before editing widths; this is not a simple endpoint transition.

Blockers: pad C6.1.

Track UUIDs: `5f627183-a6db-4b9c-9cdb-c5dd1ab91efd`, `839e3ae7-ee40-4c6b-8761-9665e29d799e`.

### W079 — +3.3V / F.Cu

(17.9375, 11.7875) mm; **0.150 ↔ 0.400 mm**; `overlap_topology_review` / `copper_overlap`.

Inspect the overlapping copper join before editing widths; this is not a simple endpoint transition.

Blockers: pad C32.2; pad C32.1; pad L1.2; track 82f36b29-9ab5-4a56-a853-952df0bacef1; pad C6.2; pad C6.1; track d5c323b5-baa1-4d8b-b50e-89b6d36698ba; via d81329fa-92a2-4473-a6d5-78d427db4f3d; pad Y1.GND-A.

Zone refill required; verify plane continuity after widening.

Track UUIDs: `49a99554-c1ae-426a-819b-25b4830c1abd`, `dfdcfb27-b5bd-44b0-83b2-19473435e667`.

### W080 — +3.3V / F.Cu

(17.9375, 11.7875) mm; **0.150 ↔ 0.400 mm**; `overlap_topology_review` / `copper_overlap`.

Inspect the overlapping copper join before editing widths; this is not a simple endpoint transition.

Blockers: pad C32.2; pad C32.1; pad L1.2; track 82f36b29-9ab5-4a56-a853-952df0bacef1; pad C6.2; pad C6.1; track d5c323b5-baa1-4d8b-b50e-89b6d36698ba; via d81329fa-92a2-4473-a6d5-78d427db4f3d; pad Y1.GND-A.

Zone refill required; verify plane continuity after widening.

Track UUIDs: `839e3ae7-ee40-4c6b-8761-9665e29d799e`, `dfdcfb27-b5bd-44b0-83b2-19473435e667`.

### W081 — +3.3V / F.Cu

(17.8625, 11.8125) mm; **0.250 ↔ 0.400 mm**; `overlap_topology_review` / `copper_overlap`.

Inspect the overlapping copper join before editing widths; this is not a simple endpoint transition.

Blockers: pad C6.1.

Track UUIDs: `583e3fda-aac3-4326-9b0c-dff5b83dbe15`, `c9cf75ae-708a-479c-96e6-e32bd06e13e1`.

### W082 — +3.3V / F.Cu

(17.8625, 11.8125) mm; **0.250 ↔ 0.400 mm**; `overlap_topology_review` / `copper_overlap`.

Inspect the overlapping copper join before editing widths; this is not a simple endpoint transition.

Blockers: pad C6.1.

Track UUIDs: `b66e5382-ca95-4347-8215-c204ac2068f4`, `c9cf75ae-708a-479c-96e6-e32bd06e13e1`.

### W083 — +3.3V / F.Cu

(17.9000, 11.8125) mm; **0.250 ↔ 0.400 mm**; `overlap_topology_review` / `copper_overlap`.

Inspect the overlapping copper join before editing widths; this is not a simple endpoint transition.

Blockers: pad C6.1.

Track UUIDs: `583e3fda-aac3-4326-9b0c-dff5b83dbe15`, `5f627183-a6db-4b9c-9cdb-c5dd1ab91efd`.

### W084 — +3.3V / F.Cu

(17.9000, 11.8125) mm; **0.250 ↔ 0.400 mm**; `overlap_topology_review` / `copper_overlap`.

Inspect the overlapping copper join before editing widths; this is not a simple endpoint transition.

Blockers: pad C6.1.

Track UUIDs: `5f627183-a6db-4b9c-9cdb-c5dd1ab91efd`, `b66e5382-ca95-4347-8215-c204ac2068f4`.

### W085 — +3.3V / F.Cu

(17.9625, 11.8125) mm; **0.150 ↔ 0.250 mm**; `overlap_topology_review` / `copper_overlap`.

Inspect the overlapping copper join before editing widths; this is not a simple endpoint transition.

Blockers: pad C32.2; pad C32.1; pad L1.2; pad C6.1; track d5c323b5-baa1-4d8b-b50e-89b6d36698ba; via d81329fa-92a2-4473-a6d5-78d427db4f3d.

Zone refill required; verify plane continuity after widening.

Track UUIDs: `50475509-9c76-4027-b991-b6be077c2b8f`, `dfdcfb27-b5bd-44b0-83b2-19473435e667`.

### W086 — +3.3V / F.Cu

(17.9625, 11.8125) mm; **0.150 ↔ 0.400 mm**; `overlap_topology_review` / `copper_overlap`.

Inspect the overlapping copper join before editing widths; this is not a simple endpoint transition.

Blockers: pad C32.2; pad C32.1; pad L1.2; track 82f36b29-9ab5-4a56-a853-952df0bacef1; pad C6.2; pad C6.1; track d5c323b5-baa1-4d8b-b50e-89b6d36698ba; via d81329fa-92a2-4473-a6d5-78d427db4f3d; pad Y1.GND-A.

Zone refill required; verify plane continuity after widening.

Track UUIDs: `583e3fda-aac3-4326-9b0c-dff5b83dbe15`, `dfdcfb27-b5bd-44b0-83b2-19473435e667`.

### W087 — +3.3V / F.Cu

(17.9625, 11.8125) mm; **0.150 ↔ 0.400 mm**; `overlap_topology_review` / `copper_overlap`.

Inspect the overlapping copper join before editing widths; this is not a simple endpoint transition.

Blockers: pad C32.2; pad C32.1; pad L1.2; track 82f36b29-9ab5-4a56-a853-952df0bacef1; pad C6.2; pad C6.1; track d5c323b5-baa1-4d8b-b50e-89b6d36698ba; via d81329fa-92a2-4473-a6d5-78d427db4f3d; pad Y1.GND-A.

Zone refill required; verify plane continuity after widening.

Track UUIDs: `b66e5382-ca95-4347-8215-c204ac2068f4`, `dfdcfb27-b5bd-44b0-83b2-19473435e667`.

### W088 — +3.3V / F.Cu

(17.9250, 11.8500) mm; **0.150 ↔ 0.250 mm**; `overlap_topology_review` / `copper_overlap`.

Inspect the overlapping copper join before editing widths; this is not a simple endpoint transition.

Blockers: pad C32.2; pad C32.1; pad L1.2; pad C6.1; track d5c323b5-baa1-4d8b-b50e-89b6d36698ba; via d81329fa-92a2-4473-a6d5-78d427db4f3d.

Zone refill required; verify plane continuity after widening.

Track UUIDs: `c9cf75ae-708a-479c-96e6-e32bd06e13e1`, `dfdcfb27-b5bd-44b0-83b2-19473435e667`.

### W089 — +3.3V / F.Cu

(13.7820, 11.8945) mm; **0.150 ↔ 0.300 mm**; `overlap_topology_review` / `copper_overlap`.

Inspect the overlapping copper join before editing widths; this is not a simple endpoint transition.

Blockers: pad C37.2; pad C1.1.

Zone refill required; verify plane continuity after widening.

Track UUIDs: `8a8bd08b-bc03-4c00-bf93-66940244275c`, `d79ff3c6-ab71-4244-a054-da7a54e96a4d`.

### W090 — +3.3V / F.Cu

(12.6750, 11.9375) mm; **0.200 ↔ 0.300 mm**; `overlap_topology_review` / `copper_overlap`.

Inspect the overlapping copper join before editing widths; this is not a simple endpoint transition.

Blockers: via 218d243f-bfd6-45a3-ae83-5646a368d189.

Zone refill required; verify plane continuity after widening.

Track UUIDs: `02254c29-8180-4c00-8f43-0ca704385a0d`, `cdde7750-576b-42e0-be42-d92723c68cf7`.

### W091 — +3.3V / F.Cu

(12.6875, 11.9375) mm; **0.200 ↔ 0.300 mm**; `overlap_topology_review` / `copper_overlap`.

Inspect the overlapping copper join before editing widths; this is not a simple endpoint transition.

Blockers: via 218d243f-bfd6-45a3-ae83-5646a368d189.

Zone refill required; verify plane continuity after widening.

Track UUIDs: `ab95aa2f-6ef0-4c86-b177-9d6d908a8458`, `cdde7750-576b-42e0-be42-d92723c68cf7`.

### W092 — +3.3V / F.Cu

(12.7000, 11.9599) mm; **0.200 ↔ 0.300 mm**; `overlap_topology_review` / `copper_overlap`.

Inspect the overlapping copper join before editing widths; this is not a simple endpoint transition.

Blockers: via 218d243f-bfd6-45a3-ae83-5646a368d189.

Zone refill required; verify plane continuity after widening.

Track UUIDs: `85416b75-7701-45bb-a8ca-ffcb0d9d8e90`, `cdde7750-576b-42e0-be42-d92723c68cf7`.

### W093 — +3.3V / F.Cu

(13.7165, 11.9599) mm; **0.150 ↔ 0.300 mm**; `overlap_topology_review` / `copper_overlap`.

Inspect the overlapping copper join before editing widths; this is not a simple endpoint transition.

Blockers: pad C37.2; pad C1.1.

Zone refill required; verify plane continuity after widening.

Track UUIDs: `85416b75-7701-45bb-a8ca-ffcb0d9d8e90`, `d79ff3c6-ab71-4244-a054-da7a54e96a4d`.

### W094 — +3.3V / F.Cu

(13.5625, 17.2750) mm; **0.100 ↔ 0.200 mm**; `overlap_topology_review` / `copper_overlap`.

Inspect the overlapping copper join before editing widths; this is not a simple endpoint transition.

Blockers: pad U1.57.

Zone refill required; verify plane continuity after widening.

Track UUIDs: `1adad6c3-aba9-4009-a9e5-5ff19c8395a2`, `a235fd27-bb11-4650-b487-05739362589a`.

### W095 — +3.3V / F.Cu

(13.5026, 17.3000) mm; **0.100 ↔ 0.200 mm**; `overlap_topology_review` / `copper_overlap`.

Inspect the overlapping copper join before editing widths; this is not a simple endpoint transition.

Blockers: pad U1.57.

Zone refill required; verify plane continuity after widening.

Track UUIDs: `1adad6c3-aba9-4009-a9e5-5ff19c8395a2`, `4683de65-0fe5-46ac-a97e-3bb542d2a1cf`.

### W096 — +3.3V / F.Cu

(13.5375, 17.3000) mm; **0.100 ↔ 0.200 mm**; `overlap_topology_review` / `copper_overlap`.

Inspect the overlapping copper join before editing widths; this is not a simple endpoint transition.

Blockers: pad U1.57.

Zone refill required; verify plane continuity after widening.

Track UUIDs: `0317e350-0a7a-4124-bf5f-9eb27bc04b4e`, `1adad6c3-aba9-4009-a9e5-5ff19c8395a2`.

### W097 — +3.3V / F.Cu

(6.4974, 17.7000) mm; **0.200 ↔ 0.300 mm**; `overlap_topology_review` / `copper_overlap`.

Inspect the overlapping copper join before editing widths; this is not a simple endpoint transition.

Blockers: via 70edb013-28f5-45b8-ba9d-d71301e6a4c1; pad U1.28.

Zone refill required; verify plane continuity after widening.

Track UUIDs: `482f7e55-6da0-4e68-ba68-6cffb1a8ce30`, `69a2a252-c14c-4928-80d5-deec7309c1ba`.

### W098 — +3.3V / F.Cu

(6.5099, 17.7125) mm; **0.200 ↔ 0.300 mm**; `overlap_topology_review` / `copper_overlap`.

Inspect the overlapping copper join before editing widths; this is not a simple endpoint transition.

Blockers: via 70edb013-28f5-45b8-ba9d-d71301e6a4c1; pad U1.28.

Zone refill required; verify plane continuity after widening.

Track UUIDs: `69a2a252-c14c-4928-80d5-deec7309c1ba`, `fb42a986-2fe9-4f71-8cf1-d7b61486b58b`.

### W099 — +3.3V / F.Cu

(15.6625, 24.7750) mm; **0.300 ↔ 0.400 mm**; `overlap_topology_review` / `copper_overlap`.

Inspect the overlapping copper join before editing widths; this is not a simple endpoint transition.

Blockers: track a8e4a2d1-7a14-42b3-aab1-644181c94a78; pad U3.5.

Zone refill required; verify plane continuity after widening.

Track UUIDs: `133e8530-e2eb-4c1e-97a5-363267cb7a2b`, `fbcbc6ff-a856-411d-bb3e-18851b0dfb59`.

### W100 — +3.3V / F.Cu

(15.6750, 24.8125) mm; **0.300 ↔ 0.400 mm**; `overlap_topology_review` / `copper_overlap`.

Inspect the overlapping copper join before editing widths; this is not a simple endpoint transition.

Blockers: pad U3.5.

Zone refill required; verify plane continuity after widening.

Track UUIDs: `21895ce1-2009-4c4e-82d5-ead25a05dbb4`, `c4ecb65e-2675-444f-a251-519c177fb4d7`.

### W101 — +3.3V / F.Cu

(15.6875, 24.8250) mm; **0.300 ↔ 0.400 mm**; `overlap_topology_review` / `copper_overlap`.

Inspect the overlapping copper join before editing widths; this is not a simple endpoint transition.

Blockers: pad U3.5.

Zone refill required; verify plane continuity after widening.

Track UUIDs: `21895ce1-2009-4c4e-82d5-ead25a05dbb4`, `dbf2ae00-ad1d-4299-a8d6-47c03ff1044c`.

### W102 — +3.3V / F.Cu

(15.6625, 24.8375) mm; **0.300 ↔ 0.400 mm**; `overlap_topology_review` / `copper_overlap`.

Inspect the overlapping copper join before editing widths; this is not a simple endpoint transition.

Blockers: track a8e4a2d1-7a14-42b3-aab1-644181c94a78; pad U3.5.

Zone refill required; verify plane continuity after widening.

Track UUIDs: `133e8530-e2eb-4c1e-97a5-363267cb7a2b`, `c4ecb65e-2675-444f-a251-519c177fb4d7`.

### W103 — +3.3V / F.Cu

(15.6875, 24.8375) mm; **0.300 ↔ 0.400 mm**; `overlap_topology_review` / `copper_overlap`.

Inspect the overlapping copper join before editing widths; this is not a simple endpoint transition.

Blockers: pad U3.5.

Zone refill required; verify plane continuity after widening.

Track UUIDs: `21895ce1-2009-4c4e-82d5-ead25a05dbb4`, `830dac8a-1cbd-4119-875b-aa3b249119ca`.

### W104 — +3.3V / F.Cu

(15.6625, 24.8500) mm; **0.300 ↔ 0.400 mm**; `overlap_topology_review` / `copper_overlap`.

Inspect the overlapping copper join before editing widths; this is not a simple endpoint transition.

Blockers: track a8e4a2d1-7a14-42b3-aab1-644181c94a78; pad U3.5.

Zone refill required; verify plane continuity after widening.

Track UUIDs: `4384b4f2-b77d-4d74-bc1c-146b589a7fc0`, `c4ecb65e-2675-444f-a251-519c177fb4d7`.

### W105 — +3.3V / F.Cu

(15.6625, 24.8500) mm; **0.300 ↔ 0.400 mm**; `overlap_topology_review` / `copper_overlap`.

Inspect the overlapping copper join before editing widths; this is not a simple endpoint transition.

Blockers: track a8e4a2d1-7a14-42b3-aab1-644181c94a78; pad U3.5.

Zone refill required; verify plane continuity after widening.

Track UUIDs: `4384b4f2-b77d-4d74-bc1c-146b589a7fc0`, `fbcbc6ff-a856-411d-bb3e-18851b0dfb59`.

### W106 — +3.3V / F.Cu

(15.6625, 24.8500) mm; **0.300 ↔ 0.400 mm**; `overlap_topology_review` / `copper_overlap`.

Inspect the overlapping copper join before editing widths; this is not a simple endpoint transition.

Blockers: track a8e4a2d1-7a14-42b3-aab1-644181c94a78; pad U3.5; track 0c51e033-e3ea-4f66-b50c-06bf246a6f8d.

Zone refill required; verify plane continuity after widening.

Track UUIDs: `c4ecb65e-2675-444f-a251-519c177fb4d7`, `c88f44c1-7501-4883-81cb-096c19b21902`.

### W107 — +3.3V / F.Cu

(15.6625, 24.8500) mm; **0.300 ↔ 0.400 mm**; `overlap_topology_review` / `copper_overlap`.

Inspect the overlapping copper join before editing widths; this is not a simple endpoint transition.

Blockers: track a8e4a2d1-7a14-42b3-aab1-644181c94a78; pad U3.5; track 0c51e033-e3ea-4f66-b50c-06bf246a6f8d.

Zone refill required; verify plane continuity after widening.

Track UUIDs: `c88f44c1-7501-4883-81cb-096c19b21902`, `fbcbc6ff-a856-411d-bb3e-18851b0dfb59`.

### W108 — +3.3V / F.Cu

(15.6750, 24.8500) mm; **0.300 ↔ 0.400 mm**; `overlap_topology_review` / `copper_overlap`.

Inspect the overlapping copper join before editing widths; this is not a simple endpoint transition.

Blockers: track a8e4a2d1-7a14-42b3-aab1-644181c94a78; pad U3.5.

Zone refill required; verify plane continuity after widening.

Track UUIDs: `133e8530-e2eb-4c1e-97a5-363267cb7a2b`, `dbf2ae00-ad1d-4299-a8d6-47c03ff1044c`.

### W109 — +3.3V / F.Cu

(15.6687, 24.8562) mm; **0.300 ↔ 0.400 mm**; `overlap_topology_review` / `copper_overlap`.

Inspect the overlapping copper join before editing widths; this is not a simple endpoint transition.

Blockers: track a8e4a2d1-7a14-42b3-aab1-644181c94a78; pad U3.5.

Zone refill required; verify plane continuity after widening.

Track UUIDs: `0bf0f774-4caa-4a64-bfc3-3e81eb402d14`, `c4ecb65e-2675-444f-a251-519c177fb4d7`.

### W110 — +3.3V / F.Cu

(15.6687, 24.8562) mm; **0.300 ↔ 0.400 mm**; `overlap_topology_review` / `copper_overlap`.

Inspect the overlapping copper join before editing widths; this is not a simple endpoint transition.

Blockers: track a8e4a2d1-7a14-42b3-aab1-644181c94a78; pad U3.5.

Zone refill required; verify plane continuity after widening.

Track UUIDs: `0bf0f774-4caa-4a64-bfc3-3e81eb402d14`, `fbcbc6ff-a856-411d-bb3e-18851b0dfb59`.

### W111 — +3.3V / F.Cu

(15.6687, 24.8562) mm; **0.300 ↔ 0.400 mm**; `overlap_topology_review` / `copper_overlap`.

Inspect the overlapping copper join before editing widths; this is not a simple endpoint transition.

Blockers: track a8e4a2d1-7a14-42b3-aab1-644181c94a78; pad U3.5.

Zone refill required; verify plane continuity after widening.

Track UUIDs: `f2ba0ebc-b89f-4fa3-ae6d-051e850ec4fe`, `fbcbc6ff-a856-411d-bb3e-18851b0dfb59`.

### W112 — +3.3V / F.Cu

(15.6750, 24.8625) mm; **0.300 ↔ 0.400 mm**; `overlap_topology_review` / `copper_overlap`.

Inspect the overlapping copper join before editing widths; this is not a simple endpoint transition.

Blockers: track a8e4a2d1-7a14-42b3-aab1-644181c94a78; pad U3.5.

Zone refill required; verify plane continuity after widening.

Track UUIDs: `133e8530-e2eb-4c1e-97a5-363267cb7a2b`, `830dac8a-1cbd-4119-875b-aa3b249119ca`.

### W113 — +3.3V / F.Cu

(15.6750, 24.8625) mm; **0.300 ↔ 0.400 mm**; `overlap_topology_review` / `copper_overlap`.

Inspect the overlapping copper join before editing widths; this is not a simple endpoint transition.

Blockers: track a8e4a2d1-7a14-42b3-aab1-644181c94a78; pad U3.5.

Zone refill required; verify plane continuity after widening.

Track UUIDs: `4384b4f2-b77d-4d74-bc1c-146b589a7fc0`, `dbf2ae00-ad1d-4299-a8d6-47c03ff1044c`.

### W114 — +3.3V / F.Cu

(15.6750, 24.8750) mm; **0.300 ↔ 0.400 mm**; `overlap_topology_review` / `copper_overlap`.

Inspect the overlapping copper join before editing widths; this is not a simple endpoint transition.

Blockers: track a8e4a2d1-7a14-42b3-aab1-644181c94a78; pad U3.5.

Zone refill required; verify plane continuity after widening.

Track UUIDs: `4384b4f2-b77d-4d74-bc1c-146b589a7fc0`, `830dac8a-1cbd-4119-875b-aa3b249119ca`.

### W115 — +3.3V / F.Cu

(15.6937, 24.8813) mm; **0.300 ↔ 0.400 mm**; `overlap_topology_review` / `copper_overlap`.

Inspect the overlapping copper join before editing widths; this is not a simple endpoint transition.

Blockers: track a8e4a2d1-7a14-42b3-aab1-644181c94a78; pad U3.5.

Zone refill required; verify plane continuity after widening.

Track UUIDs: `c4ecb65e-2675-444f-a251-519c177fb4d7`, `f2ba0ebc-b89f-4fa3-ae6d-051e850ec4fe`.

### W116 — +3.3V / F.Cu

(15.7000, 24.8875) mm; **0.300 ↔ 0.400 mm**; `overlap_topology_review` / `copper_overlap`.

Inspect the overlapping copper join before editing widths; this is not a simple endpoint transition.

Blockers: track a8e4a2d1-7a14-42b3-aab1-644181c94a78; pad U3.5.

Zone refill required; verify plane continuity after widening.

Track UUIDs: `0358ecbd-b91b-4207-8cee-1d18262dea0b`, `830dac8a-1cbd-4119-875b-aa3b249119ca`.

### W117 — +3.3V / F.Cu

(15.6750, 24.9000) mm; **0.300 ↔ 0.400 mm**; `overlap_topology_review` / `copper_overlap`.

Inspect the overlapping copper join before editing widths; this is not a simple endpoint transition.

Blockers: track a8e4a2d1-7a14-42b3-aab1-644181c94a78; pad U3.5; track 0c51e033-e3ea-4f66-b50c-06bf246a6f8d.

Zone refill required; verify plane continuity after widening.

Track UUIDs: `830dac8a-1cbd-4119-875b-aa3b249119ca`, `c88f44c1-7501-4883-81cb-096c19b21902`.

### W118 — +3.3V / F.Cu

(15.6750, 24.9000) mm; **0.300 ↔ 0.400 mm**; `overlap_topology_review` / `copper_overlap`.

Inspect the overlapping copper join before editing widths; this is not a simple endpoint transition.

Blockers: track a8e4a2d1-7a14-42b3-aab1-644181c94a78; pad U3.5; track 0c51e033-e3ea-4f66-b50c-06bf246a6f8d.

Zone refill required; verify plane continuity after widening.

Track UUIDs: `c88f44c1-7501-4883-81cb-096c19b21902`, `dbf2ae00-ad1d-4299-a8d6-47c03ff1044c`.

### W119 — +3.3V / F.Cu

(15.6750, 25.0625) mm; **0.300 ↔ 0.400 mm**; `overlap_topology_review` / `copper_overlap`.

Inspect the overlapping copper join before editing widths; this is not a simple endpoint transition.

Blockers: track a8e4a2d1-7a14-42b3-aab1-644181c94a78; pad U3.5; track 0c51e033-e3ea-4f66-b50c-06bf246a6f8d.

Zone refill required; verify plane continuity after widening.

Track UUIDs: `dbf2ae00-ad1d-4299-a8d6-47c03ff1044c`, `eb1fbcee-b8f7-4895-8aa1-a2832499ca75`.

### W120 — +3.3V / F.Cu

(15.7000, 25.0875) mm; **0.300 ↔ 0.400 mm**; `overlap_topology_review` / `copper_overlap`.

Inspect the overlapping copper join before editing widths; this is not a simple endpoint transition.

Blockers: track a8e4a2d1-7a14-42b3-aab1-644181c94a78; pad U3.5; track 0c51e033-e3ea-4f66-b50c-06bf246a6f8d.

Zone refill required; verify plane continuity after widening.

Track UUIDs: `830dac8a-1cbd-4119-875b-aa3b249119ca`, `eb1fbcee-b8f7-4895-8aa1-a2832499ca75`.

### W121 — +3.3V / F.Cu

(12.2500, 33.1850) mm; **0.250 ↔ 0.400 mm**; `overlap_topology_review` / `copper_overlap`.

Inspect the overlapping copper join before editing widths; this is not a simple endpoint transition.

Blockers: via 4b386c5b-0373-492b-9162-66a3ff590934.

Zone refill required; verify plane continuity after widening.

Track UUIDs: `0bf4d4ec-e4c5-40f6-97b3-481190c83370`, `32b01eed-d7c3-4936-9d79-905c7e2d6447`.

### W122 — +3.3V / F.Cu

(12.2250, 33.2000) mm; **0.250 ↔ 0.400 mm**; `overlap_topology_review` / `copper_overlap`.

Inspect the overlapping copper join before editing widths; this is not a simple endpoint transition.

Blockers: via 4b386c5b-0373-492b-9162-66a3ff590934.

Zone refill required; verify plane continuity after widening.

Track UUIDs: `32b01eed-d7c3-4936-9d79-905c7e2d6447`, `93825af3-f365-414c-8512-2fa25e898264`.

### W123 — +3.3V / F.Cu

(7.7322, 34.5476) mm; **0.100 ↔ 0.200 mm**; `overlap_topology_review` / `copper_overlap`.

Inspect the overlapping copper join before editing widths; this is not a simple endpoint transition.

Blockers: pad SJ1.2; pad SJ1.3; via 73571995-cbf2-4ce4-b487-be077b9cc435.

Track UUIDs: `390ef521-138c-482e-a9f7-8f8e3ec6d593`, `86f8c49a-c0ae-4a1f-9163-13eb4d5bf07f`.

### W124 — +3.3V / F.Cu

(8.2375, 36.3250) mm; **0.100 ↔ 0.400 mm**; `overlap_topology_review` / `copper_overlap`.

Inspect the overlapping copper join before editing widths; this is not a simple endpoint transition.

Blockers: pad U2.23; track 6cf4e8b5-4f66-46f2-ab77-b527f596a957; track 00a58d13-5480-4411-8f9d-fe6cb53df2b3; track 47299f60-cd60-48c8-b250-37138a606504.

Track UUIDs: `49a96588-e8ee-41e5-829b-05e823518f82`, `eead542b-573e-4a3c-b490-6cc3f37f126e`.

### W125 — +3.3V / F.Cu

(13.8688, 42.2188) mm; **0.100 ↔ 0.200 mm**; `overlap_topology_review` / `copper_overlap`.

Inspect the overlapping copper join before editing widths; this is not a simple endpoint transition.

Blockers: via a3159c4a-d259-486d-9a24-dbcd1a0c1255; track a7d53fc6-860b-4fa2-b9d4-fc7afc42f54c; track 8a68faa2-e40b-481e-88a3-3b98fea640fe.

Zone refill required; verify plane continuity after widening.

Track UUIDs: `79da0a7b-035b-45d3-a8ff-cb176da04105`, `987b2137-9f15-4460-acb8-23b115eecaf7`.

### W126 — +3.3V / F.Cu

(13.8375, 42.2500) mm; **0.100 ↔ 0.200 mm**; `overlap_topology_review` / `copper_overlap`.

Inspect the overlapping copper join before editing widths; this is not a simple endpoint transition.

Blockers: via a3159c4a-d259-486d-9a24-dbcd1a0c1255; track a7d53fc6-860b-4fa2-b9d4-fc7afc42f54c; track 8a68faa2-e40b-481e-88a3-3b98fea640fe.

Zone refill required; verify plane continuity after widening.

Track UUIDs: `987b2137-9f15-4460-acb8-23b115eecaf7`, `d5730c9f-7df4-435c-a721-8f8cbec2a067`.

### W127 — +3.3V / F.Cu

(14.2375, 43.7125) mm; **0.150 ↔ 0.400 mm**; `overlap_topology_review` / `copper_overlap`.

Inspect the overlapping copper join before editing widths; this is not a simple endpoint transition.

Blockers: pad D1.P$4; pad D1.P$3.

Track UUIDs: `710f5547-603a-47dd-adad-0a1a31b92567`, `beb0a547-3e5d-496d-88d8-a33bb560269f`.

### W128 — +3.3V / F.Cu

(14.2000, 43.7375) mm; **0.150 ↔ 0.400 mm**; `overlap_topology_review` / `copper_overlap`.

Inspect the overlapping copper join before editing widths; this is not a simple endpoint transition.

Blockers: pad D1.P$4; pad D1.P$3.

Track UUIDs: `4a4fdd32-407a-4332-8d2b-6915c145b524`, `710f5547-603a-47dd-adad-0a1a31b92567`.

### W129 — +3.3V / F.Cu

(14.2125, 43.7375) mm; **0.150 ↔ 0.400 mm**; `overlap_topology_review` / `copper_overlap`.

Inspect the overlapping copper join before editing widths; this is not a simple endpoint transition.

Blockers: pad D1.P$4; pad D1.P$3.

Track UUIDs: `033383cf-b9dd-4b20-bc3b-85173580e284`, `710f5547-603a-47dd-adad-0a1a31b92567`.

### W130 — +3.3V / F.Cu

(14.1875, 43.7500) mm; **0.150 ↔ 0.400 mm**; `overlap_topology_review` / `copper_overlap`.

Inspect the overlapping copper join before editing widths; this is not a simple endpoint transition.

Blockers: pad D1.P$4; pad D1.P$3.

Track UUIDs: `64fa98f9-6272-4a69-8cb6-bdba1dee4b3e`, `710f5547-603a-47dd-adad-0a1a31b92567`.

### W131 — ESP_VDD3P3 / F.Cu

(11.6750, 10.6750) mm; **0.100 ↔ 0.250 mm**; `overlap_topology_review` / `copper_overlap`.

Inspect the overlapping copper join before editing widths; this is not a simple endpoint transition.

Blockers: pad L3.1.

Zone refill required; verify plane continuity after widening.

Track UUIDs: `2b9e829c-ba18-4618-ba0b-115e21e84012`, `7f1ee53b-829e-4e3e-996e-008169a57ad3`.

### W132 — ESP_VDD3P3 / F.Cu

(18.0025, 10.9250) mm; **0.200 ↔ 0.250 mm**; `overlap_topology_review` / `copper_overlap`.

Inspect the overlapping copper join before editing widths; this is not a simple endpoint transition.

Blockers: pad R22.1; via e128b6fe-f854-4b47-82fe-e2759cc05e3f; pad L1.1; pad L3.2; pad L3.1; track a85e8c30-1f3d-4fa0-8348-ff209ff313b7; via 32141843-2452-4ebb-820d-46620f78dfbb.

Zone refill required; verify plane continuity after widening.

Track UUIDs: `1325266b-96e5-49ee-bd82-fbf511640759`, `1733a48f-7bf7-42a6-ab6c-9e53b7e274f6`.

### W133 — FPGA_VCCIO0 / F.Cu

(3.7226, 40.7500) mm; **0.100 ↔ 0.150 mm**; `overlap_topology_review` / `copper_overlap`.

Inspect the overlapping copper join before editing widths; this is not a simple endpoint transition.

Blockers: via 3b18a63f-68e8-4fc7-af82-358083e0bcf0.

Zone refill required; verify plane continuity after widening.

Track UUIDs: `e201305d-5fa2-4e5a-a857-97313e82ceef`, `e8bb8deb-87e0-4343-b280-ff4096d06489`.

### W134 — FPGA_VCCIO0 / F.Cu

(4.7846, 40.7750) mm; **0.100 ↔ 0.200 mm**; `overlap_topology_review` / `copper_overlap`.

Inspect the overlapping copper join before editing widths; this is not a simple endpoint transition.

Blockers: track d1dc0a1e-b56e-45d5-9233-0c47b4bce818; via 3b18a63f-68e8-4fc7-af82-358083e0bcf0; pad C46.2.

Zone refill required; verify plane continuity after widening.

Track UUIDs: `2e249688-455f-4696-b856-02a73b412c5d`, `e8bb8deb-87e0-4343-b280-ff4096d06489`.

### W135 — FPGA_VCCIO0 / F.Cu

(5.3750, 40.7750) mm; **0.100 ↔ 0.200 mm**; `overlap_topology_review` / `copper_overlap`.

Inspect the overlapping copper join before editing widths; this is not a simple endpoint transition.

Blockers: track d1dc0a1e-b56e-45d5-9233-0c47b4bce818; via 3b18a63f-68e8-4fc7-af82-358083e0bcf0; pad C46.2.

Zone refill required; verify plane continuity after widening.

Track UUIDs: `ce49a44b-41ba-47b7-8747-bba1065628f8`, `e8bb8deb-87e0-4343-b280-ff4096d06489`.

### W136 — FPGA_VCCIO0 / F.Cu

(6.0702, 40.8000) mm; **0.100 ↔ 0.200 mm**; `overlap_topology_review` / `copper_overlap`.

Inspect the overlapping copper join before editing widths; this is not a simple endpoint transition.

Blockers: track d1dc0a1e-b56e-45d5-9233-0c47b4bce818; via 3b18a63f-68e8-4fc7-af82-358083e0bcf0; pad C46.2.

Zone refill required; verify plane continuity after widening.

Track UUIDs: `04d7849b-7f2d-42da-be96-8edd8f0e28f6`, `4d70c820-c2bf-4c9e-9814-675329155028`.

### W137 — FPGA_VCCIO0 / F.Cu

(5.5375, 40.8375) mm; **0.100 ↔ 0.200 mm**; `overlap_topology_review` / `copper_overlap`.

Inspect the overlapping copper join before editing widths; this is not a simple endpoint transition.

Blockers: track d1dc0a1e-b56e-45d5-9233-0c47b4bce818; via 3b18a63f-68e8-4fc7-af82-358083e0bcf0; pad C46.2.

Zone refill required; verify plane continuity after widening.

Track UUIDs: `4a2a9bdc-00f8-4d40-b266-75e1f2ae8d40`, `5eaf5e92-0f1b-4fd5-be96-4007bf2ce4fd`.

### W138 — FPGA_VCCIO0 / F.Cu

(5.9500, 40.8601) mm; **0.100 ↔ 0.200 mm**; `overlap_topology_review` / `copper_overlap`.

Inspect the overlapping copper join before editing widths; this is not a simple endpoint transition.

Blockers: track d1dc0a1e-b56e-45d5-9233-0c47b4bce818; via 3b18a63f-68e8-4fc7-af82-358083e0bcf0; pad C46.2.

Zone refill required; verify plane continuity after widening.

Track UUIDs: `04d7849b-7f2d-42da-be96-8edd8f0e28f6`, `258132fe-5c07-4c91-95be-39cfc50c2537`.

### W139 — FPGA_VCCIO0 / F.Cu

(5.5875, 40.8875) mm; **0.100 ↔ 0.200 mm**; `overlap_topology_review` / `copper_overlap`.

Inspect the overlapping copper join before editing widths; this is not a simple endpoint transition.

Blockers: track d1dc0a1e-b56e-45d5-9233-0c47b4bce818; via 3b18a63f-68e8-4fc7-af82-358083e0bcf0; pad C46.2.

Zone refill required; verify plane continuity after widening.

Track UUIDs: `04d7849b-7f2d-42da-be96-8edd8f0e28f6`, `5eaf5e92-0f1b-4fd5-be96-4007bf2ce4fd`.

### W140 — GND / B.Cu

(13.1000, 39.1250) mm; **0.100 ↔ 0.200 mm**; `overlap_topology_review` / `copper_overlap`.

Inspect the overlapping copper join before editing widths; this is not a simple endpoint transition.

Blockers: pad J2.2.

Track UUIDs: `3fd4c4ad-7507-4c69-adb1-0f40ee10f1ae`, `98153eae-0024-4938-a3e6-e34c1bfffba3`.

### W141 — GND / B.Cu

(13.1000, 39.1750) mm; **0.100 ↔ 0.200 mm**; `overlap_topology_review` / `copper_overlap`.

Inspect the overlapping copper join before editing widths; this is not a simple endpoint transition.

Blockers: pad J2.2.

Track UUIDs: `3fd4c4ad-7507-4c69-adb1-0f40ee10f1ae`, `44e346ce-99b6-4457-9dbd-15a5889d71f3`.

### W142 — GND / B.Cu

(10.7250, 39.3375) mm; **0.100 ↔ 0.150 mm**; `overlap_topology_review` / `copper_overlap`.

Inspect the overlapping copper join before editing widths; this is not a simple endpoint transition.

Blockers: track e6f2f6da-31a9-4c69-9d78-e7353ef60b48.

Track UUIDs: `3cca13e7-5066-43ba-b509-b9af703dc690`, `6a132136-311d-4c2d-9313-7af69219d9ad`.

### W143 — GND / B.Cu

(10.7250, 39.3375) mm; **0.100 ↔ 0.150 mm**; `overlap_topology_review` / `copper_overlap`.

Inspect the overlapping copper join before editing widths; this is not a simple endpoint transition.

Blockers: track ad4a5e25-3ae6-446e-a1ad-9c9199be8ba1; track fb8bd343-ea94-4aca-b160-b1038518e06c; track 7837d937-d90d-4240-aabf-b84394e38619.

Track UUIDs: `3cca13e7-5066-43ba-b509-b9af703dc690`, `9fbcb8a6-fad1-4ddc-b1ba-17b22a6ba05d`.

### W144 — GND / B.Cu

(10.7250, 39.3500) mm; **0.100 ↔ 0.150 mm**; `overlap_topology_review` / `copper_overlap`.

Inspect the overlapping copper join before editing widths; this is not a simple endpoint transition.

Blockers: track ad4a5e25-3ae6-446e-a1ad-9c9199be8ba1; track fb8bd343-ea94-4aca-b160-b1038518e06c; track 7837d937-d90d-4240-aabf-b84394e38619.

Track UUIDs: `082ff6f0-d0c5-447c-9850-21ffa0fc0c3f`, `3cca13e7-5066-43ba-b509-b9af703dc690`.

### W145 — GND / B.Cu

(10.7250, 39.3875) mm; **0.100 ↔ 0.150 mm**; `overlap_topology_review` / `copper_overlap`.

Inspect the overlapping copper join before editing widths; this is not a simple endpoint transition.

Blockers: track ad4a5e25-3ae6-446e-a1ad-9c9199be8ba1; track fb8bd343-ea94-4aca-b160-b1038518e06c; track 7837d937-d90d-4240-aabf-b84394e38619.

Track UUIDs: `082ff6f0-d0c5-447c-9850-21ffa0fc0c3f`, `99b6ede0-ef80-4916-b40c-457a2596a6fa`.

### W146 — GND / B.Cu

(12.8750, 39.4875) mm; **0.200 ↔ 0.250 mm**; `overlap_topology_review` / `copper_overlap`.

Inspect the overlapping copper join before editing widths; this is not a simple endpoint transition.

Blockers: pad J2.2.

Track UUIDs: `3cae1169-fff2-4a52-84c4-9c38b23df04e`, `44e346ce-99b6-4457-9dbd-15a5889d71f3`.

### W147 — GND / F.Cu

(17.2250, 15.7375) mm; **0.150 ↔ 0.250 mm**; `overlap_topology_review` / `copper_overlap`.

Inspect the overlapping copper join before editing widths; this is not a simple endpoint transition.

Blockers: track 593dcb02-9008-4763-8d34-e989d22f4f8e.

Track UUIDs: `0894003a-6897-4a78-934d-cec2be879c9a`, `24c2b684-67cd-4ae3-afc8-34a710a5c29c`.

### W148 — GND / F.Cu

(17.2125, 15.7500) mm; **0.150 ↔ 0.250 mm**; `overlap_topology_review` / `copper_overlap`.

Inspect the overlapping copper join before editing widths; this is not a simple endpoint transition.

Blockers: track 593dcb02-9008-4763-8d34-e989d22f4f8e.

Track UUIDs: `0894003a-6897-4a78-934d-cec2be879c9a`, `ba49abec-3070-431c-97d5-b15073dbe955`.

### W149 — GND / F.Cu

(17.2125, 15.7625) mm; **0.150 ↔ 0.250 mm**; `overlap_topology_review` / `copper_overlap`.

Inspect the overlapping copper join before editing widths; this is not a simple endpoint transition.

Blockers: track 593dcb02-9008-4763-8d34-e989d22f4f8e.

Track UUIDs: `04d2538a-be43-4ec7-a563-dc43ce30b3f3`, `0894003a-6897-4a78-934d-cec2be879c9a`.

### W150 — GND / F.Cu

(17.1875, 15.7875) mm; **0.150 ↔ 0.250 mm**; `overlap_topology_review` / `copper_overlap`.

Inspect the overlapping copper join before editing widths; this is not a simple endpoint transition.

Blockers: track 593dcb02-9008-4763-8d34-e989d22f4f8e.

Track UUIDs: `0894003a-6897-4a78-934d-cec2be879c9a`, `1a9de834-f86c-470a-89b0-dfcf06990055`.

### W151 — GND / F.Cu

(19.4750, 16.2000) mm; **0.200 ↔ 0.250 mm**; `overlap_topology_review` / `copper_overlap`.

Inspect the overlapping copper join before editing widths; this is not a simple endpoint transition.

Blockers: pad Y1.OUT/IN.

Track UUIDs: `3cd6e990-1d4b-4d85-b81c-510ef47cb569`, `8c848de0-1d0f-4b9e-badd-dd60c30c383b`.

### W152 — GND / F.Cu

(19.4625, 16.2250) mm; **0.200 ↔ 0.250 mm**; `overlap_topology_review` / `copper_overlap`.

Inspect the overlapping copper join before editing widths; this is not a simple endpoint transition.

Blockers: pad Y1.OUT/IN.

Track UUIDs: `54f9072c-a614-4565-8c5c-b2f7f760fa69`, `a25ed502-f7c0-4d65-ae1e-7e2351a2ce4f`.

### W153 — GND / F.Cu

(19.4625, 16.2375) mm; **0.200 ↔ 0.250 mm**; `overlap_topology_review` / `copper_overlap`.

Inspect the overlapping copper join before editing widths; this is not a simple endpoint transition.

Blockers: pad Y1.OUT/IN.

Track UUIDs: `1bbcf8ad-f911-4220-9668-b23774c1e8be`, `a25ed502-f7c0-4d65-ae1e-7e2351a2ce4f`.

### W154 — GND / F.Cu

(19.4500, 16.2500) mm; **0.200 ↔ 0.250 mm**; `overlap_topology_review` / `copper_overlap`.

Inspect the overlapping copper join before editing widths; this is not a simple endpoint transition.

Blockers: pad Y1.OUT/IN.

Track UUIDs: `1bbcf8ad-f911-4220-9668-b23774c1e8be`, `3cd6e990-1d4b-4d85-b81c-510ef47cb569`.

### W155 — GND / F.Cu

(19.1750, 16.5250) mm; **0.200 ↔ 0.250 mm**; `overlap_topology_review` / `copper_overlap`.

Inspect the overlapping copper join before editing widths; this is not a simple endpoint transition.

Blockers: pad Y1.OUT/IN.

Track UUIDs: `3cd6e990-1d4b-4d85-b81c-510ef47cb569`, `c78cb7fb-94ec-43f7-b24c-be1846f461c1`.

### W156 — GND / F.Cu

(19.1500, 16.5500) mm; **0.200 ↔ 0.250 mm**; `overlap_topology_review` / `copper_overlap`.

Inspect the overlapping copper join before editing widths; this is not a simple endpoint transition.

Blockers: pad Y1.OUT/IN.

Track UUIDs: `1bbcf8ad-f911-4220-9668-b23774c1e8be`, `924f1d9c-62ce-4de0-afdb-63b40c6fc113`.

### W157 — GND / F.Cu

(19.1500, 16.5500) mm; **0.200 ↔ 0.250 mm**; `overlap_topology_review` / `copper_overlap`.

Inspect the overlapping copper join before editing widths; this is not a simple endpoint transition.

Blockers: pad Y1.OUT/IN.

Track UUIDs: `1bbcf8ad-f911-4220-9668-b23774c1e8be`, `eb2b3a44-64ad-471b-8c0f-9bc62e2de0dd`.

### W158 — GND / F.Cu

(19.1500, 16.5750) mm; **0.200 ↔ 0.250 mm**; `overlap_topology_review` / `copper_overlap`.

Inspect the overlapping copper join before editing widths; this is not a simple endpoint transition.

Blockers: pad Y1.OUT/IN.

Track UUIDs: `c78cb7fb-94ec-43f7-b24c-be1846f461c1`, `eb2b3a44-64ad-471b-8c0f-9bc62e2de0dd`.

### W159 — GND / F.Cu

(19.1500, 17.0000) mm; **0.200 ↔ 0.250 mm**; `overlap_topology_review` / `copper_overlap`.

Inspect the overlapping copper join before editing widths; this is not a simple endpoint transition.

Blockers: pad Y1.OUT/IN.

Track UUIDs: `924f1d9c-62ce-4de0-afdb-63b40c6fc113`, `c78cb7fb-94ec-43f7-b24c-be1846f461c1`.

### W160 — GND / F.Cu

(16.6375, 22.9125) mm; **0.150 ↔ 0.250 mm**; `overlap_topology_review` / `copper_overlap`.

Inspect the overlapping copper join before editing widths; this is not a simple endpoint transition.

Blockers: pad U3.2; pad U3.3; track f3b4c344-aba7-4f78-bb5a-d8f7c18674c0.

Track UUIDs: `d289bb99-7cda-425a-a309-bc6640437031`, `f803cf5a-7e9f-4232-af82-0d925307aaf5`.

### W161 — GND / F.Cu

(16.7125, 22.9625) mm; **0.150 ↔ 0.250 mm**; `overlap_topology_review` / `copper_overlap`.

Inspect the overlapping copper join before editing widths; this is not a simple endpoint transition.

Blockers: track f3b4c344-aba7-4f78-bb5a-d8f7c18674c0.

Track UUIDs: `32990613-fb35-4ec0-ab27-38a3e34e4cf0`, `842dd64b-d6b8-4701-9574-bf43697eb43e`.

### W162 — GND / F.Cu

(16.6875, 23.0500) mm; **0.150 ↔ 0.250 mm**; `overlap_topology_review` / `copper_overlap`.

Inspect the overlapping copper join before editing widths; this is not a simple endpoint transition.

Blockers: pad U3.2; pad U3.3; track f3b4c344-aba7-4f78-bb5a-d8f7c18674c0.

Track UUIDs: `842dd64b-d6b8-4701-9574-bf43697eb43e`, `d289bb99-7cda-425a-a309-bc6640437031`.

### W163 — VIN_5V / B.Cu

(13.8000, 14.3775) mm; **0.200 ↔ 0.400 mm**; `overlap_topology_review` / `copper_overlap`.

Inspect the overlapping copper join before editing widths; this is not a simple endpoint transition.

Blockers: via e01403df-2be0-4644-a730-7a0ac54d009a.

Zone refill required; verify plane continuity after widening.

Track UUIDs: `277c8d73-5fca-45ce-a290-76285610c07c`, `6c7c7b69-03f0-4c29-91de-f5416eb0881c`.

### W164 — VIN_5V / B.Cu

(13.0000, 15.1775) mm; **0.300 ↔ 0.400 mm**; `overlap_topology_review` / `copper_overlap`.

Inspect the overlapping copper join before editing widths; this is not a simple endpoint transition.

Blockers: track b262dd2b-d54a-4a15-85c5-399fbe2cf63e.

Zone refill required; verify plane continuity after widening.

Track UUIDs: `226259e1-0627-4110-a7eb-ef2edef884d3`, `37684a37-6518-4ecf-ad4d-252c21509aaf`.

## Limits

- Read-only geometry triage, not a DRC waiver or electrical approval.
- Counts are contacting different-width track pairs; multiple pairs can share a branch location.
- Uses the largest configured netclass clearance conservatively; custom .kicad_dru rules require KiCad DRC.
- Pad outlines use 1 um polygon approximation; arcs use <=5 um sampling.
- Filled foreign zones are reported separately: widening requires refill plus plane-connectivity checks. No impedance/current requirements are inferred.
