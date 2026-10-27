# Conformance

Pinned program instances used to test whether an implementation behaves as USG v0.12 specifies.

- `fail_no_need.json` — strategic stop at S01
- `fail_all_sites_prohibited.json` — all site candidates prohibited
- `instance_adu_backyard.json` — exploratory ADU/site-envelope case
- `stress_one_mile_city.json` — design-ahead-of-premise stress case

Run the mutation suite with `python tests/test_runner.py protocol/versions/USG_v0_12.json` and each instance with `python tools/run_usg.py protocol/versions/USG_v0_12.json conformance/instances/<file>.json`. CI runs both against the version named in `protocol/CURRENT`.
