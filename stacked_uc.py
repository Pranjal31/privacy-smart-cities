import pandas as pd
import matplotlib.pyplot as plt
import csv
import numpy as np
import sys

def plotPercentStackedBarPlots(segmentList, usecase):
    n = len(segmentList)
    r = range(n)
    if usecase == "pp":
        names = ('Laws & Policies','Anonymize Data', 'Publish Tech. Details')
        raw_data = {'blueBars': [segmentList[0][0], segmentList[1][0], segmentList[2][0]], 'greenBars': [segmentList[0][1], segmentList[1][1],segmentList[2][1]],'orangeBars': [segmentList[0][2], segmentList[1][2], segmentList[2][2]]}
    else:
        names = ('Laws & Policies','Anonymize Data', 'Publish Tech. Details', 'Notify Data Collection')
        raw_data = {'blueBars': [segmentList[0][0], segmentList[1][0], segmentList[2][0], segmentList[3][0]], 'greenBars': [segmentList[0][1], segmentList[1][1],segmentList[2][1], segmentList[3][1]],'orangeBars': [segmentList[0][2], segmentList[1][2], segmentList[2][2], segmentList[3][2]]}

    df = pd.DataFrame(raw_data)
    # From raw value to percentage
    totals = [i+j+k for i,j,k in zip(df['orangeBars'], df['greenBars'], df['blueBars'])]
    orangeBars = [i * 100.0 / j for i,j in zip(df['orangeBars'], totals)]
    greenBars = [i * 100.0 / j for i,j in zip(df['greenBars'], totals)]
    blueBars = [i * 100.0 / j for i,j in zip(df['blueBars'], totals)]

    # plot
    barWidth = 0.65
    # Create green Bars
    plt.bar(r, greenBars, color='yellowgreen', edgecolor='white', width=barWidth, label='Helpful')
    # Create orange Bars
    plt.bar(r, orangeBars, bottom=greenBars, color='lightcoral', edgecolor='white', width=barWidth, label='Not Helpful')
    # Create blue Bars
    plt.bar(r, blueBars, bottom=[i+j for i,j in zip(greenBars, orangeBars)], color='lightskyblue', edgecolor='white', width=barWidth, label='Neutral')

    # Add text
    for num in r:
        i = greenBars[num]
        j = orangeBars[num]
        k = blueBars[num]
        threshold = 10
        reduced_factor = 4
        if i != 0.0:
            factor = 2
            if i < threshold:
                factor = reduced_factor
            plt.text(num - 0.1, i/factor, str(round(i, 2)) + "%")
        if j != 0.0:
            factor = 2
            if j < threshold:
                factor = reduced_factor
            plt.text(num - 0.1, i + j/factor, str(round(j, 2)) + "%")
        if k != 0.0:
            factor = 2
            if k < threshold:
                factor = reduced_factor
            plt.text(num - 0.1, i + j + k/factor, str(round(k, 2)) + "%")

    # Custom x axis and title
    plt.xticks(r, names)
    if usecase == "pp":
        uc_fullname = "Predictive Policing"
    elif usecase == "scs":
        uc_fullname = "Smart Complaint System"
    else:
        uc_fullname = "Smart Transportation"
    plt.xlabel("Factors affecting comfort level with " + uc_fullname, fontweight='bold')
    plt.title("Impact of factors for " + uc_fullname, fontweight='bold')

    # Custom y axis
    plt.yticks(np.arange(0, 120, step=20))
    # Note: Total respondents includes only the ones who saw an increase in confidence level
    plt.ylabel("% of respondents", fontweight='bold')  

    # Add a legend
    plt.legend(loc='lower right')

    # Show graphic
    plt.show() 


def getFactorsForUsecase(usecase):
    if usecase == "pp":
        return [usecase + '_lp', usecase + '_anon', usecase + '_publish']
    else:
        return [usecase + '_lp', usecase + '_anon', usecase + '_publish', usecase + '_notify']

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("the script expects exactly one argument, valid values are pp, scs and st")
        sys.exit(2)
    if sys.argv[1] != "pp" and sys.argv[1] != "scs" and sys.argv[1] != "st":
        print("invalid argument")
        sys.exit(2)  

    data = pd.read_csv('data/survey_responses.csv')
    usecase = sys.argv[1]

    # data cleaning
    data.columns = data.columns.str.strip().str.lower().str.replace(' ', '_').str.replace('(', '').str.replace(')', '')

    comf_thresh = 3     # threshold for high comfort
    help_thresh = 3     # threshold for high helpfulness
    help_levels = ['neutral','helpful','nothelpful']    # helpfulness levels

    factorDict = {}
    dictInitialized = False

    for i in range(len(data)): 
        col = usecase+ '_with_cpo'
        # sample size should include only the users that have high comfort post-CPO
        if data.loc[i, col] > comf_thresh:   
            factors = getFactorsForUsecase(usecase)

            # initialize the dictionary, if not already done so
            if dictInitialized == False:
                for factor in factors:
                    for help_level in help_levels:
                        key = factor + '_' + help_level
                        factorDict[key] = 0
                dictInitialized = True
                
            # for each factor, segment users based on how helpful they perceive the factor to be
            for factor_col in factors:
                if data.loc[i, factor_col] == help_thresh:
                    key = factor_col + '_neutral'
                elif data.loc[i, factor_col] > help_thresh:
                    key = factor_col + '_helpful'
                else:
                    key = factor_col + '_nothelpful'
                factorDict[key] += 1   
    factor_list_list = []
    for factor in factors:
        factor_list = []
        for help_level in help_levels:
            key = factor + '_' + help_level
            factor_list.append(factorDict[key])
        factor_list_list.append(factor_list)

    plotPercentStackedBarPlots(factor_list_list, usecase)