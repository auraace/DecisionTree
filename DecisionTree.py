import math

class sample:
    def __init__(self, attributes, classification=0):
        self.attributes = attributes
        self.classification = classification

class node:
    def __init__(self, name, attributes=[], parent=None):
        self.name = name
        self.parent = parent
        self.children = []
        self.attributes = attributes

    def show(self, depth):
        print('name: ' + str(self.name) + ', depth: ' + str(depth))
        for c in self.children:
            c.show(depth + 1)

def information(classes, total):
    I = 0
    for c in classes:
        if c != 0:
            I = I - c/total * math.log(c/total,2)
    return I

def isSamplesSameClass(samples):
    last = samples[0]
    for s in samples:
        if last.classification != s.classification:
            return False
        last = s
    return True

def findMostCommonClass(samples, numClasses):
    numSamples = []
    for i in range(numClasses):
        numSamples.append(0)
    for s in samples:
        numSamples[s.classification] = numSamples[s.classification] + 1
    maxValue = max(numSamples)
    maxIndex = numSamples.index(maxValue)
    return maxIndex

def classCount(samples, key):
    count = 0
    for s in samples:
        if s.classification == key:
            count = count + 1
    return count

def getClassCoutns(samples, numClasses):
    classes = []
    for c in range(numClasses):
        classes.append(classCount(samples, c))
    return classes

def samplesWithAttributeValue(samples, attr, value):
    matchingSamples = []
    for s in samples:
        attributes = s.attributes
        if attributes[attr] == value:
            matchingSamples.append(s)
    return matchingSamples

def findHighestInformationGain(samples, arrtList, attrValues, numClasses):
    classes = getClassCoutns(samples, numClasses)
    I = information(classes, len(samples))

    gains = []
    for i in range(len(arrtList)):
        res = 0
        for attrVal in attrValues[i]:
            tempSamples = samplesWithAttributeValue(samples, attrList[i], attrVal)
            tempClasses = getClassCoutns(tempSamples, numClasses)
            valueInfo = 0
            if len(tempSamples) > 0:
                valueInfo = information(tempClasses, len(tempSamples))
            probVal = len(tempSamples) / len(samples)
            res = res + probVal * valueInfo
        gain = I - res
        gains.append(gain)

    maxValue = max(gains)
    maxIndex = attrList[gains.index(maxValue)]
    return maxIndex

def findHighestGainRatio(samples, arrtList, attrValues, numClasses):
    classes = getClassCoutns(samples, numClasses)
    I = information(classes, len(samples))

    gains = []
    for i in range(len(arrtList)):
        res = 0
        splitInfo = 0
        for attrVal in attrValues[i]:
            tempSamples = samplesWithAttributeValue(samples, attrList[i], attrVal)
            tempClasses = getClassCoutns(tempSamples, numClasses)
            valueInfo = 0
            if len(tempSamples) > 0:
                valueInfo = information(tempClasses, len(tempSamples))
            probVal = len(tempSamples) / len(samples)
            res = res + probVal * valueInfo
            if probVal != 0:
                splitInfo = splitInfo - probVal * math.log(probVal,2)
        gain = (I - res)
        gainRatio = gain / splitInfo
        gains.append(gainRatio)

    maxValue = max(gains)
    maxIndex = attrList[gains.index(maxValue)]
    return maxIndex

def findHighestGiniIndex(samples, arrtList, attrValues, numClasses):
    ginis = []
    for i in range(len(arrtList)):
        gini = 1
        for attrVal in attrValues[i]:
            tempSamples = samplesWithAttributeValue(samples, attrList[i], attrVal)
            probVal = len(tempSamples) / len(samples)
            gini = gini - (probVal**2)
        ginis.append(gini)

    maxValue = max(ginis)
    maxIndex = attrList[ginis.index(maxValue)]
    return maxIndex

def generateDecisionTree(samples, attribute_list, global_attribute_list, attribute_values, attribute_names, num_classes, metric):
    n = node('name')
    if isSamplesSameClass(samples):
        n.name = 'class: ' + str(samples[0].classification)
        return n
    if len(attribute_list) == 0:
        cl = findMostCommonClass(samples, num_classes)
        n.name = 'class: ' + str(cl)
        return n

    if metric == 0:
        test_attribute = findHighestInformationGain(samples, attribute_list, attribute_values, num_classes)
    elif metric == 1:
        test_attribute = findHighestGainRatio(samples, attribute_list, attribute_values, num_classes)
    else:
        test_attribute = findHighestGiniIndex(samples, attribute_list, attribute_values, num_classes)

    testIndex = attribute_list.index(test_attribute)
    globalAttrIndex = global_attribute_list.index(test_attribute)
    attrVals = attribute_values[testIndex]
    attrName = attribute_names[testIndex]
    n.name = attrName
    attribute_list.pop(testIndex)
    attribute_values.pop(testIndex)
    attribute_names.pop(testIndex)
    for attrVal in attrVals:
        attrNode = node(attrVal)
        n.children.append(attrNode)
        si = samplesWithAttributeValue(samples, globalAttrIndex, attrVal)
        if len(si) == 0:
            cl = findMostCommonClass(samples, num_classes)
            leafNode = node('class: ' + str(cl))
        else:
            leafNode = generateDecisionTree(si, attribute_list, global_attribute_list, attribute_values, attribute_names, num_classes, metric)
        attrNode.children.append(leafNode)
    return n


# using tennis data from question 3
input = [['sunny', '80 to 89', '80 to 89', 'not windy', 0],
        ['sunny', '80 to 89', '90 to 99', 'windy', 0],
        ['overcast', '80 to 89', '80 to 89', 'not windy', 1],
        ['rainy', '70 to 79', '90 to 99', 'not windy', 1],
        ['rainy', '60 to 69', '80 to 89', 'not windy', 1],
        ['rainy', '60 to 69', '70 to 79', 'windy', 0],
        ['overcast', '60 to 69', '60 to 69', 'windy', 1],
        ['sunny', '70 to 79', '90 to 99', 'not windy', 0],
        ['sunny', '60 to 69', '70 to 79', 'not windy', 1],
        ['rainy', '70 to 79', '80 to 89', 'not windy', 1],
        ['sunny', '70 to 79', '70 to 79', 'windy', 1],
        ['overcast', '70 to 79', '90 to 99', 'windy', 1],
        ['overcast', '80 to 89', '70 to 79', 'not windy', 1],
        ['rainy', '70 to 79', '90 to 99', 'windy', 0]]
samples = []
for s in input:
    attr = []
    classification = s.pop()
    samp = sample(s, classification)
    samples.append(samp)
attrNames = ['outlook', 'temperature', 'humidity', 'wind level']
attrList = [0, 1, 2, 3]
attrList2 = [0, 1, 2, 3]
attrValues = [['sunny', 'rainy', 'overcast'],
              ['60 to 69', '70 to 79', '80 to 89'],
              ['60 to 69', '70 to 79', '80 to 89', '90 to 99'],
              ['not windy', 'windy']]
attrValues2 = [[1, 2, 3],
              [6, 7, 8],
              [6, 7, 8, 9],
              [0, 1]]
numClasses = 2
# 0 = information gain
# 1 = gain ratio
# 2 = gini index
metric = 0
findHighestGainRatio(samples, attrList, attrValues, numClasses)
DT = generateDecisionTree(samples, attrList, attrList2, attrValues, attrNames, numClasses, metric)
DT.show(0)