import pytest
from scholarship_awards import award_amount, is_eligible, application_status


# Tests for award_amount
def test_award_amount_unknown_category():
    with pytest.raises(ValueError, match="unknown category"):
        award_amount("engineering", 80, "low", False)


def test_award_amount_invalid_marks():
    with pytest.raises(ValueError, match="invalid marks"):
        award_amount("merit", -5, "low", False)


def test_award_amount_below_or_equal_cutoff():
    assert award_amount("merit", 70, "low", False) == 0
    assert award_amount("merit", 75, "low", False) == 0


def test_award_amount_renewal_merit_low_income():
    # renewal merit: cutoff 70, marks 80 -> above 10 <= 15 -> rate 100 -> 1000
    assert award_amount("merit", 80, "low", True) == 1000


def test_award_amount_non_low_income_bonus():
    # arts cutoff 65, marks 85 -> above 20 > 15 -> rate 60 + 40 = 100 -> 2000
    assert award_amount("arts", 85, "medium", False) == 2000


def test_award_amount_low_income_bonus():
    # merit cutoff 75, marks 95 -> above 20 > 15 -> rate 100 + 40 + 20 = 160 -> 3200
    assert award_amount("merit", 95, "low", False) == 3200


# Tests for is_eligible
def test_is_eligible_special_quota():
    assert is_eligible(60, 2, True) is True
    assert is_eligible(90, 3, True) is False


def test_is_eligible_regular_low_attendance():
    assert is_eligible(70, 0, False) is False


def test_is_eligible_regular_backlogs():
    assert is_eligible(90, 0, False) is True
    assert is_eligible(80, 1, False) is True
    assert is_eligible(80, 2, False) is False


# Tests for application_status
def test_application_status_renewal_paper_open():
    assert application_status(40, True, True) == "open"


def test_application_status_regular_electronic_closing():
    assert application_status(10, False, False) == "closing"


def test_application_status_regular_electronic_closed():
    assert application_status(4, False, False) == "closed"
