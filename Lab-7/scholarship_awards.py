import math

def parse_applicant(text):
    """
    Parses an applicant string in the format 'category:marks'.
    Hardened against invalid types, malformed delimiters, non-numeric marks,
    negative values, and special float representations (NaN, inf).
    Returns (category.title(), float(marks)) or None if invalid.
    """
    if text is None or not isinstance(text, str):
        return None
    if text.count(':') != 1:
        return None
    parts = text.split(':')
    category_raw, marks_raw = parts[0].strip(), parts[1].strip()
    if not category_raw:
        return None
    try:
        marks = float(marks_raw)
        if math.isnan(marks) or math.isinf(marks) or marks < 0:
            return None
        return category_raw.title(), marks
    except (ValueError, TypeError):
        return None

def marks_average(marks_csv):
    """
    Parses a comma-separated list of integer marks and computes the integer average.
    Hardened against None, empty strings, non-integers, whitespace, empty tokens,
    negative values, and division-by-zero.
    Returns integer average or None if invalid.
    """
    if marks_csv is None or not isinstance(marks_csv, str):
        return None
    parts = marks_csv.split(',')
    if not parts or parts == ['']:
        return None
    values = []
    for r in parts:
        item = r.strip()
        if not item:
            return None
        try:
            val = int(item)
            if val < 0:
                return None
            values.append(val)
        except (ValueError, TypeError):
            return None
    if not values:
        return None
    return sum(values) // len(values)

def payable_award(text):
    """
    Parses 'award|deduction' string and computes payable award:
    total = award * 1.18 - deduction, bounded at >= 0.
    Hardened against None, invalid delimiters, non-numeric values, NaN, inf,
    and negative values.
    Returns float payable award rounded to 2 decimals, or None if invalid.
    """
    if text is None or not isinstance(text, str):
        return None
    if text.count('|') != 1:
        return None
    parts = text.split('|')
    try:
        award = float(parts[0].strip())
        deduction = float(parts[1].strip())
        if math.isnan(award) or math.isinf(award) or math.isnan(deduction) or math.isinf(deduction):
            return None
        if award < 0 or deduction < 0:
            return None
        total = award * 1.18 - deduction
        return max(round(total, 2), 0.0)
    except (ValueError, TypeError):
        return None

def main():
    print("==== Running parse_applicant ====")
    user_input = input("Enter category:marks (e.g. merit:82): ")
    result = parse_applicant(user_input)
    print("Category and Marks:", result)

    print("\n==== Running marks_average ====")
    user_input = input("Enter marks as CSV (e.g. 72,85,90): ")
    result = marks_average(user_input)
    print("Average Marks:", result)

    print("\n==== Running payable_award ====")
    user_input = input("Enter award|deduction (e.g. 5000|500): ")
    result = payable_award(user_input)
    print("Payable Award:", result)

if __name__ == "__main__":
    main()
