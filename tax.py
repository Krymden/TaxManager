#-*- coding: utf-8 -*-
from income import Salary


class IncomeTax:
    # Parameters in Japan
    deduction_base = 380000
    deduction_student = 270000
    deduction = {"基礎控除":deduction_base}
    special_rate_offset = 2.1 #復興特別所得税

    def __init__(self, income, student=True, insurance=0):
        self.income = income
        self.student = student
        self.insurance = insurance
        self.deducted_income = self.target_income()

    def target_income(self):
        income = self.income
        if self.student and income <= 650000:
            self.deduction["勤労学生控除"] = self.deduction_student
        if self.insurance > 0:
            self.deduction["社会保険料控除"] = self.insurance

        self.deduction_sum = 0
        for key, value in self.deduction.items():
            self.deduction_sum += value
        return max(income-self.deduction_sum, 0)

    def pay(self):
        income = self.deducted_income
        if income <= 1950000:
            rate = 5
            tax_deduction = 0
        elif 1950000 < income <= 3300000:
            rate = 10
            tax_deduction = 97500
        elif 3300000 < income <= 6950000:
            rate = 20
            tax_deduction = 427500
        elif 6950000 < income <= 9000000:
            rate = 23
            tax_deduction = 636000
        elif 9000000 < income <= 18000000:
            rate = 33
            tax_deduction = 1536000
        elif 18000000 < income <= 40000000:
            rate = 40
            tax_deduction = 2796000
        else:
            rate = 45
            tax_deduction = 4796000
        total_rate = (rate * (100 + self.special_rate_offset)) // 100
        self.rate = rate
        self.total_rate = total_rate
        self.tax_deduction = tax_deduction
        self.tax = int((income * total_rate) // 100 - tax_deduction)
        return self.tax


class ResidentTax(IncomeTax):
    # Local Parameters in Sendai city
    res_offset = 6200
    res_rate = 10
    # Deductions
    deduction_base_res = 330000
    deduction_student_res = 260000
    deduction = {"基礎控除":deduction_base_res}

    def target_income(self):
        income = self.income
        if self.student and income <= 650000:
            self.deduction["勤労学生控除"] = self.deduction_student_res
        if self.insurance > 0:
            self.deduction["社会保険料控除"] = self.insurance

        self.deduction_sum = 0
        for key, value in self.deduction.items():
            self.deduction_sum += value
        return max(income-self.deduction_sum, 0)

    def pay(self):
        income = self.deducted_income
        if income > 0:
            personal_diff = self.diff_deduction()
            if income <= 2000000:
                tax_deduction = (min(personal_diff, income) * 5) // 100
            else:
                tax_deduction = (max(personal_diff-(income-2000000), 50000) * 5) // 100
            rate = self.res_rate
            offset = self.res_offset
            self.tax_deduction = tax_deduction
            self.tax = int((income * rate) // 100 + offset - tax_deduction)
        else:
            self.tax_deduction = 0
            self.tax = 0
        return self.tax

    def diff_deduction(self):
        personal = {"基礎控除":self.deduction_base-self.deduction_base_res,
                "勤労学生控除":self.deduction_student-self.deduction_student_res}
        diff = 0
        for key in self.deduction.keys():
            if key in personal:
                diff += personal[key]
        return diff
