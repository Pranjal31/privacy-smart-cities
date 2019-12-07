import pandas as pd
import matplotlib.pyplot as plt
import csv
import numpy as np

def plotPercentStackedBarPlots(segmentList):
    n = len(segmentList)
    r = range(n)
    names = ('Enforce Laws and Policies','Anonymize Data', 'Publish Technical Details', 'Notify about Data Collection')
    raw_data = {'blueBars': [segmentList[0][0], segmentList[1][0], segmentList[2][0], segmentList[3][0]], 'greenBars': [segmentList[0][1], segmentList[1][1],segmentList[2][1], segmentList[3][1]],'orangeBars': [segmentList[0][2], segmentList[1][2], segmentList[2][2], segmentList[3][2]]}

    df = pd.DataFrame(raw_data)
    # From raw value to percentage
    totals = [i+j+k for i,j,k in zip(df['orangeBars'], df['greenBars'], df['blueBars'])]
    orangeBars = [i * 100.0 / j for i,j in zip(df['orangeBars'], totals)]
    greenBars = [i * 100.0 / j for i,j in zip(df['greenBars'], totals)]
    blueBars = [i * 100.0 / j for i,j in zip(df['blueBars'], totals)]

    # plot
    barWidth = 0.85
    # Create green Bars
    plt.bar(r, greenBars, color='yellowgreen', edgecolor='white', width=barWidth, label='Helpful')
    # Create orange Bars
    plt.bar(r, orangeBars, bottom=greenBars, color='lightcoral', edgecolor='white', width=barWidth, label='Not Helpful')
    # Create blue Bars
    plt.bar(r, blueBars, bottom=[i+j for i,j in zip(greenBars, orangeBars)], color='lightskyblue', edgecolor='white', width=barWidth, label='Neutral')
 
    # Custom x axis
    plt.xticks(r, names)
    plt.xlabel("Factors affecting overall comfort levels across the three use cases", fontweight='bold')

    # Custom y axis
    plt.yticks(np.arange(0, 120, step=20))
    # Note: Total respondents includes only the ones who saw an increase in confidence level
    plt.ylabel("% of respondents", fontweight='bold')  

    # Add a legend
    plt.legend(loc='upper left', bbox_to_anchor=(1,1), ncol=1)

    # Show graphic
    plt.show() 


def getFactorsForUsecase(usecase):
    if usecase == "pp":
        return ['lp', 'anon','publish']
    else:
        return ['lp', 'anon', 'publish', 'notify']

if __name__ == '__main__':
    data = pd.read_csv('data/survey_responses.csv')

    # data cleaning
    data.columns = data.columns.str.strip().str.lower().str.replace(' ', '_').str.replace('(', '').str.replace(')', '')

    comf_thresh = 3     # threshold for high comfort
    help_thresh = 3     # threshold for high helpfulness
    help_levels = ['neutral','helpful','nothelpful']    # helpfulness levels
    usecases = ['pp','scs','st']    # all the usecases
    factors = ['lp', 'anon', 'publish', 'notify']
    factorDict = {}

    # initialize the dictionary
    for factor in factors:
        for help_level in help_levels:
            key = factor + '_' + help_level
            factorDict[key] = 0

    for i in range(len(data)): 
        for usecase in usecases:
            col = usecase+ '_with_cpo'
            
            # sample size should include only the users that have high comfort post-CPO
            if data.loc[i, col] > comf_thresh:   
                ucFactors = getFactorsForUsecase(usecase)
                    
                # for each factor, segment users based on how helpful they perceive the factor to be
                for ucFactor in ucFactors:
                    if data.loc[i, usecase + '_' + ucFactor] == help_thresh:
                        key = ucFactor + '_neutral'
                    elif data.loc[i, usecase + '_' + ucFactor] > help_thresh:
                        key = ucFactor + '_helpful'
                    else:
                        key = ucFactor + '_nothelpful'
                    factorDict[key] += 1   

    factor_list_list = []
    for factor in factors:
        factor_list = []
        for help_level in help_levels:
            key = factor + '_' + help_level
            factor_list.append(factorDict[key])
        factor_list_list.append(factor_list)
    plotPercentStackedBarPlots(factor_list_list)