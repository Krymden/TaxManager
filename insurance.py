#-*- coding: utf-8 -*-
class NationalPension:
    # Parameters in 2020
    premium = 16410 * 12

    def pay(self):
        return self.premium


class NationalHealthInsurance:
    ### 本当は健康保険は年度計算
    # Local Parameters in Sendai city
    deduction_base = 330000
    # medical part
    medical_rate = 7.47
    medical_offset_person = 23990
    medical_offset_family = 25150
    medical_limit = 610000
    # support part
    support_rate = 2.63
    support_offset_person = 8270
    support_offset_family = 8670
    support_limit = 190000
    # care part
    care_rate = 2.46
    care_offset_person = 9150
    care_offset_family = 7020
    care_limit = 160000

    def __init__(self, income, age):
        self.income = income
        self.age = age
        self.deducted_income = income - self.deduction_base

    def calc(self, rate, offset_p, offset_f, limit, num=1):
        income = self.deducted_income
        premium = ((income * rate) // 100) + (offset_p * num) + offset_f
        return min(premium, limit)

    def pay(self):
        premium = 0
        premium += self.calc(self.medical_rate, self.medical_offset_person,
                             self.medical_offset_family, self.medical_limit)
        premium += self.calc(self.support_rate, self.support_offset_person,
                             self.support_offset_family, self.support_limit)
        if 40 <= self.age < 65:
            premium += self.calc(self.care_rate, self.care_offset_person,
                                 self.care_offset_family, self.care_limit)
        self.premium = int(premium)
        return self.premium
