import numpy as np
from matplotlib import pyplot as plt 

colorSiWithUpdate = '#e74c3c'
colorSi = '#2980b9'
colorSiPost = '#8e44ad'
colorWRAcc = '#27ae60'
colorWRAccPost = '#34495e'
colorKLD = '#d35400'
colorKLDPost = '#f39c12'
lineWidth = 2.5

boxpropsSiWithUpdate = dict(linewidth = lineWidth, color = colorSiWithUpdate)
cappropsSiWithUpdate = dict(linewidth = lineWidth, color = colorSiWithUpdate)
whiskerpropsSiWithUpdate = dict(linewidth = lineWidth, color = colorSiWithUpdate)
flierpropsSiWithUpdate = dict(linewidth = lineWidth, color = colorSiWithUpdate)
medianpropsSiWithUpdate = dict(linewidth = lineWidth, color = colorSiWithUpdate)

boxpropsSi = dict(linewidth = lineWidth, color = colorSi)
cappropsSi = dict(linewidth = lineWidth, color = colorSi)
whiskerpropsSi = dict(linewidth = lineWidth, color = colorSi)
flierpropsSi = dict(linewidth = lineWidth, color = colorSi)
medianpropsSi = dict(linewidth = lineWidth, color = colorSi)

boxpropsSiPost = dict(linewidth = lineWidth, color = colorSiPost)
cappropsSiPost = dict(linewidth = lineWidth, color = colorSiPost)
whiskerpropsSiPost = dict(linewidth = lineWidth, color = colorSiPost)
flierpropsSiPost = dict(linewidth = lineWidth, color = colorSiPost)
medianpropsSiPost = dict(linewidth = lineWidth, color = colorSiPost)

boxpropsWRAcc = dict(linewidth = lineWidth, color = colorWRAcc)
cappropsWRAcc = dict(linewidth = lineWidth, color = colorWRAcc)
whiskerpropsWRAcc = dict(linewidth = lineWidth, color = colorWRAcc)
flierpropsWRAcc = dict(linewidth = lineWidth, color = colorWRAcc)
medianpropsWRAcc = dict(linewidth = lineWidth, color = colorWRAcc)

boxpropsWRAccPost = dict(linewidth = lineWidth, color = colorWRAccPost)
cappropsWRAccPost = dict(linewidth = lineWidth, color = colorWRAccPost)
whiskerpropsWRAccPost = dict(linewidth = lineWidth, color = colorWRAccPost)
flierpropsWRAccPost = dict(linewidth = lineWidth, color = colorWRAccPost)
medianpropsWRAccPost = dict(linewidth = lineWidth, color = colorWRAccPost)

boxpropsKLD = dict(linewidth = lineWidth, color = colorKLD)
cappropsKLD  = dict(linewidth = lineWidth, color = colorKLD)
whiskerpropsKLD  = dict(linewidth = lineWidth, color = colorKLD)
flierpropsKLD  = dict(linewidth = lineWidth, color = colorKLD)
medianpropsKLD  = dict(linewidth = lineWidth, color = colorKLD)

boxpropsKLDPost = dict(linewidth = lineWidth, color = colorKLDPost)
cappropsKLDPost = dict(linewidth = lineWidth, color = colorKLDPost)
whiskerpropsKLDPost = dict(linewidth = lineWidth, color = colorKLDPost)
flierpropsKLDPost = dict(linewidth = lineWidth, color = colorKLDPost)
medianpropsKLDPost = dict(linewidth = lineWidth, color = colorKLDPost)

def resultOnePattern(row, minerSD) :
    
    
    indicesListSnapshots = [int(x) for x in row['indiceListSnapshots'].strip('[]').split(',')]
    patternIds = [int(x) for x in row['patternIds'].strip('[]').split(',')]
    patternNames = [x.strip() [1:-1] for x in row['patternNames'].strip('[]').split(',')]

    results = []
    
    for cpt, idAntichain in enumerate (patternIds) :
        firstTime = True
        d_pattern = {}
        xHats = []
        for idMiner in indicesListSnapshots :
            for sdnode in minerSD[idMiner].allSdNodes :
                if sdnode.node.id == idAntichain :
                    xHats.append(sdnode.xHat)
                    if firstTime :
                        xBar = sdnode.xBar
                        firstTime = False
        
        d_pattern['id']   = idAntichain
        d_pattern['name'] = patternNames[cpt]
        d_pattern['xBar'] = xBar
        d_pattern['min']  = np.array(xHats).min()
        d_pattern['max']  = np.array(xHats).max()
        d_pattern['mean'] = round(np.array(xHats).mean())
        d_pattern['med']  = int(np.median(np.array(xHats)))
        d_pattern['q_20'] = round(np.percentile(xHats, 20))
        
        results.append(d_pattern)
    
    return results


def plotOnePattern(row, minerSD, logScale = False) :
    
    results = resultOnePattern(row, minerSD)
    fig, ax = plt.subplots(3, 1, figsize=(5, len(results)*4), constrained_layout=True, sharex = True)
    title = '< ' + row['subgroup'] + ' : ' + str(int(row['lenSubgroup'])) + ' snapshots ' +' >'
    fig.suptitle(title, fontsize = 15)
    names = []
    xBars = []
    minValues = []
    maxValues = []
    meanValues = []
    medValues = []
    qValues = []
    height = 0.5
    
    for result in results :
        names.append(result['name'])
        minValues.append(result['min'])
        maxValues.append(result['max'])
        meanValues.append(result['mean'])
        medValues.append(result['med'])
        qValues.append(result['q_20'])
        xBars.append(result['xBar'])
        
    ax[0].barh(names, xBars, label='xBars', color = '#e74c3c', log = logScale, height = 0.5)
    ax[0].barh(names, minValues, left = xBars, label = 'xHats', color = '#27ae60', log = logScale, height = height)
    ax[0].set_title('Min')
    ax[0].ticklabel_format(axis = 'x', style='', scilimits=(0,0))
    
    ax[1].barh(names, xBars, label='xBars', color = '#e74c3c', log = logScale, height = height)
    ax[1].barh(names, meanValues, left = xBars, label = 'xHats', color = '#27ae60', log = logScale , height = height)
    ax[1].set_title('Average')
    
    ax[2].barh(names, xBars, label='xBars', color = '#e74c3c', log = logScale, height = height)
    ax[2].barh(names, qValues, left = xBars, label = 'xHats', color = '#27ae60', log = logScale, height = height)
    ax[2].set_title('q_20')
    
    
    
    ax[2].set_xlabel('counters', fontsize = 12)
    
    
def avgNormalizedCounters(df, indRows, minerSD) :
    l = []
    for iRow in indRows :
        row = df.iloc[iRow]
        
        indicesListSnapshots = [int(x) for x in row['indiceListSnapshots'].strip('[]').split(',')]
        patternIds = [int(x) for x in row['patternIds'].strip('[]').split(',')]            

        for p in patternIds :
            s = 0
            s_root = 0
            for idMiner in indicesListSnapshots :
                for sdnode in minerSD[idMiner].allSdNodes :
                    if sdnode.node.id == p :
                        s += sdnode.xHat
                s_root += minerSD[idMiner].allSdNodes[0].xHat
            l.append(s / s_root)
    return l
    

def plotOneAvgNormalizedCounters(df, indRows, minerSD, label) :
    
    
    l = avgNormalizedCounters(df, indRows, minerSD)
    if label == 'SI with update' :
        plt.boxplot(l, labels = [label], showmeans=True, boxprops = boxpropsSiWithUpdate, 
                    capprops = cappropsSiWithUpdate, whiskerprops = whiskerpropsSiWithUpdate, 
                    flierprops = flierpropsSiWithUpdate, medianprops = medianpropsSiWithUpdate)
    elif label == 'SI' :
        plt.boxplot(l, labels = [label], showmeans=True, boxprops = boxpropsSi, 
            capprops = cappropsSi, whiskerprops = whiskerpropsSi, 
            flierprops = flierpropsSi, medianprops = medianpropsSi)
    else :
        plt.boxplot(l, labels = [label], showmeans=True, boxprops = boxpropsWRAcc,
                    capprops = cappropsWRAcc, whiskerprops = whiskerpropsWRAcc,
                    flierprops = flierpropsWRAcc, medianprops = medianpropsWRAcc)
    plt.ylabel('Avg normalized counters', fontsize = 12)
    plt.show()
    
    
def plotAllAvgsNormalizedCounters(listDataFrames, listIndRows, minerSD) :
    
    l = []
    for i in range(len(listDataFrames)) :
        l.append(avgNormalizedCounters(listDataFrames[i], listIndRows[i], minerSD))
    plt.figure(figsize=(5,3.5))
    plt.boxplot(l[0], labels = ['SI-update'], showmeans=True, positions=[1.75], boxprops = boxpropsSiWithUpdate,
                capprops = cappropsSiWithUpdate, whiskerprops = whiskerpropsSiWithUpdate,
                flierprops = flierpropsSiWithUpdate, medianprops = medianpropsSiWithUpdate)
    
    plt.boxplot(l[1], labels = ['SI'], showmeans=True, positions=[2], boxprops = boxpropsSi,
                capprops = cappropsSi, whiskerprops = whiskerpropsSi,flierprops = flierpropsSi, 
                medianprops = medianpropsSi)
    
    plt.boxplot(l[2], labels = ['SI-pp'], showmeans=True, positions=[2.25], boxprops = boxpropsSiPost,
                capprops = cappropsSiPost, whiskerprops = whiskerpropsSiPost, flierprops = flierpropsSiPost, 
                medianprops = medianpropsSiPost)
    
    plt.boxplot(l[3], labels = ['CWRAcc'], showmeans=True, positions=[2.5], boxprops = boxpropsWRAcc,
                capprops = cappropsWRAcc, whiskerprops = whiskerpropsWRAcc,
                flierprops = flierpropsWRAcc, medianprops = medianpropsWRAcc)
    
    plt.boxplot(l[4], labels = ['CWRAcc-pp'], showmeans=True, positions=[2.75], boxprops = boxpropsWRAccPost,
                capprops = cappropsWRAccPost, whiskerprops = whiskerpropsWRAccPost,
                flierprops = flierpropsWRAccPost, medianprops = medianpropsWRAccPost)
    plt.gca().legend(('SI-update','SI','SI-PP','CWRAcc','CWRAcc-PP'), loc = 'upper left', fontsize = 10)
    ax = plt.gca()
    leg = ax.get_legend()
    leg.legendHandles[0].set_color('#e74c3c')
    leg.legendHandles[1].set_color('#2980b9')
    leg.legendHandles[2].set_color('#8e44ad')
    leg.legendHandles[3].set_color('#27ae60')
    leg.legendHandles[4].set_color('#34495e')
    
    #plt.ylabel('Avg normalized values', fontsize = 12)
    plt.xticks([])
    plt.savefig('avg normalized', bbox_inches='tight')
    plt.show()
      

def contrastMeasure (df, indRows, minerSD) :
    l = []
    for iRow in indRows :
        s_row = 0
        row = df.iloc[iRow]
        
        indicesListSnapshots = [int(x) for x in row['indiceListSnapshots'].strip('[]').split(',')]
        patternIds = [int(x) for x in row['patternIds'].strip('[]').split(',')]            
        
        for cpt, p in enumerate(patternIds, start = 1) :
            s = 0
            firstTime = True
            for idMiner in indicesListSnapshots :
                for sdnode in minerSD[idMiner].allSdNodes :
                    if sdnode.node.id == p :
                        s += sdnode.xHat
                        if firstTime :
                            xBar = sdnode.xBar
                            firstTime = False 
            s_normalized = s / (len(indicesListSnapshots))
            s_row += (s_normalized - xBar) / s_normalized
        s_row = s_row / cpt
        l.append(s_row)
    return l

def plotOneContrastMeasure(df, indRows, minerSD, label) :
    
    
    l = contrastMeasure(df, indRows, minerSD)
    if label == 'SI with update' :
        plt.boxplot(l, labels = [label], showmeans=True, boxprops = boxpropsSiWithUpdate, 
                    capprops = cappropsSiWithUpdate, whiskerprops = whiskerpropsSiWithUpdate, 
                    flierprops = flierpropsSiWithUpdate, medianprops = medianpropsSiWithUpdate)
    elif label == 'SI' :
        plt.boxplot(l, labels = [label], showmeans=True, boxprops = boxpropsSi, 
            capprops = cappropsSi, whiskerprops = whiskerpropsSi, 
            flierprops = flierpropsSi, medianprops = medianpropsSi)
    else : 
        plt.boxplot(l, labels = [label], showmeans=True, boxprops = boxpropsWRAcc, 
            capprops = cappropsWRAcc, whiskerprops = whiskerpropsWRAcc, 
            flierprops = flierpropsWRAcc, medianprops = medianpropsWRAcc)
    plt.ylabel('Avg contrast', fontsize = 12)
    plt.show()


def plotAllContrastMeasure(listDataFrames, listIndRows, minerSD) :
    l = []
    for i in range(len(listDataFrames)) :
        l.append(contrastMeasure(listDataFrames[i], listIndRows[i], minerSD))
    fig, axs = plt.subplots(figsize=(6,3.5))
    bp0 = axs.boxplot(l[0], labels = ['SI-update'], showmeans=True, positions=[1.75], boxprops = boxpropsSiWithUpdate,
                capprops = cappropsSiWithUpdate, whiskerprops = whiskerpropsSiWithUpdate,
                flierprops = flierpropsSiWithUpdate, medianprops = medianpropsSiWithUpdate)
    
    bp1 = axs.boxplot(l[1], labels = ['SI'], showmeans=True, positions=[2], boxprops = boxpropsSi,
                capprops = cappropsSi, whiskerprops = whiskerpropsSi,flierprops = flierpropsSi, 
                medianprops = medianpropsSi)
    
    bp2 = axs.boxplot(l[2], labels = ['SI-pp'], showmeans=True, positions=[2.25], boxprops = boxpropsSiPost,
                capprops = cappropsSiPost, whiskerprops = whiskerpropsSiPost, flierprops = flierpropsSiPost, 
                medianprops = medianpropsSiPost)
    
    bp3 = axs.boxplot(l[3], labels = ['CWRAcc'], showmeans=True, positions=[2.5], boxprops = boxpropsWRAcc,
                capprops = cappropsWRAcc, whiskerprops = whiskerpropsWRAcc,
                flierprops = flierpropsWRAcc, medianprops = medianpropsWRAcc)
    
    bp4 = axs.boxplot(l[4], labels = ['CWRAcc-pp'], showmeans=True, positions=[2.75], boxprops = boxpropsWRAccPost,
                capprops = cappropsWRAccPost, whiskerprops = whiskerpropsWRAccPost,
                flierprops = flierpropsWRAccPost, medianprops = medianpropsWRAccPost)
    
    bp5 = axs.boxplot(l[5], labels = ['KL-Div'], showmeans=True, positions=[3], boxprops = boxpropsKLD,
            capprops = cappropsKLD, whiskerprops = whiskerpropsKLD,
            flierprops = flierpropsKLD, medianprops = medianpropsKLD)
  
    bp6 = axs.boxplot(l[6], labels = ['KL-Div-pp'], showmeans=True, positions=[3.25], boxprops = boxpropsKLDPost,
    capprops = cappropsKLDPost, whiskerprops = whiskerpropsKLDPost,
    flierprops = flierpropsKLDPost, medianprops = medianpropsKLDPost)
    
    axs.legend([bp0["boxes"][0], bp1["boxes"][0], bp2["boxes"][0], bp3["boxes"][0], bp4["boxes"][0], bp5["boxes"][0], bp6["boxes"][0]],
               ['SCA-Miner','SI','SI-PP','CWRACC','CWRACC-PP','KL-Div','KL-Div-PP'], 
               ncol = 2, loc = 'lower left', fontsize = 12)
    """
    ax = plt.gca()
    leg = ax.get_legend()
    leg.legendHandles[0].set_color('#e74c3c')
    leg.legendHandles[1].set_color('#2980b9')
    leg.legendHandles[2].set_color('#8e44ad')
    leg.legendHandles[3].set_color('#27ae60')
    leg.legendHandles[4].set_color('#34495e')
    leg.legendHandles[5].set_color('#d35400')
    leg.legendHandles[6].set_color('#f39c12')
    """
    plt.ticklabel_format(axis = 'y', style='', scilimits=(0,0))
    plt.ylabel('Contrast', fontsize = 12)
    plt.xticks([])
    plt.yticks(fontsize= 12)
    plt.savefig('contrast', bbox_inches='tight')
    plt.show()
    

def jaccard (l1, l2) :
    s1 = set(l1)
    s2 = set(l2)
    return float(len(s1.intersection(s2)) / len(s1.union(s2)))

def isParentOrChild(p1, p2, minerSD):
    for sdnode in minerSD[0].allSdNodes :
        if sdnode.node.id == p1 :
            for asc in sdnode.node.allAsc :
                if asc.id == p2 :
                    return 1
            for desc in sdnode.node.allDesc :
                if desc.id == p2 :
                    return 1
    return 0 

def redundVersion1(df, indRows, minerSD):
    
    factor = 0
    for i in np.arange(len(indRows)) :
        for j in range(i + 1, len(indRows)) : 
            row1 = df.iloc[indRows[i]]
            row2 = df.iloc[indRows[j]]
            
            row1IndicesListSnapshots = [int(x) for x in row1['indiceListSnapshots'].strip('[]').split(',')]
            row1PatternIds = [int(x) for x in row1['patternIds'].strip('[]').split(',')]

            row2IndicesListSnapshots = [int(x) for x in row2['indiceListSnapshots'].strip('[]').split(',')]
            row2PatternIds = [int(x) for x in row2['patternIds'].strip('[]').split(',')]


            factor1 = jaccard(row1IndicesListSnapshots, row2IndicesListSnapshots)
            if factor1 == 0 :
                factor += 0
            else :
                factor2 = 0
                for p1 in row1PatternIds :
                    for p2 in row2PatternIds :
                        if p1 == p2 :
                            factor2 += 1
                        else :
                            factor2 += isParentOrChild (p1, p2, minerSD)
                factor2 = factor2 / len(set(row1PatternIds).union(set(row2PatternIds)))
                factor += factor1 * factor2
    if len(indRows) == 1 :
        return 0
    else :
        return factor / (len(indRows) * (len(indRows)-1) / 2)
    

def redundVersion2(df, indRows, minerSD):
    factor = 0
    for i in np.arange(len(indRows))[1:] :
        tmp = []
        for j in range(0, i) :
            row1 = df.iloc[indRows[i]]
            row2 = df.iloc[indRows[j]]
            
            row1IndicesListSnapshots = [int(x) for x in row1['indiceListSnapshots'].strip('[]').split(',')]
            row1PatternIds = [int(x) for x in row1['patternIds'].strip('[]').split(',')]

            row2IndicesListSnapshots = [int(x) for x in row2['indiceListSnapshots'].strip('[]').split(',')]
            row2PatternIds = [int(x) for x in row2['patternIds'].strip('[]').split(',')]

            factor1 = jaccard(row1IndicesListSnapshots, row2IndicesListSnapshots)
            if factor1 == 0 :
                tmp.append(0)
            else :
                factor2 = 0
                for p1 in row1PatternIds :
                    best_match = []
                    for p2 in row2PatternIds :
                        if p1 == p2 :
                            best_match.append(1)
                        else :
                            best_match.append(isParentOrChild (p1, p2, minerSD))
                    factor2 += max(best_match)    
                factor2 = factor2 / len(set(row1PatternIds).union(set(row2PatternIds)))
                tmp.append(factor1 * factor2)
        factor += max(tmp)
    if len(indRows) == 1 :
        return 0
    else :
        return factor / (len(indRows)-1)  

def plotAllRedundV1(listDataFrames, listIndRows, minerSD):
    plt.figure(figsize=(6.5,3.5))
    l = []
    for i in range(len(listDataFrames)) :
        l.append(redundVersion1(listDataFrames[i], listIndRows[i], minerSD))
    plt.bar(['SCA-Miner', 'SI', 'SI-PP','CWRAcc','CWRAcc-PP', 'KL-Div', 'KL-Div-PP'], l, color = [colorSiWithUpdate, colorSi, colorSiPost, colorWRAcc, colorWRAccPost, colorKLD, colorKLDPost], width = 0.5)
    plt.ylabel('Redundancy', fontsize = 12)
    plt.ticklabel_format(axis = 'y', style='', scilimits=(0,0))
    plt.yticks(fontsize= 12)
    plt.savefig('redund', bbox_inches='tight')
    plt.show()
    

def plotAllRedundV2(listDataFrames, listIndRows, minerSD):
    plt.figure(figsize=(6.5,3.5))
    l = []
    for i in range(len(listDataFrames)) :
        l.append(redundVersion2(listDataFrames[i], listIndRows[i], minerSD))
    plt.bar(['SCA-Miner', 'SI', 'SI-PP','CWRAcc','CWRAcc-PP', 'KL-Div', 'KL-Div-PP'], l, color = [colorSiWithUpdate, colorSi, colorSiPost, colorWRAcc, colorWRAccPost, colorKLD, colorKLDPost], width = 0.5)
    plt.ylabel('Redundancy', fontsize = 12)
    plt.ticklabel_format(axis = 'y', style='', scilimits=(0,0))
    plt.yticks(fontsize= 12)
    plt.savefig('redund', bbox_inches='tight')
    plt.show()