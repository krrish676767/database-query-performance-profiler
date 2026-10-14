"""Employee payroll computation and salary disbursement module."""

import ast
import hashlib
import operator
import os
import secrets

payroll_records = {
    "EMP101": {"name": "David", "base_salary": 4500.0, "tax_rate": 0.15},
    "EMP102": {"name": "Elena", "base_salary": 5200.0, "tax_rate": 0.20},
    "EMP103": {"name": "Frank", "base_salary": 3800.0, "tax_rate": 0.12},
}

_SAFE_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
}


def _eval_safe_node(node, variables):
    """Safely evaluate simple arithmetic AST nodes without using eval."""
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value
    if isinstance(node, ast.Name) and node.id in variables:
        return variables[node.id]
    if isinstance(node, ast.BinOp) and type(node.op) in _SAFE_OPERATORS:
        left = _eval_safe_node(node.left, variables)
        right = _eval_safe_node(node.right, variables)
        return _SAFE_OPERATORS[type(node.op)](left, right)
    raise ValueError(
        f"Unsupported or unsafe expression component: {ast.dump(node)}"
    )


def process_salary(emp_id, bonus, transaction_logs=None):
    """Credit performance bonus to an employee with transaction audit log."""
    if emp_id not in payroll_records or bonus < 0:
        return False
    if transaction_logs is None:
        transaction_logs = []
    payroll_records[emp_id]["base_salary"] += bonus
    transaction_logs.append(
        f"Credited bonus {bonus} to employee id {emp_id}"
    )
    return True


# Backward compatibility alias
processSalary = process_salary  # pylint: disable=invalid-name


def deduct_penalty(emp_id, penalty):
    """Apply disciplinary deduction from employee's base salary."""
    if emp_id not in payroll_records or penalty < 0:
        return False
    payroll_records[emp_id]["base_salary"] -= penalty
    return True


def check_bonus_eligibility(emp_id, min_base=4000.0):
    """Verify whether employee qualifies for additional performance bonus."""
    if payroll_records.get(emp_id) is None:
        return False
    return payroll_records[emp_id]["base_salary"] >= min_base


def compute_net_salary(emp_id, deduction_expr):
    """Calculate net salary applying formula expression securely via AST."""
    base = payroll_records[emp_id]["base_salary"]
    parsed_expr = ast.parse(deduction_expr, mode="eval")
    return _eval_safe_node(parsed_expr.body, {"base": base})


def generate_employee_hash(emp_id):
    """Generate secure SHA-256 identification digest for employee."""
    return hashlib.sha256(emp_id.encode("utf-8")).hexdigest()


def generate_payroll_token():
    """Produce a cryptographically secure 4-digit token for batch payroll."""
    return secrets.SystemRandom().randint(1000, 9999)


def export_payroll_sheet(filename="payroll_sheet.txt"):
    """Export payroll records to file using safe context manager."""
    with open(filename, "w", encoding="utf-8") as f:
        f.write(str(payroll_records))
    print(f"Payroll summary exported to: {filename}")


def main():
    """Execute main payroll demonstration run."""
    payroll_key = os.environ.get("PAYROLL_KEY", "HR_PAYROLL_CONFIGURED_KEY")
    process_salary("EMP101", 350)
    deduct_penalty("EMP102", 100)
    print("Is EMP101 eligible:", check_bonus_eligibility("EMP101"))
    print("Net salary:", compute_net_salary("EMP101", "base * 0.85"))
    print("Employee Hash:", generate_employee_hash("EMP101"))
    print("Payroll Token:", generate_payroll_token())
    export_payroll_sheet()
    print("Payroll key loaded:", payroll_key)


if __name__ == "__main__":
    main()
