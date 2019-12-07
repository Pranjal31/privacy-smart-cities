import pandas as pd
import matplotlib.pyplot as plt
import csv
import sys
           
def classifyUser(i, data, usecase):
    sig_incr_thresh = 3      # threshold for significant increase
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
    numResponses = segments[0] + segments[1] +segments[2] +segments[3]
    sig_inc_pc = 100.0 * segments[0] / numResponses
    insig_inc_pc = 100.0 * segments[1] / numResponses
    nc_pc = 100.0 * segments[2] / numResponses
    dec_pc = 100.0 * segments[3] / numResponses

    labels = [r'Significant Increase (' + str(sig_inc_pc)+ '%)', r'Insignificant Increase (' + str(insig_inc_pc)+ '%)', 
    r'No Change (' + str(nc_pc)+ '%)', r'Decrease (' + str(dec_pc)+ '%)']
    colors = ['lightskyblue', 'gold', 'lightcoral', 'yellowgreen']
    patches, texts = plt.pie(segments, colors=colors, startangle=90)
    plt.legend(patches, labels, loc="best")
    # Set aspect ratio to be equal so that pie is drawn as a circle.
    plt.axis('equal')
    plt.tight_layout()
    plt.show()

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

    numSignificantIncrease = 0
    numInsignificantIncrease = 0
    numNoChange = 0
    numDecrease = 0

    # segment users
    for i in range(len(data)): 
        segment = classifyUser(i, data, usecase)
        if(segment == "SignificantIncrease"):
            numSignificantIncrease += 1
        elif(segment == "InsignificantIncrease"):
            numInsignificantIncrease += 1
        elif(segment == "NoChange"):
            numNoChange += 1
        else:
            numDecrease += 1

    segments = [numSignificantIncrease, numInsignificantIncrease, numNoChange, numDecrease]
    plotPieChart(segments)
 




    