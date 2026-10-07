import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import pytest


@pytest.fixture
def identity_calibration(tmp_path, monkeypatch):
    """Instrument physics tests run against identity calibration maps, so they do not depend on the
    fitted files in config/calibration (those are checked separately in test_calibration_files)."""
    from satclip import calibration
    monkeypatch.setattr(calibration, "CAL_DIR", tmp_path / "no-calibration")
    calibration.load.cache_clear()
    yield
    calibration.load.cache_clear()
