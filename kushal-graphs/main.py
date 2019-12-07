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
        indexes["index_" + lower_usecase] = usecase + " - Without CPO"
        indexes["index_" + lower_usecase + "_with_cpo"] = usecase + " - With CPO"
        for factor in all_factors:
            if usecase == "PP" and factor == "Notify":
                continue
            indexes["index_" + lower_usecase + "_factor_" + factor.lower()] = usecase + " - " + factor


def fetch_data_from_csv(filename):
    return pandas.read_csv(filename)


def plot_ccdf(without_cpo, with_cpo, title):
    Y1 = [len([x for x in without_cpo if x >= y])/len(without_cpo) for y in range(1,6)]
    Y2 = [len([x for x in with_cpo if x >= y])/len(with_cpo) for y in range(1,6)]
    X = [1, 2, 3, 4, 5]
    pyl.xlabel("User Comfort Rating (5=highest)")
    pyl.ylabel("CCDF - Probability(User's Comfort rating is greater than X)")
    pyl.title(title)
    pyl.xticks([1,2,3,4,5])
    pyl.plot(X, Y1, label="Without CPO", color="red")
    pyl.plot(X, Y2, label="With CPO", color="green")
    for i, j in zip(X, Y1):
        pyl.text(i, j, str(round(j, 2)))
    for i, j in zip(X, Y2):
        pyl.text(i, j, str(round(j, 2)))
    pyl.legend()
    pyl.savefig(title + ".png")
    pyl.show()


def main():
    create_indexes()
    data = fetch_data_from_csv("survey_responses.csv")
    without_cpo = []
    with_cpo = []
    individual_usecase = {}
    for usecase in all_usecases:
        lower_usecase = usecase.lower()
        rows = data[[indexes["index_" + lower_usecase], indexes["index_" + lower_usecase + "_with_cpo"]]]
        rows.rename(columns={indexes["index_" + lower_usecase]: "Without CPO",
                             indexes["index_" + lower_usecase + "_with_cpo"]: "With CPO"}, inplace=True)
        usecase_list = rows["Without CPO"].values.tolist()
        usecase_list_cpo = rows["With CPO"].values.tolist()
        without_cpo += usecase_list
        with_cpo += usecase_list_cpo
        individual_usecase[usecase] = {"Without CPO": usecase_list, "With CPO": usecase_list_cpo}
    print("Printing list without CPO:")
    print(sorted(without_cpo))
    print("Printing list with CPO:")
    print(sorted(with_cpo))
    print("Individual:")
    print(individual_usecase)
    plot_ccdf(without_cpo, with_cpo, "Overall CCDF graph of User Comfort")
    plot_ccdf(individual_usecase["PP"]["Without CPO"], individual_usecase["PP"]["With CPO"],
              "CCDF graph of User Comfort for Predictive Policing")
    plot_ccdf(individual_usecase["SCS"]["Without CPO"], individual_usecase["SCS"]["With CPO"],
              "CCDF graph of User Comfort for Smart Complaint System")
    plot_ccdf(individual_usecase["ST"]["Without CPO"], individual_usecase["ST"]["With CPO"],
              "CCDF graph of User Comfort for Smart Transportation")


if __name__ == '__main__':
    main()
