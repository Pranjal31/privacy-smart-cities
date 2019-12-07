from pprint import pprint
import pylab as pyl
import numpy as np

import pandas

data = {}
indexes = {}
all_usecases = ["PP", "SCS", "ST"]
all_factors = ["LP", "Notify", "Anon", "Publish", "Custom"]


def create_indexes():
    # index_pp, index_pp_without_cpo, index_pp_factor_lp
    for usecase in all_usecases:
        lower_usecase = usecase.lower()
        indexes["index_" + lower_usecase] = usecase + " Without CPO"
        indexes["index_" + lower_usecase + "_with_cpo"] = usecase + " With CPO"
        for factor in all_factors:
            if usecase == "PP" and factor == "Notify":
                continue
            indexes["index_" + lower_usecase + "_factor_" + factor.lower()] = usecase + " " + factor


def fetch_data_from_csv(filename):
    return pandas.read_csv(filename)


def plot_ccdf(list_tuples, title, xlabel = None, ylabel = None):
    X = [1, 2, 3, 4, 5]
    if not xlabel:
        pyl.xlabel("User Comfort Rating (5=highest)")
    else:
        pyl.xlabel(xlabel)
    if not ylabel:
        pyl.ylabel("Modified CCDF - Probability(User's Comfort rating is greater than or equal to X)")
    else:
        pyl.ylabel(ylabel)
    pyl.title(title)
    pyl.xticks([1,2,3,4,5])
    for _label, y_item in list_tuples:
        Y = [len([x for x in y_item if x >= y])/len(y_item) for y in range(1,6)]
        pyl.plot(X, Y, label=_label)
        for i, j in zip(X, Y):
            pyl.text(i, j, str(round(j, 2)))
    pyl.legend()
    # pyl.savefig(title + ".png")
    pyl.show()


def main():
    create_indexes()
    data = fetch_data_from_csv("data/survey_responses.csv")
    without_cpo = []
    with_cpo = []
    individual_usecase = {}
    factors = {}
    for usecase in all_usecases:
        lower_usecase = usecase.lower()
        usecase_list = data[indexes["index_" + lower_usecase]].values.tolist()
        usecase_list_cpo = data[indexes["index_" + lower_usecase + "_with_cpo"]].values.tolist()
        without_cpo += usecase_list
        with_cpo += usecase_list_cpo
        individual_usecase[usecase] = {"Without CPO": usecase_list, "With CPO": usecase_list_cpo}
        factor_list = {}
        for factor in all_factors:
            if usecase == "PP" and factor == "Notify":
                continue
            factor_list[factor] = data[indexes["index_" + lower_usecase + "_factor_" + factor.lower()]].dropna().values.tolist()
        factors[usecase] = factor_list
    print("Printing list without CPO:")
    print(sorted(without_cpo))
    print("Printing list with CPO:")
    print(sorted(with_cpo))
    print("Individual:")
    print(individual_usecase)
    print(factors)
    plot_ccdf([("Without CPO", without_cpo), ("With CPO", with_cpo)],
              "Overall CCDF (Modified) graph of User Comfort")
    plot_ccdf([("Without CPO", individual_usecase["PP"]["Without CPO"]),
               ("With CPO", individual_usecase["PP"]["With CPO"])],
              "CCDF (Modified) graph of User Comfort for Predictive Policing")
    plot_ccdf([("Without CPO", individual_usecase["SCS"]["Without CPO"]), ("With CPO", individual_usecase["SCS"]["With CPO"])],
              "CCDF (Modified) graph of User Comfort for Smart Complaint System")
    plot_ccdf([("Without CPO", individual_usecase["ST"]["Without CPO"]), ("With CPO", individual_usecase["ST"]["With CPO"])],
              "CCDF (Modified) graph of User Comfort for Smart Transportation")

    plot_ccdf([("Enforce Laws and Policies", factors["PP"]["LP"]),
                    ("Anonymize Data", factors["PP"]["Anon"]),
                    ("Publish Technical Details", factors["PP"]["Publish"])],
              "CCDF (Modified) graph of Impact for Factors for Predictive Policing",
              "Rating of Impact of Factor",
              "Modified CCDF - Probability(Impact of factor is greater than or equal to X)")
    plot_ccdf([("Enforce Laws and Policies", factors["SCS"]["LP"]),
                    ("Notify about Data Collection", factors["SCS"]["Notify"]),
                    ("Anonymize Data", factors["SCS"]["Anon"]),
                    ("Publish Technical Details", factors["SCS"]["Publish"])],
              "CCDF (Modified) graph of Impact for Factors for Smart Complaint System",
              "Rating of Impact of Factor",
              "Modified CCDF - Probability(Impact of factor is greater than or equal to X)")
    plot_ccdf([("Enforce Laws and Policies", factors["ST"]["LP"]),
                    ("Notify about Data Collection", factors["ST"]["Notify"]),
                    ("Anonymize Data", factors["ST"]["Anon"]),
                    ("Publish Technical Details", factors["ST"]["Publish"])],
              "CCDF (Modified) graph of Impact for Factors for Smart Transportation",
              "Rating of Impact of Factor",
              "Modified CCDF - Probability(Impact of factor is greater than or equal to X)")


if __name__ == '__main__':
    main()
