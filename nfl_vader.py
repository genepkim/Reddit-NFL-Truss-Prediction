from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

def main():

   #initialize vader sentiment intensity analyzer
    analyzer = SentimentIntensityAnalyzer()

    #create dictionaries for negative and positive sentences
    positive = []
    negative = []
    neutral  = []

    #read in targeted file to train
    with open('testresult.txt') as f:
        lines = f.readlines()
        for comment in lines:
            vs = analyzer.polarity_scores(comment)
            compound = vs['compound']

            if(compound >= .05):
                positive.append(comment)
            elif(compound <= -.05):
                negative.append(comment)
            elif(compound > -.05 and compound< .05):
                neutral.append(comment)

           #print("{:-<65} {}".format(comment,str(vs['compound']))) #formatting from vader documentation
    total_classified = len(positive) + len(negative) + len(neutral)

    poss_per         = len(positive) / total_classified
    neg_per         = len(negative) / total_classified
    neu_per         = len(neutral) / total_classified


    print("positive percentage = " + str(poss_per))
    print("negative percentage = " + str(neg_per))
    print("neutral percentage = " + str(neu_per))

    # if neg_per > .3:
    #     if neg_per > pos_per:
    #         print("Outcome for Game: Loss")
    #
    #     print("yes")
    getProb(poss_per, neg_per)
    # print(prob)
    # print("Pos:" str(poss_per))
    # print(str(neg_per))
    # print(str(neu_per))


def getProb(pos, neg):
    if neg < pos:
        if neg < .2:
            print("100% chance of Win")
        else:
            print("76% chance of Win")
    elif pos < neg:
        if pos < .35 and pos < neg:
            print("40% chance of Win")
        else:
            print("600% chance of Loss")
    elif pos == neg:
        print("inconclusive")


if __name__ == "__main__":
    main()
