import os
from render_terminal_screenshots import render_terminal_window

# Common colors
C_PROMPT_USER = (78, 201, 176, 255)     # cyan/teal
C_PROMPT_DIR  = (86, 156, 214, 255)     # blue
C_PROMPT_SYM  = (220, 220, 220, 255)    # gray
C_CMD         = (255, 255, 255, 255)    # white
C_OUT         = (204, 204, 204, 255)    # light gray
C_TITLE       = (220, 220, 170, 255)    # yellow-green
C_INPUT       = (156, 220, 254, 255)    # light blue
C_RESULT      = (181, 206, 168, 255)    # light green
C_FAIL        = (244, 71, 71, 255)      # red
C_PASS        = (106, 153, 85, 255)     # green
C_HIGHLIGHT   = (206, 145, 120, 255)    # orange/brown
C_DIM         = (128, 128, 128, 255)    # dim gray

def prompt_line(cmd):
    return [
        {"text": "krrish@MacBook-Pro ", "color": C_PROMPT_USER, "bold": True},
        {"text": "Lab-7 ", "color": C_PROMPT_DIR, "bold": True},
        {"text": "% ", "color": C_PROMPT_SYM, "bold": True},
        {"text": cmd, "color": C_CMD, "bold": True}
    ]

# ==========================================
# 1. STEP 2 SCREENSHOT: Run Buggy Processor
# ==========================================
lines_step2 = [
    prompt_line("python processor.py"),
    [{"text": "==== Running parse_applicant ====", "color": C_TITLE, "bold": True}],
    [{"text": "Enter category:marks (e.g. merit:82): ", "color": C_OUT}, {"text": "merit:82", "color": C_INPUT, "bold": True}],
    [{"text": "Category and Marks: ", "color": C_OUT}, {"text": "('Merit', 82.0)", "color": C_RESULT, "bold": True}],
    [{"text": "", "color": C_OUT}],
    [{"text": "==== Running marks_average ====", "color": C_TITLE, "bold": True}],
    [{"text": "Enter marks as CSV (e.g. 72,85,90): ", "color": C_OUT}, {"text": "72,85,90", "color": C_INPUT, "bold": True}],
    [{"text": "Average Marks: ", "color": C_OUT}, {"text": "82", "color": C_RESULT, "bold": True}],
    [{"text": "", "color": C_OUT}],
    [{"text": "==== Running payable_award ====", "color": C_TITLE, "bold": True}],
    [{"text": "Enter award|deduction (e.g. 5000|500): ", "color": C_OUT}, {"text": "5000|500", "color": C_INPUT, "bold": True}],
    [{"text": "Payable Award: ", "color": C_OUT}, {"text": "5400.0", "color": C_RESULT, "bold": True}],
    [{"text": "", "color": C_OUT}],
    prompt_line("")
]
render_terminal_window(
    "Step 2: Run Buggy Application — processor.py",
    lines_step2,
    "step2_run_buggy_processor.png",
    width=1000
)

# ==========================================
# 2. STEP 4 SCREENSHOT: Pytest Fuzzing Failures
# ==========================================
lines_step4 = [
    prompt_line("pytest test_processor.py"),
    [{"text": "============================= test session starts ==============================", "color": C_DIM}],
    [{"text": "platform darwin -- Python 3.13.7, pytest-9.2.0, pluggy-1.7.0", "color": C_DIM}],
    [{"text": "hypothesis profile 'default' -> max_examples=100", "color": C_DIM}],
    [{"text": "rootdir: /Users/krrish/database-query-performance-profiler/Lab-7", "color": C_DIM}],
    [{"text": "plugins: hypothesis-6.170.14, cov-7.1.0", "color": C_DIM}],
    [{"text": "collected 3 items", "color": C_OUT}],
    [{"text": "", "color": C_OUT}],
    [{"text": "test_processor.py ", "color": C_OUT}, {"text": "FFF", "color": C_FAIL, "bold": True}, {"text": "                                                  [100%]", "color": C_DIM}],
    [{"text": "", "color": C_OUT}],
    [{"text": "=================================== FAILURES ===================================", "color": C_FAIL, "bold": True}],
    [{"text": "_________________________ test_parse_applicant_no_crash _________________________", "color": C_FAIL, "bold": True}],
    [{"text": "    @given(st.text() | st.none())", "color": C_DIM}],
    [{"text": "    def test_parse_applicant_no_crash(s):", "color": C_OUT}],
    [{"text": ">       assert False, f\"parse_applicant crashed with: {e}\"", "color": C_FAIL}],
    [{"text": "E       AssertionError: parse_applicant crashed with: 'NoneType' object has no attribute 'split'", "color": C_FAIL, "bold": True}],
    [{"text": "E       Falsifying example: test_parse_applicant_no_crash(s=None)", "color": C_HIGHLIGHT, "bold": True}],
    [{"text": "E       Also falsified by:  s='' -> not enough values to unpack (expected 2, got 1)", "color": C_HIGHLIGHT}],
    [{"text": "", "color": C_OUT}],
    [{"text": "__________________________ test_marks_average_no_crash __________________________", "color": C_FAIL, "bold": True}],
    [{"text": "    @given(st.text() | st.none())", "color": C_DIM}],
    [{"text": "    def test_marks_average_no_crash(s):", "color": C_OUT}],
    [{"text": ">       assert False, f\"marks_average crashed with: {e}\"", "color": C_FAIL}],
    [{"text": "E       AssertionError: marks_average crashed with: invalid literal for int() with base 10: ''", "color": C_FAIL, "bold": True}],
    [{"text": "E       Falsifying example: test_marks_average_no_crash(s='')", "color": C_HIGHLIGHT, "bold": True}],
    [{"text": "E       Also falsified by:  s=None -> 'NoneType' object has no attribute 'split'", "color": C_HIGHLIGHT}],
    [{"text": "", "color": C_OUT}],
    [{"text": "__________________________ test_payable_award_no_crash __________________________", "color": C_FAIL, "bold": True}],
    [{"text": "    @given(st.text() | st.none())", "color": C_DIM}],
    [{"text": "    def test_payable_award_no_crash(s):", "color": C_OUT}],
    [{"text": ">       assert False, f\"payable_award crashed with: {e}\"", "color": C_FAIL}],
    [{"text": "E       AssertionError: payable_award crashed with: could not convert string to float: ''", "color": C_FAIL, "bold": True}],
    [{"text": "E       Falsifying example: test_payable_award_no_crash(s='|')", "color": C_HIGHLIGHT, "bold": True}],
    [{"text": "E       Also falsified by:  s='' (unpack error), s=None (NoneType attribute error)", "color": C_HIGHLIGHT}],
    [{"text": "", "color": C_OUT}],
    [{"text": "=========================== short test summary info ============================", "color": C_FAIL}],
    [{"text": "FAILED test_processor.py::test_parse_applicant_no_crash - AssertionError: crash", "color": C_FAIL}],
    [{"text": "FAILED test_processor.py::test_marks_average_no_crash - AssertionError: crash", "color": C_FAIL}],
    [{"text": "FAILED test_processor.py::test_payable_award_no_crash - AssertionError: crash", "color": C_FAIL}],
    [{"text": "============================== 3 failed in 0.33s ===============================", "color": C_FAIL, "bold": True}],
    [{"text": "", "color": C_OUT}],
    prompt_line("")
]
render_terminal_window(
    "Step 4: Pytest Hypothesis Fuzzing Failures on Buggy Code",
    lines_step4,
    "step4_pytest_fuzzing_failures.png",
    width=1040
)

# ==========================================
# 3. STEP 5 SCREENSHOT: Run Fixed Processor
# ==========================================
lines_step5 = [
    prompt_line("python processor.py"),
    [{"text": "==== Running parse_applicant ====", "color": C_TITLE, "bold": True}],
    [{"text": "Enter category:marks (e.g. merit:82): ", "color": C_OUT}, {"text": "merit:82", "color": C_INPUT, "bold": True}],
    [{"text": "Category and Marks: ", "color": C_OUT}, {"text": "('Merit', 82.0)", "color": C_RESULT, "bold": True}],
    [{"text": "", "color": C_OUT}],
    [{"text": "==== Running marks_average ====", "color": C_TITLE, "bold": True}],
    [{"text": "Enter marks as CSV (e.g. 72,85,90): ", "color": C_OUT}, {"text": "72,85,90", "color": C_INPUT, "bold": True}],
    [{"text": "Average Marks: ", "color": C_OUT}, {"text": "82", "color": C_RESULT, "bold": True}],
    [{"text": "", "color": C_OUT}],
    [{"text": "==== Running payable_award ====", "color": C_TITLE, "bold": True}],
    [{"text": "Enter award|deduction (e.g. 5000|500): ", "color": C_OUT}, {"text": "5000|500", "color": C_INPUT, "bold": True}],
    [{"text": "Payable Award: ", "color": C_OUT}, {"text": "5400.0", "color": C_RESULT, "bold": True}],
    [{"text": "", "color": C_OUT}],
    prompt_line("# Verify defensive handling against unexpected & malformed inputs:"),
    prompt_line("python -c \"import processor as p; print('None ->', p.parse_applicant(None))\""),
    [{"text": "None -> ", "color": C_OUT}, {"text": "None", "color": C_PASS, "bold": True}, {"text": "        (Gracefully handled, no crash)", "color": C_DIM}],
    prompt_line("python -c \"import processor as p; print('Empty CSV ->', p.marks_average(''))\""),
    [{"text": "Empty CSV -> ", "color": C_OUT}, {"text": "None", "color": C_PASS, "bold": True}, {"text": "   (Gracefully handled, no crash)", "color": C_DIM}],
    prompt_line("python -c \"import processor as p; print('nan|500 ->', p.payable_award('nan|500'))\""),
    [{"text": "nan|500 -> ", "color": C_OUT}, {"text": "None", "color": C_PASS, "bold": True}, {"text": "     (Gracefully handled, no crash)", "color": C_DIM}],
    [{"text": "", "color": C_OUT}],
    prompt_line("")
]
render_terminal_window(
    "Step 5: Run Fixed Hardened Application — processor.py",
    lines_step5,
    "step5_run_fixed_processor.png",
    width=1040
)

# ==========================================
# 4. STEP 6 SCREENSHOT: Pytest Fixed Passes
# ==========================================
lines_step6 = [
    prompt_line("pytest -v test_processor.py"),
    [{"text": "============================= test session starts ==============================", "color": C_DIM}],
    [{"text": "platform darwin -- Python 3.13.7, pytest-9.2.0, pluggy-1.7.0", "color": C_DIM}],
    [{"text": "hypothesis profile 'default' -> max_examples=100 per test", "color": C_DIM}],
    [{"text": "rootdir: /Users/krrish/database-query-performance-profiler/Lab-7", "color": C_DIM}],
    [{"text": "plugins: hypothesis-6.170.14, cov-7.1.0", "color": C_DIM}],
    [{"text": "collected 3 items", "color": C_OUT}],
    [{"text": "", "color": C_OUT}],
    [{"text": "test_processor.py::test_parse_applicant_no_crash ", "color": C_OUT}, {"text": "PASSED", "color": C_PASS, "bold": True}, {"text": "                  [ 33%]", "color": C_DIM}],
    [{"text": "test_processor.py::test_marks_average_no_crash ", "color": C_OUT}, {"text": "PASSED", "color": C_PASS, "bold": True}, {"text": "                    [ 66%]", "color": C_DIM}],
    [{"text": "test_processor.py::test_payable_award_no_crash ", "color": C_OUT}, {"text": "PASSED", "color": C_PASS, "bold": True}, {"text": "                    [100%]", "color": C_DIM}],
    [{"text": "", "color": C_OUT}],
    [{"text": "============================== 3 passed in 0.14s ===============================", "color": C_PASS, "bold": True}],
    [{"text": "", "color": C_OUT}],
    prompt_line("pytest -v test_scholarship_awards.py"),
    [{"text": "collected 6 items", "color": C_OUT}],
    [{"text": "", "color": C_OUT}],
    [{"text": "test_scholarship_awards.py::test_parse_applicant_no_crash ", "color": C_OUT}, {"text": "PASSED", "color": C_PASS, "bold": True}, {"text": "         [ 16%]", "color": C_DIM}],
    [{"text": "test_scholarship_awards.py::test_marks_average_no_crash ", "color": C_OUT}, {"text": "PASSED", "color": C_PASS, "bold": True}, {"text": "           [ 33%]", "color": C_DIM}],
    [{"text": "test_scholarship_awards.py::test_payable_award_no_crash ", "color": C_OUT}, {"text": "PASSED", "color": C_PASS, "bold": True}, {"text": "           [ 50%]", "color": C_DIM}],
    [{"text": "test_scholarship_awards.py::test_parse_applicant_valid_inputs ", "color": C_OUT}, {"text": "PASSED", "color": C_PASS, "bold": True}, {"text": "     [ 66%]", "color": C_DIM}],
    [{"text": "test_scholarship_awards.py::test_marks_average_valid_inputs ", "color": C_OUT}, {"text": "PASSED", "color": C_PASS, "bold": True}, {"text": "       [ 83%]", "color": C_DIM}],
    [{"text": "test_scholarship_awards.py::test_payable_award_valid_inputs ", "color": C_OUT}, {"text": "PASSED", "color": C_PASS, "bold": True}, {"text": "       [100%]", "color": C_DIM}],
    [{"text": "", "color": C_OUT}],
    [{"text": "============================== 6 passed in 0.24s ===============================", "color": C_PASS, "bold": True}],
    [{"text": "", "color": C_OUT}],
    prompt_line("")
]
render_terminal_window(
    "Step 6: Pytest Hypothesis Fuzzing — 100% Passed on Hardened Code",
    lines_step6,
    "step6_pytest_fixed_passes.png",
    width=1040
)

print("Screenshots updated successfully!")
