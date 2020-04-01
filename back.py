#-*- coding: utf-8 -*-
from income import Income, Salary
from tax import IncomeTax, ResidentTax
from insurance import NationalPension, NationalHealthInsurance

class Person:
    def __init__(self, age, student=True, pension=False):
        self.age = age
        self.student = student
        self.pension = pension

    def simulate(self, salary, verbose=False):
        income = Salary(sales=salary).income()
        if verbose: print(f"控除前所得: ¥{income}")

        insurance_fee = 0
        if salary >= 1300000:
            insurance = NationalHealthInsurance(income=income, age=self.age)
            insurance_fee += insurance.pay()
            if verbose: print(f"国民健康保険料: ¥{insurance.pay()}")
        if self.pension or (income >= 1180000 + insurance_fee):
            pention = NationalPension().pay()
            insurance_fee += pention
            if verbose: print(f"国民年金保険料: ¥{pention}")
        if verbose: print(f"社会保険料合計額: ¥{insurance_fee}")

        country = IncomeTax(income=income, student=self.student,
                            insurance=insurance_fee)
        resident = ResidentTax(income=income, student=self.student,
                               insurance=insurance_fee)
        country_tax = country.pay()
        resident_tax = resident.pay()
        #print(f"控除後所得税課税所得: ¥{country.deducted_income}")
        if verbose: print(f"所得税: ¥{country_tax}")
        #print(f"控除後住民税課税所得: ¥{country.deducted_income}")
        if verbose: print(f"住民税: ¥{resident_tax}")
        balance = int(salary - insurance_fee - country_tax - resident_tax)
        self.insurance_fee = insurance_fee
        self.country_tax = country_tax
        self.resident_tax = resident_tax
        self.balance = balance
        return balance

    def back_simulate(self, salary, epoch=5, lr=1.0):
        estimated = salary
        while epoch > 0:
            res = self.simulate(estimated)
            delta = salary - res
            estimated += delta * lr
            epoch -= 1
        return estimated


if __name__ == "__main__":
    person = Person(age=20, student=True, pension=False)
    while True:
        print("=" * 25)
        salary = int(input("目標手取り: "))
        res = person.back_simulate(salary=salary)
        print(f"【推定額面: ¥{res}】")
        real = person.simulate(res, verbose=True)
        print(f"手取り: ¥{real}")
        print(f"（誤差: ¥{real - salary}）")
