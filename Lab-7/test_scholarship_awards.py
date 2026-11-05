from hypothesis import given, strategies as st
import math
from scholarship_awards import parse_applicant, marks_average, payable_award

# Property-Based Fuzzing Tests (Required: st.text() | st.none())
@given(st.text() | st.none())
def test_parse_applicant_no_crash(s):
    try:
        parse_applicant(s)
    except Exception as e:
        assert False, f"parse_applicant crashed with: {e}"

@given(st.text() | st.none())
def test_marks_average_no_crash(s):
    try:
        marks_average(s)
    except Exception as e:
        assert False, f"marks_average crashed with: {e}"

@given(st.text() | st.none())
def test_payable_award_no_crash(s):
    try:
        payable_award(s)
    except Exception as e:
        assert False, f"payable_award crashed with: {e}"

# Domain Property Tests: Verifying mathematical properties on valid generated inputs
@given(
    category=st.text(alphabet=st.characters(categories=('Lu', 'Ll')), min_size=1, max_size=25),
    marks=st.floats(min_value=0.0, max_value=100.0, allow_nan=False, allow_infinity=False)
)
def test_parse_applicant_valid_inputs(category, marks):
    input_str = f"{category}:{marks}"
    result = parse_applicant(input_str)
    assert result is not None
    cat, m = result
    assert cat == category.strip().title()
    assert abs(m - marks) < 1e-4

@given(st.lists(st.integers(min_value=0, max_value=100), min_size=1, max_size=50))
def test_marks_average_valid_inputs(marks_list):
    csv_str = ",".join(str(m) for m in marks_list)
    avg = marks_average(csv_str)
    expected = sum(marks_list) // len(marks_list)
    assert avg == expected

@given(
    award=st.floats(min_value=0.0, max_value=1000000.0, allow_nan=False, allow_infinity=False),
    deduction=st.floats(min_value=0.0, max_value=1000000.0, allow_nan=False, allow_infinity=False)
)
def test_payable_award_valid_inputs(award, deduction):
    input_str = f"{award}|{deduction}"
    res = payable_award(input_str)
    expected = max(round(float(award) * 1.18 - float(deduction), 2), 0.0)
    assert res is not None
    assert abs(res - expected) < 1e-2
    assert res >= 0.0
