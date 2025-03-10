#!/usr/bin/python3

import sys

hkd_to_twd = 3.91
jpy_to_twd = 0.23
jpy_to_hkd = 0.059
jpy_to_usd = 0.0075
million = 1000000.0
mortgage_twd_monthly = "TO_UPDATE"
sep = "=" * 30 + "\n"

## Individual income taxes consist of national income tax and local inhabitant tax.


def deduction(taxable_income_in_million):
    income = taxable_income_in_million
    if income <= 1.625:
        return 0.55
    elif income <= 1.8:
        return income * 0.4 - 0.1
    elif income <= 3.6:
        return income * 0.3 + 0.08
    elif income <= 6.6:
        return income * 0.2 + 0.44
    elif income <= 8.5:
        return income * 0.1 + 1.1
    else:
        return 1.95


def jp_estimate(taxable_income_in_million):
    """
    Calculates the income tax for residents of Tokyo based on the taxable income.
    reference:
    https://taxsummaries.pwc.com/japan/individual/sample-personal-income-tax-calculation
    """

    income = taxable_income_in_million
    employment_deduction = deduction(income)
    other_deduction = 0.0
    taxable_income = income - employment_deduction - other_deduction
    # taxable_income = income
    tax_brackets = [0, 1.95, 3.3, 6.95, 9, 18, 40, 1000]
    tax_rates = [0, 0.05, 0.1, 0.2, 0.23, 0.33, 0.4, 0.45]
    b4_bucket_tax = [0, 0, 0.0975, 0.4275, 0.636, 1.536, 2.796, 4.796]

    bracket = 0
    while taxable_income > tax_brackets[bracket]:
        bracket += 1

    tax = round(tax_rates[bracket] * taxable_income - b4_bucket_tax[bracket], 6)
    surtax = round(tax * 0.021, 6)
    inhabitant_tax = round(0.1 * taxable_income, 6)
    total_tax = round(tax + surtax + inhabitant_tax, 6)
    take_home = round(income - total_tax, 6)
    take_home_twd_monthly = round(take_home * million * jpy_to_twd / 12.0, 0)
    jp_rent_in_twd_monthly = round(0.2 * million * jpy_to_twd, 6)
    free_twd_monthly = take_home_twd_monthly - jp_rent_in_twd_monthly - mortgage_twd_monthly
    free_jpy_monthly = free_twd_monthly / jpy_to_twd
    free_money_jpy_daily = round(free_jpy_monthly / 30.0, 6)
    print(
        sep + f"income={income}M\n" + sep + f"deduction={employment_deduction}M\n"
        f"other_deduction={other_deduction}M\n" + sep + f"taxable_income={taxable_income}M\n"
        f"income_tax={tax}M\n"
        f"surtax={surtax}M\n"
        f"inhabitant_tax={inhabitant_tax}M\n"
        f"total_tax={total_tax}M\n"
        f"tax/income={round(total_tax * 100/ income, 2)}%\n" + sep + f"take_home={take_home}M\n"
        f"take_home (TWD monthly)={take_home_twd_monthly}\n"
        f"jp_rent (TWD monthly)={jp_rent_in_twd_monthly}\n"
        f"tw_mortgage (TWD monthly)={mortgage_twd_monthly}\n" + sep + f"free_money (JPY daily)={free_money_jpy_daily}\n"
        f"free_money (TWD monthly)={free_twd_monthly}\n"
    )
    return round(tax, 6)


def hk_comparison():
    income = 2.2 * million
    take_home = income * 0.83
    take_home_jpy = round(take_home / jpy_to_hkd / million, 6)
    take_home_twd_monthly = round(take_home * hkd_to_twd / 12.0, 0)
    hk_rent_twd_monthly = 22000 * hkd_to_twd
    free_twd_monthly = take_home_twd_monthly - hk_rent_twd_monthly - mortgage_twd_monthly
    free_jpy_monthly = free_twd_monthly / jpy_to_twd
    free_money_jpy_daily = round(free_jpy_monthly / 30.0, 6)
    print(
        f"take_home_hkd={take_home}\n"
        f"take_home_jpy={take_home_jpy}M\n"
        f"take_home (TWD monthly)={take_home_twd_monthly}\n"
        f"hk_rent (TWD monthly)={hk_rent_twd_monthly}\n"
        f"tw_mortgage (TWD monthly)={mortgage_twd_monthly}\n" + sep + f"free_money (JPY daily)={free_money_jpy_daily}\n"
        f"free_money (TWD monthly)={free_twd_monthly}\n"
    )


income = float(sys.argv[1])
jp_estimate(income)
print("-" * 50)
hk_comparison()
