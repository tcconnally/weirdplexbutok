"""Static guardrails for the public status display.

Run with:
    python tests/run_static_guards.py
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"


def page() -> str:
    return INDEX.read_text(encoding="utf-8")


def test_header_does_not_claim_online_before_verified_status():
    text = page()
    header = text.split('<main class="hologram-container">', 1)[0]
    assert "greg.status unknown" in header
    assert "<span>greg.online</span>" not in header


def test_no_faux_health_pools_drive_availability_or_ticker():
    text = page()
    assert "FAUX_SYS" not in text
    assert "FAUX_MEDIA" not in text
    assert "faux" not in text.lower()
    assert "smart green" not in text
    assert "containers stable" not in text
    assert "indexers green" not in text


def test_status_payload_must_be_fresh_before_it_counts_as_live():
    text = page()
    assert "STATUS_MAX_AGE_MS" in text
    assert "function isStatusFresh" in text
    assert "statusAgeMs" in text
    assert "return d.online === false ? 'offline' : 'online';" in text


def test_unverified_status_is_labeled_unknown_or_stale():
    text = page()
    assert "greg.status unknown" in text
    assert "`greg.${mode}`" in text
    assert "stale: 'var(--neon-yellow)'" in text
    assert "unknown: 'var(--neon-yellow)'" in text
    assert "no current health assertion" in text
    assert "availability unknown" in text
    assert "telemetry stale" in text


def test_ticker_uses_live_data_or_truthful_fallback_only():
    text = page()
    assert "buildSysMsgs(d).concat(buildMediaMsgs(d))" in text
    assert "waiting for live telemetry" in text
    assert "no current health assertion" in text
    assert "live.concat" not in text
    assert "concat(faux)" not in text
