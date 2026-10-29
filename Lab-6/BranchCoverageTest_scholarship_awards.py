import pytest
from scholarship_awards import award_amount, is_eligible, application_status


class TestScholarshipAwardsBranchCoverage:
    """Test suite designed to achieve 100% branch coverage for scholarship_awards.py,

    covering all decision branches, truth combinations, and boundary conditions.
    """

    # =========================================================================
    # Branch Tests for: award_amount(category, marks, income_level, is_renewal)
    # =========================================================================

    def test_award_amount_category_validation(self):
        # Branch: if category not in CUTOFF_MARKS -> True (raise ValueError)
        with pytest.raises(ValueError, match="unknown category"):
            award_amount("music", 85, "low", False)

        # Branch: if category not in CUTOFF_MARKS -> False (valid category)
        # We verify valid categories work
        assert award_amount("merit", 70, "low", False) == 0

    def test_award_amount_marks_validation(self):
        # Branch: if marks < 0 -> True (raise ValueError)
        with pytest.raises(ValueError, match="invalid marks"):
            award_amount("merit", -1, "low", False)

        # Boundary: marks == 0 -> False (does not raise)
        assert award_amount("merit", 0, "low", False) == 0

    def test_award_amount_renewal_and_sports_branch_combinations(self):
        # Branch condition: if is_renewal and category != "sports":
        # Case 1: (is_renewal=True, category != "sports" [True]) -> cutoff reduced by 5
        # merit cutoff: 75 -> 70. marks=76 -> above=6 <= 15. low income -> rate=100.
        assert award_amount("merit", 76, "low", True) == 6 * 100

        # Case 2: (is_renewal=True, category == "sports" [False]) -> cutoff unchanged (60)
        # marks=66 -> above=6 <= 15. low income -> rate=100.
        assert award_amount("sports", 66, "low", True) == 6 * 100

        # Case 3: (is_renewal=False, category != "sports" [True]) -> cutoff unchanged (65 for arts)
        # marks=71 -> above=6 <= 15. low income -> rate=100.
        assert award_amount("arts", 71, "low", False) == 6 * 100

        # Case 4: (is_renewal=False, category == "sports" [False]) -> cutoff unchanged (60)
        assert award_amount("sports", 66, "low", False) == 6 * 100

    def test_award_amount_above_cutoff_branch(self):
        # Branch: if above <= 0 -> True (marks <= cutoff)
        # merit cutoff=75: marks=75 (above=0) -> returns 0
        assert award_amount("merit", 75, "low", False) == 0
        # marks=74 (above=-1) -> returns 0
        assert award_amount("merit", 74, "low", False) == 0

        # Branch: if above <= 0 -> False (marks > cutoff)
        assert award_amount("merit", 76, "low", False) == 1 * 100

    def test_award_amount_income_level_and_bonus_combinations(self):
        # Branch 1: above <= 15, income_level == "low"
        # arts cutoff=65, marks=75 (above=10 <= 15). rate = 100. award = 1000
        assert award_amount("arts", 75, "low", False) == 1000

        # Branch 2: above <= 15, income_level != "low"
        # arts cutoff=65, marks=75 (above=10 <= 15). rate = 60. award = 600
        assert award_amount("arts", 75, "high", False) == 600

        # Branch 3: above > 15, income_level == "low"
        # arts cutoff=65, marks=85 (above=20 > 15). rate = 100 + 40 + 20 = 160. award = 3200
        assert award_amount("arts", 85, "low", False) == 3200

        # Branch 4: above > 15, income_level != "low"
        # arts cutoff=65, marks=85 (above=20 > 15). rate = 60 + 40 = 100. award = 2000
        assert award_amount("arts", 85, "medium", False) == 2000

    # =========================================================================
    # Branch Tests for: is_eligible(attendance, backlogs, is_special_quota)
    # =========================================================================

    def test_is_eligible_special_quota_branches(self):
        # Branch: if is_special_quota -> True
        # Sub-branch: backlogs <= 2 -> True (backlogs=0, 1, 2)
        assert is_eligible(50, 0, True) is True
        assert is_eligible(50, 2, True) is True

        # Sub-branch: backlogs <= 2 -> False (backlogs=3)
        assert is_eligible(95, 3, True) is False

    def test_is_eligible_regular_quota_branches(self):
        # Branch: if is_special_quota -> False
        # Branch: if attendance < 75 -> True (low attendance fails immediately)
        assert is_eligible(74, 0, False) is False

        # Branch: if attendance < 75 -> False (sufficient attendance: boundary 75)
        # Sub-branch: backlogs <= 1 -> True (backlogs=0, 1)
        assert is_eligible(75, 1, False) is True
        assert is_eligible(85, 0, False) is True

        # Sub-branch: backlogs <= 1 -> False (backlogs=2)
        assert is_eligible(75, 2, False) is False

    # =========================================================================
    # Branch Tests for: application_status(days_left, is_renewal, is_paper)
    # =========================================================================

    def test_application_status_renewal_and_paper_cutoffs(self):
        # Branch: is_renewal -> True (base=30), is_paper -> True (cutoff=40)
        # days_left >= cutoff (40 >= 40) -> "open"
        assert application_status(40, True, True) == "open"
        assert application_status(45, True, True) == "open"

        # days_left >= cutoff - 15 (40 - 15 = 25). Boundary tests:
        assert application_status(39, True, True) == "closing"
        assert application_status(25, True, True) == "closing"

        # days_left < cutoff - 15 (24 < 25) -> "closed"
        assert application_status(24, True, True) == "closed"

    def test_application_status_regular_electronic_cutoffs(self):
        # Branch: is_renewal -> False (base=20), is_paper -> False (cutoff=20)
        # days_left >= cutoff (20 >= 20) -> "open"
        assert application_status(20, False, False) == "open"

        # days_left >= cutoff - 15 (20 - 15 = 5) -> "closing"
        assert application_status(19, False, False) == "closing"
        assert application_status(5, False, False) == "closing"

        # days_left < cutoff - 15 (4 < 5) -> "closed"
        assert application_status(4, False, False) == "closed"
        assert application_status(0, False, False) == "closed"

    def test_application_status_mixed_modes(self):
        # is_renewal -> True (30), is_paper -> False (cutoff=30)
        assert application_status(30, True, False) == "open"
        assert application_status(20, True, False) == "closing"
        assert application_status(14, True, False) == "closed"

        # is_renewal -> False (20), is_paper -> True (cutoff=30)
        assert application_status(30, False, True) == "open"
        assert application_status(15, False, True) == "closing"
        assert application_status(14, False, True) == "closed"
