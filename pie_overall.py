import pandas as pd
import matplotlib.pyplot as plt
import csv


def classifyUser(i, data, usecase):
    sig_incr_thresh = 3  # threshold for significant increase
    col_w_cpo = usecase + "_with_cpo"
    col_wo_cpo = usecase + "_without_cpo"
    confidenceDiff = data.loc[i, col_w_cpo] - data.loc[i, col_wo_cpo]

    # segmentation criterion
    if confidenceDiff == 0:
        return "NoChange"
    elif confidenceDiff < 0:
        return "Decrease"
    elif data.loc[i, col_wo_cpo] <= sig_incr_thresh and data.loc[i, col_w_cpo] > sig_incr_thresh:
        return "SignificantIncrease"
    else:
        return "InsignificantIncrease"


def plotPieChart(segments):
    labels = [r'Significant Increase', r'Marginal Increase',
              r'No Change', r'Decrease']
    colors = ['yellowgreen', 'gold', 'lightskyblue', 'lightcoral']
    explode = (0.1, 0, 0, 0)
    plt.pie(segments, colors=colors, labels=labels, explode=explode, autopct='%1.1f%%', startangle=90)
    # Set aspect ratio to be equal so that pie is drawn as a circle.
    plt.axis('equal')
    plt.title("Change in Privacy Confidence due to CPO appointment",fontweight='bold')
    plt.show()


if __name__ == '__main__':
    data = pd.read_csv('data/survey_responses.csv')
    usecases = ['pp', 'scs', 'st']

    # data cleaning
    data.columns = data.columns.str.strip().str.lower().str.replace(' ', '_').str.replace('(', '').str.replace(')', '')

    numSignificantIncrease = 0
    numInsignificantIncrease = 0
    numNoChange = 0
    numDecrease = 0

    # segment users
    for i in range(len(data)):
        for usecase in usecases:
            segment = classifyUser(i, data, usecase)
            if (segment == "SignificantIncrease"):
                numSignificantIncrease += 1
            elif (segment == "InsignificantIncrease"):
                numInsignificantIncrease += 1
            elif (segment == "NoChange"):
                numNoChange += 1
            else:
                numDecrease += 1

    segments = [numSignificantIncrease, numInsignificantIncrease, numNoChange, numDecrease]
    plotPieChart(segments)
