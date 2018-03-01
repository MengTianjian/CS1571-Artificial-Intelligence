import sys

def readfile(filename):
    f = open(filename, 'r')
    data = []
    for i in range(6):
        data.append([])
    count = 0
    for line in f:
        instance = readline(line,count)
        data[0].append(instance)
        data[count%5+1].append(instance)
        count += 1
    threshold = ['threshold', 0.10455, 0.21301, 0.28066, 0.065425,
                 0.31222, 0.095901, 0.11421, 0.10529, 0.090067,
                 0.23941, 0.059824, 0.5417, 0.09393, 0.058626,
                 0.049205, 0.24885, 0.14259, 0.18474, 1.6621,
                 0.085577, 0.80976, 0.1212, 0.10165, 0.094269,
                 0.5495, 0.26538, 0.7673, 0.12484, 0.098915,
                 0.10285, 0.064753, 0.047048, 0.097229, 0.047835,
                 0.10541, 0.097477, 0.13695, 0.013201, 0.078629,
                 0.064834, 0.043667, 0.13234, 0.046099, 0.079196,
                 0.30122, 0.17982, 0.0054445, 0.031869, 0.038575,
                 0.13903, 0.016976, 0.26907, 0.075811, 0.044238,
                 5.1915, 52.173, 283.29, 0.39404]
    # print(data[1][1][0])
    return data, threshold

def readline(line, count):
    data = [count+1]
    line = line.split(",")
    for i in line:
        data.append(float(i))
    data[56] = int(data[56])
    data[57] = int(data[57])
    data[58] = int(data[58])
    return data

def train(train_data, val_data, threshold):
    table = [[0 for x in range(58)] for y in range(2)]
    # print len(train_data)
    for i in train_data:
        table[i[58]][0] +=1
        for j in range(57):
            if i[j+1] > threshold[j+1]:
                table[i[58]][j+1] += 1
    prob = [[0 for x in range(58)] for y in range(2)]
    for count, i in enumerate(table):
        prob[count][0] = i[0]/len(train_data)
        for j in range(57):
            prob[count][j+1] = i[j+1]/i[0]
    return test(val_data, prob, threshold)

def test(data, prob, threshold):
    result = []
    # print len(train_data)
    for i in data:
        spam = prob[1][0]
        nonspam = prob[0][0]
        for j in range(57):
            if i[j+1] > threshold[j+1]:
                spam *= prob[1][j+1]
                nonspam *= prob[0][j+1]
            else:
                spam *= (1-prob[1][j+1])
                nonspam *= (1-prob[0][j+1])
        if spam > nonspam:
            result.append(1)
        else:
            result.append(0)
    correct = 0
    fp = 0
    fn = 0
    for i in range(len(data)):
        # if data[i][58]:
        #     fp += 1
        if data[i][58] == result[i]:
            correct += 1
        elif data[i][58]:
            fn += 1
        else:
            fp += 1
    # print(correct/(len(data)))
    return fp, fn

def collect_data(data):
    neg = 0
    pos = 0
    for i in data:
        if i[58]:
            pos += 1
        else:
            neg += 1
    print("POS: "+str(pos/len(data)))
    print("NEG: "+str(neg/len(data)))

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Wrong input arguments!")
    filename = sys.argv[1]
    data, threshold = readfile(filename)
    fp = []
    fn = []
    for i in range(5):
        val_data = data[5-i]
        train_data = []
        # print()
        for j in range(5):
            if j != i:
                train_data += data[5-j]
        # print("Train_"+str(i+1))
        # collect_data(train_data)
        # print("Val_"+str(i+1))
        # collect_data(val_data)
        temp_fp, temp_fn = train(train_data, val_data, threshold)
        print("Fold_"+str(i+1)+",\t"+str(temp_fp/len(val_data))+",\t"+str(temp_fn/len(val_data))+",\t"+str((temp_fp+temp_fn)/len(val_data)))
        fp.append(temp_fp)
        fn.append(temp_fn)
    print("Avg,\t"+str(sum(fp)/len(data[0]))+",\t"+str(sum(fn)/len(data[0]))+",\t"+str((sum(fp)+sum(fn))/len(data[0])))
