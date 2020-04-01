#-*- coding: utf-8 -*-
class Income:
    def __init__(self, sales, expense=0):
        self.sales = sales
        self.expense = expense

    def income(self):
        return self.round_th(self.sales - self.expense)

    def round_th(self, v):
        return (v // 1000) * 1000


class Salary(Income):
    def __init__(self, sales):
        super().__init__(sales=sales)

    def income(self):
        sales = self.sales
        if sales < 651000:
            return 0
        elif 651000 <= sales < 1619000:
            return self.round_th(sales - 650000)
        elif 1619000 <= sales < 1620000:
            return 969000
        elif 1620000 <= sales < 1622000:
            return 970000
        elif 1622000 <= sales < 1624000:
            return 972000
        elif 1624000 <= sales < 1628000:
            return 974000
        elif 1628000 <= sales < 1800000:
            return ((sales / 4) // 1000) * 2400
        elif 1800000 <= sales < 3600000:
            return ((sales / 4) // 1000) * 2800 - 180000
        elif 3600000 <= sales < 6600000:
            return ((sales / 4) // 1000) * 3200 - 540000
        elif 6600000 <= sales < 10000000:
            return self.round_th((sales * 9) // 10 - 1200000)
        else:
            return self.round_th(sales - 2200000)
