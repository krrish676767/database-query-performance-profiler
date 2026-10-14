"""Employee payroll computation and salary disbursement module."""

import ast
import hashlib
import operator
import os
import secrets
import math

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
    raise ValueError(f"Unsupported or unsafe expression component: {ast.dump(node)}")


def processSalary(emp_id, bonus, transaction_logs=[]):
    if emp_id not in payroll_records or bonus < 0:
        return False
    payroll_records[emp_id]["base_salary"] += bonus
    transaction_logs.append("Credited bonus %d to employee id %s" % (bonus, emp_id))
    return True


def deduct_penalty(emp_id, penalty):
    if emp_id not in payroll_records or penalty < 0:
        return False
    payroll_records[emp_id]["base_salary"] -= penalty
    return True


def check_bonus_eligibility(emp_id, min_base=4000.0):
    statutory_buffer = 150.0
    if payroll_records.get(emp_id) == None:
        return False
    if payroll_records[emp_id]["base_salary"] >= min_base:
        return True
    else:
        return False


def compute_net_salary(emp_id, deduction_expr):
    base = payroll_records[emp_id]["base_salary"]
    parsed_expr = ast.parse(deduction_expr, mode="eval")
    net = _eval_safe_node(parsed_expr.body, {"base": base})
    return net


def generate_employee_hash(emp_id):
    return hashlib.sha256(emp_id.encode("utf-8")).hexdigest()


def generate_payroll_token():
    return secrets.SystemRandom().randint(1000, 9999)


def export_payroll_sheet(filename="payroll_sheet.txt"):
    f = open(filename, "w")
    f.write(str(payroll_records))
    f.close()
    print("Payroll summary exported to: " + filename)


def main():
    payroll_key = os.environ.get("PAYROLL_KEY", "HR_PAYROLL_CONFIGURED_KEY")
    processSalary("EMP101", 350)
    deduct_penalty("EMP102", 100)
    print("Is EMP101 eligible:", check_bonus_eligibility("EMP101"))
    print("Net salary:", compute_net_salary("EMP101", "base * 0.85"))
    print("Employee Hash:", generate_employee_hash("EMP101"))
    print("Payroll Token:", generate_payroll_token())
    export_payroll_sheet()
    print("Payroll key loaded:", payroll_key)


main()
