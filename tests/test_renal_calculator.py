from app.tools.renal_calculator import check_renal_threshold


def test_metformin_contraindicated_below_30():
    r = check_renal_threshold("metformin", 25)
    assert r["status"] == "contraindicated"


def test_metformin_initiation_not_recommended_30_45():
    assert check_renal_threshold("Metformin", 40)["status"] == "initiation_not_recommended"


def test_metformin_no_restriction_above_45():
    assert check_renal_threshold("metformin", 80)["status"].startswith("no_renal")


def test_unknown_drug_returns_error():
    assert "error" in check_renal_threshold("warfarin", 50)