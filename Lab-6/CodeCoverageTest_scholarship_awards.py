import pytest
from scholarship_awards import award_amount, is_eligible, application_status


class TestScholarshipAwardsCodeCoverage:
    """Test suite designed to achieve 100% statement/line coverage for scholarship_awards.py."""

    # 1. Tests for award_amount
    def test_award_amount_unknown_category_raises(self):
        with pytest.raises(ValueError, match="unknown category"):
            award_amount("engineering", 80, "low", False)

    def test_award_amount_invalid_negative_marks_raises(self):
        with pytest.raises(ValueError, match="invalid marks"):
            award_amount("merit", -5, "low", False)

    def test_award_amount_marks_below_or_equal_cutoff(self):
        # merit cutoff is 75, marks=75 -> above = 0 <= 0 -> 0
        assert award_amount("merit", 75, "low", False) == 0
        # marks=70 -> above = -5 <= 0 -> 0
        assert award_amount("merit", 70, "low", False) == 0

    def test_award_amount_renewal_merit_low_income_no_bonus(self):
        # merit renewal cutoff = 75 - 5 = 70. Marks = 80 -> above = 10 (<= 15)
        # income_level == "low" -> rate = 100. Award = 10 * 100 = 1000
        assert award_amount("merit", 80, "low", True) == 1000

    def test_award_amount_non_low_income_with_bonus(self):
        # arts cutoff = 65, is_renewal = False. Marks = 85 -> above = 20 (> 15)
        # income_level == "medium" -> rate = 60 + 40 = 100. Award = 20 * 100 = 2000
        assert award_amount("arts", 85, "medium", False) == 2000

    def test_award_amount_low_income_with_bonus(self):
        # merit cutoff = 75, is_renewal = False. Marks = 95 -> above = 20 (> 15)
        # income_level == "low" -> rate = 100 + 40 + 20 = 160. Award = 20 * 160 = 3200
        assert award_amount("merit", 95, "low", False) == 3200

    # 2. Tests for is_eligible
    def test_is_eligible_special_quota_allowed(self):
        # Special quota with backlogs <= 2
        assert is_eligible(60, 2, True) is True

    def test_is_eligible_special_quota_exceeded(self):
        # Special quota with backlogs > 2
        assert is_eligible(90, 3, True) is False

    def test_is_eligible_regular_low_attendance(self):
        # Regular quota with attendance < 75
        assert is_eligible(70, 0, False) is False

    def test_is_eligible_regular_sufficient_attendance_and_backlogs(self):
        # Regular quota with attendance >= 75 and backlogs <= 1
        assert is_eligible(80, 1, False) is True
        assert is_eligible(80, 2, False) is False

    # 3. Tests for application_status
    def test_application_status_renewal_paper_open(self):
        # is_renewal: cutoff = 30; is_paper: cutoff += 10 = 40. days_left = 40 >= 40 -> open
        assert application_status(40, True, True) == "open"

    def test_application_status_regular_electronic_closing(self):
        # is_renewal: False -> cutoff = 20; is_paper: False -> cutoff = 20.
        # days_left = 10 >= 20 - 15 (5) -> closing
        assert application_status(10, False, False) == "closing"

    def test_application_status_regular_electronic_closed(self):
        # is_renewal: False -> cutoff = 20; is_paper: False -> cutoff = 20.
        # days_left = 4 < 5 -> closed
        assert application_status(4, False, False) == "closed"
