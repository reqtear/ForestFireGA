import random
import numpy as np
import matplotlib.pyplot as plt

def translateToMap(DNA):
    map = []
    mapTemp = []
    for baris in range(0,20):
        for kolom in range(0,20):
            mapTemp.append(0)
        map.append(mapTemp)
        mapTemp = []

    for x in range(0,len(DNA)):
        xMap = DNA[x][0]
        yMap = DNA[x][1]
        for i in range(0,DNA[x][3]):#panjang block
            if(DNA[x][2] == 1):#jika vertikal
                if(xMap >= len(map)):
                    break
                map[xMap][yMap] = 1
                xMap += 1
            else:
                if(yMap >= len(map)):
                    break
                map[xMap][yMap] = 1
                yMap += 1
        xMap = DNA[x][0]
        yMap = DNA[x][1]
        if(DNA[x][4] == 1 and DNA[x][2] == 1):
            if(xMap+DNA[x][3] > 19):
                map[random.randrange(xMap,20)][yMap] = 2
            else:
                map[random.randrange(xMap,xMap+DNA[x][3])][yMap] = 2
        elif(DNA[x][4] == 1 and DNA[x][2] == 0):
            if(yMap+DNA[x][3] > 19):
                map[xMap][random.randrange(yMap,20)] = 2
            else:
                map[xMap][random.randrange(yMap,yMap+DNA[x][3])] = 2
    
    return map

def initPop(size):
    DNA = [] #x,y,vertikal(1)/horizontal(0),panjang,titik api(1)/tidak(0)
    pop = []

    for i in range(0,size):

        for x in range(0,68):
            c = []
            c.append(random.randrange(0,20))
            c.append(random.randrange(0,20))
            c.append(random.randrange(0,2))
            c.append(random.randrange(1,5))
            c.append(random.randrange(0,2))
            DNA.append(c)
        
        pop.append(DNA)
        DNA = []

    return pop

def printDNA(DNA):
    for x in range(len(DNA)):
        print(DNA[x])
        print()
    
def printPop(pop):
    for x in range(len(pop)):
        print("individu ke-" + str(x) + "\n")
        printDNA(pop[x])
        print()

def gambarMap(map):
    fig = plt.figure(figsize=(6, 3.2))

    ax = fig.add_subplot(1,1,1)
    ax.set_title('colorMap')
    plt.imshow(map)
    ax.set_aspect('equal')

    cax = fig.add_axes([0.12, 0.1, 0.78, 0.8])
    cax.get_xaxis().set_visible(False)
    cax.get_yaxis().set_visible(False)
    cax.patch.set_alpha(0)
    cax.set_frame_on(False)
    plt.colorbar(orientation='vertical')
    plt.show()

def tes1(map): #check if playable

    #Array Traveled
    Trav = []

    #Array Intersection
    Inter = []

    #Cari jumlah floor
    floorCount = 0

    for b in range(len(map)):
        for k in range(len(map)):
            if(map[b][k] == 0):
                floorCount += 1

    #Cari Starting Point
    while True:
        baris = random.randrange(0,len(map))
        kolom = random.randrange(0,len(map))
        if(map[baris][kolom] == 0):
            break

    #Cek Intersection
    def isIntersect(baris, kolom):
        count = 0
        if(baris != len(map)-1 and map[baris+1][kolom] == 0):
            count += 1
        if(baris != 0 and map[baris-1][kolom] == 0):
            count += 1
        if(kolom != len(map)-1 and map[baris][kolom+1] == 0):
            count += 1
        if(kolom != 0 and map[baris][kolom-1] == 0):
            count += 1
        if(count > 1):
            return True
        else: return False

    #Cek Setiap Jalan
    while True:
        if(isIntersect(baris,kolom)):
            if([baris,kolom] in Inter):
                hitung = 0
                if(baris != len(map)-1 and map[baris+1][kolom] == 0 and [baris+1,kolom] not in Trav):
                    hitung += 1
                if(baris != 0 and map[baris-1][kolom] == 0 and [baris-1,kolom] not in Trav):
                    hitung += 1
                if(kolom != len(map)-1 and map[baris][kolom+1] == 0 and [baris,kolom+1] not in Trav):
                    hitung += 1
                if(kolom != 0 and map[baris][kolom-1] == 0 and [baris,kolom-1] not in Trav):
                    hitung += 1
                if(hitung <= 1):
                    Inter.remove([baris,kolom])
            else:
                Inter.append([baris,kolom])

        if([baris,kolom] not in Trav):
            Trav.append([baris,kolom])

        if(baris != len(map)-1 and map[baris+1][kolom] == 0 and [baris+1,kolom] not in Trav):
            baris += 1
        elif(baris != 0 and map[baris-1][kolom] == 0 and [baris-1,kolom] not in Trav):
            baris -= 1
        elif(kolom != len(map)-1 and map[baris][kolom+1] == 0 and [baris,kolom+1] not in Trav):
            kolom +=1
        elif(kolom != 0 and map[baris][kolom-1] == 0 and [baris,kolom-1] not in Trav):
            kolom -=1
        else:
            if not Inter:
                break
            else:
                baris = Inter[-1][0]
                kolom = Inter[-1][1]

    if(len(Trav) < floorCount):
        nilai1 = 0.2
    elif(len(Trav) == floorCount):
        nilai1 = 1

    return nilai1

def tes2(map): #cek persebaran pohon

    Hasil = []
    Temp = []
    sekitar = 0

    #Cari jumlah impassable
    imCount = 0

    for b in range(len(map[0])):
        for k in range(len(map[0])):
            if(map[b][k] != 0):
                imCount += 1

    #Cek kepadatan impassable
    for baris in range(0,len(map)):
        for kolom in range(0,len(map)):
            if(map[baris][kolom] != 0): #cek apakah batu/pohon
                if(baris == len(map)-1 or kolom == len(map)-1 or baris == 0 or kolom == 0): #cek apakah di pinggir
                    if(baris == len(map)-1 and kolom == len(map)-1): #cek apakah di sudut
                        sekitar += 5
                    elif(baris == 0 and kolom == len(map)-1):
                        sekitar += 5
                    elif(baris == 0 and kolom == 0):
                        sekitar += 5
                    elif(baris == len(map)-1 and kolom == 0):
                        sekitar += 5
                    else:
                        sekitar += 3
                if(kolom != len(map)-1 and map[baris][kolom+1] != 0): #kanan
                    sekitar += 1
                    Temp.append([baris,kolom+1])
                if(baris != len(map)-1 and map[baris+1][kolom] != 0): #bawah
                    sekitar += 1
                    Temp.append([baris+1,kolom])
                if(kolom != 0 and map[baris][kolom-1] != 0): #kiri
                    sekitar += 1
                    Temp.append([baris,kolom-1])
                if(baris != 0 and map[baris-1][kolom] != 0): #atas
                    sekitar += 1
                    Temp.append([baris-1,kolom])
                if(kolom != len(map)-1 and baris != 0 and map[baris-1][kolom+1] != 0): #kanan atas
                    sekitar += 1
                    Temp.append([baris-1,kolom+1])
                if(kolom != 0 and baris != 0 and map[baris-1][kolom-1] != 0): #kiri atas
                    sekitar += 1
                    Temp.append([baris-1,kolom-1])
                if(kolom != len(map)-1 and baris != len(map)-1 and map[baris+1][kolom+1] != 0): #kanan bawah
                    sekitar += 1
                    Temp.append([baris+1,kolom+1])
                if(kolom != 0 and baris != len(map)-1 and map[baris+1][kolom-1] != 0): #kiri bawah
                    sekitar += 1
                    Temp.append([baris+1,kolom-1])
                Temp.append([baris,kolom])
                if(sekitar>6):
                    for x in range(0,len(Temp)):
                        if(Temp[x] not in Hasil):
                            Hasil.append(Temp[x])
            Temp = []
            sekitar = 0

    nilai2 = round(1-len(Hasil)/imCount, 2)

    return nilai2

def tes3(DNA): #V&H ratio
    vCount = 0
    hCount = 0
    for x in range(0,len(DNA)):
        if(DNA[x][2] == 1): #jika vertikal
            vCount += 1
        else:
            hCount += 1
    
    if(vCount >= hCount):
        nilai = round(hCount/vCount,2)
    else:
        nilai = round(vCount/hCount,2)
    
    return nilai

def tes4(map): #titik api
    count = 0
    for b in range(len(map)):
        for k in range(len(map)):
            if(map[b][k] == 2):
                count +=1
    
    if(count < 5):
        nilai = 1
    else:
        nilai = round(5/count,2)

    return nilai

def nilaiFit(DNA): 
    map = translateToMap(DNA)

    nilaiFit = tes1(map)*0.4 + tes2(map)*0.1 + tes3(DNA)*0.1 + tes4(map)*0.4

    return round(nilaiFit,2)

def Parent(fitpop): #pemilihan 2 parent dalam bentuk index pop
	totalFit = sum(fitpop)
	cek1 = 0
	cek2 = 0
	indexParent = 0
	parent = []
	pickParent1 = random.uniform(0,totalFit)
	while True:
		pickParent2 = random.uniform(0,totalFit)
		if(pickParent1 != pickParent2):
			break
	for i in range(0,len(fitpop)):
		indexParent += fitpop[i]
		if(indexParent >= pickParent1 and cek1 == 0):
			parent.append(i)
			cek1 = 1
		if(indexParent >= pickParent2 and cek2 == 0):
			parent.append(i)
			cek2 = 1
	return parent

def crossOver(p1,p2):
    a1 = []
    a2 = []
    temp1 = []

    for x in range(len(p1)):
        temp1.append(p1[x][0])
        temp1.append(p2[x][1])
        temp1.append(p1[x][2])
        temp1.append(p2[x][3])
        temp1.append(p1[x][4])
        a1.append(temp1)
        temp1 = []
        temp1.append(p2[x][0])
        temp1.append(p1[x][1])
        temp1.append(p2[x][2])
        temp1.append(p1[x][3])
        temp1.append(p2[x][4])
        a2.append(temp1)
        temp1 = []
    
    return [a1,a2]

def crossOverV2(p1,p2):
    toggle = 1
    kid1 = []
    kid2 = []
    for x in range(len(p1)):
        if(toggle == 1):
            kid1.append(p1[x])
            kid2.append(p2[x])
        else:
            kid1.append(p2[x])
            kid2.append(p1[x])
        if((x + 1)% 12 == 0):
            toggle *= -1
    return [kid1,kid2]           

def mutation(pop,chance): #chance 5%
    for x in range(len(pop)):
        roll = random.random()
        if(roll <= chance):
            DNA = pop[x]
            randBaris = random.randrange(0,len(DNA))
            DNA[randBaris][0] = random.randrange(0,20)
            DNA[randBaris][1] = random.randrange(0,20)
            DNA[randBaris][2] = random.randrange(0,2)
            DNA[randBaris][3] = random.randrange(1,5)
            DNA[randBaris][4] = random.randrange(0,2)
            pop[x] = DNA
     
    return pop

def sortSecond(val):
    return val[1]

def replaceLowest(fitpop,pop,kid):
    tempPop = []
    for x in range(len(fitpop)):
        temp = []
        temp.append(x)
        temp.append(fitpop[x])
        tempPop.append(temp)
    
    tempPop.sort(key = sortSecond, reverse = True)
    pop[tempPop[-2][0]] = kid[0]
    pop[tempPop[-1][0]] = kid[1]

    return pop

def sortPop(pop,fitpop):
    tempPop = []
    for x in range(len(fitpop)):
        temp = []
        temp.append(x)
        temp.append(fitpop[x])
        tempPop.append(temp)
    
    tempPop.sort(key = sortSecond, reverse = True)
    return tempPop

#=======================================================================

pop = initPop(60)

count = 0
for j in range(0,len(pop)):
    map = translateToMap(pop[j])
    for ba in range(len(map)):
        for ko in range(len(map)):
            if(map[ba][ko] == 2):
                count += 1

rataPop0 = round(count/len(pop),2) 

averageFit = []

for i in range(0,800):
    if(i == 0):
        gambarMap(translateToMap(pop[0]))

    fitPop = []

    for x in range(0,len(pop)):
        fitPop.append(nilaiFit(pop[x]))

    parent = Parent(fitPop)

    anak = crossOver(pop[parent[0]],pop[parent[1]])

    pop = replaceLowest(fitPop,pop,anak)

    pop = mutation(pop,0.05)

    averageFit.append(round(sum(fitPop)/60,2))

    print(i)

count = 0
for j in range(0,len(pop)):
    map = translateToMap(pop[j])
    for ba in range(len(map)):
        for ko in range(len(map)):
            if(map[ba][ko] == 2):
                count += 1

rataPopAkhir = round(count/len(pop),2) 

print("rata2 jumlah titik api gen 1 = " + str(rataPop0))
print("rata2 jumlah titik api last gen = " + str(rataPopAkhir))

rank1 = sortPop(pop,fitPop)
#printDNA(rank1)
#print(averageFit[-1])
gambarMap(translateToMap(pop[rank1[0][0]]))
map = translateToMap(pop[rank1[0][0]])
printDNA(map)
#print("tes 4 rank 1 = " + str(tes4(translateToMap(pop[rank1[0][0]]))))
plt.plot(averageFit)
plt.ylabel('fitness')
plt.xlabel('generation')
plt.show()