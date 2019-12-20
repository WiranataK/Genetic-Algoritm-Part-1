import random

def convert(list):
    s = [str(i) for i in list]
    res = int("".join(s))
    return(res)

def binaryToDecimal(binary):
    binary1 = binary
    decimal, i, n = 0, 0, 0
    while (binary != 0):
        dec = binary % 10
        decimal = decimal + dec * pow(2, i)
        binary = binary // 10
        i += 1
    return decimal

def maxBiner(bilanganBulat):
    if (bilanganBulat == 0):
        return 1
    hasil = 1
    for angka in range (1, bilanganBulat + 1, 1):
        hasil = (2 ** angka) - 1
    return hasil

def crossOver(p1, p2):
    titik_potong = random.randint(1, len(p1) - 1)
    kemungkinan = random.uniform(0, 1)
    kesempatan = 0.75
    sementara1 = individu([], len(p1))
    sementara2 = individu([], len(p2))
    sementara1.kromosom = p1.copy()
    sementara2.kromosom = p2.copy()
    if (kesempatan >= kemungkinan):
        for i in range(titik_potong):
            sementara0 = sementara1.kromosom[i]
            sementara1.kromosom[i] = sementara2.kromosom[i]
            sementara2.kromosom[i] = sementara0
        sementara3 = [sementara1, sementara2]
        return(sementara3)
    anaknya = [sementara1, sementara2]
    return anaknya

def mutasi(individu):
    poin_mutasi = random.randint(0, individu.panjang_kromosom - 1)
    kemungkinan = random.uniform(0, 1)
    kesempatan = 0.5
    if (kesempatan >= kemungkinan):
        if (individu.kromosom[poin_mutasi] == 1):
            individu.kromosom[poin_mutasi] = 0
        else:
            individu.kromosom[poin_mutasi] = 1
    return individu

class individu:
    kromosom = []
    panjang_kromosom = 0
    genox1 = 0
    genox2 = 0
    fenox1 = 0
    fenox2 = 0
    fitness = 0
    
    def __init__(self, kromosom, panjang_kromosom):
        self.kromosom = kromosom
        self.panjang_kromosom = panjang_kromosom
        if (len(kromosom) == 0) :
            self.kromosom = [None] * self.panjang_kromosom
            self.individu_awal()
        self.individu_awal()
    
    def individu_awal(self):
        i = 0
        while (i < self.panjang_kromosom):
            self.kromosom[i] = random.randint(0, 1)
            i += 1
        self.fitness = 0

    def genotip(self):
        geno = self.panjang_kromosom // 2
        self.genox1 = convert(self.kromosom[0 : geno])
        self.genox2 = convert(self.kromosom[geno : self.panjang_kromosom])
        # print(self.genox1)
        # print(self.genox2)

    def fenotip(self):
        genotipdesimal1 = binaryToDecimal(self.genox1)
        genotipdesimal2 = binaryToDecimal(self.genox2)
        self.fenox1 = -3 + ((genotipdesimal1 / maxBiner(self.panjang_kromosom // 2)) * 6)
        self.fenox2 = -2 + ((genotipdesimal2 / maxBiner(self.panjang_kromosom // 2)) * 4)
        # print(self.fenox1)
        # print(self.fenox2)

    def hitung_fitness(self):
        fit = ((4 - (2.1 * self.fenox1 ** 2) + (self.fenox1 ** 4 / 3)) * self.fenox1 ** 2 + self.fenox1 * self.fenox2 + (-4 + 4 * self.fenox2 ** 2) * self.fenox2 ** 2)
        self.fitness = -fit

    def buat_individu(self):
        self.genotip()
        self.fenotip()
        self.hitung_fitness()

class populasi: 
    banyak_individu = []
    besar_populasi = 0

    def __init__(self, besar_populasi, panjang_kromosom):
        
        self.besar_populasi = besar_populasi
        self.banyak_individu = [None] * self.besar_populasi
        for i in range(self.besar_populasi):
            kromosom = []
            individu_baru = individu(kromosom, panjang_kromosom)
            self.banyak_individu[i] = individu_baru

    def populasi_baru(self, fitness_terbesar):
        sementara = [fitness_terbesar]
        for i in range(1, self.besar_populasi, 2):
            orang_tua = self.pemilihan_orang_tua()
            kromosom_populasi = crossOver(orang_tua[0].kromosom, orang_tua[1].kromosom)
            sementara.append(mutasi(kromosom_populasi[0]))
            i += 1
            if (i < self.besar_populasi):
                sementara.append(mutasi(kromosom_populasi[1]))
            kromosom_populasi.clear()
        self.banyak_individu = sementara.copy()
    
    def fitness_terbesar(self):
        individu_fitness_terbesar = self.banyak_individu[0]
        for i in range(1, self.besar_populasi):
            if (individu_fitness_terbesar.fitness <= self.banyak_individu[i].fitness):
                individu_fitness_terbesar = self.banyak_individu[i]
        return individu_fitness_terbesar

    def fitness_keseluruhan(self):
        total = 0
        for i in range(self.besar_populasi):
            total = total + self.banyak_individu[i].fitness
        return total

    def pemilihan_orang_tua(self):
        idx = 0
        kemungkinan = random.uniform(-1, 1)
        fitness_sementara = 0
        while (kemungkinan > fitness_sementara):
            fitness_sementara = fitness_sementara + (self.banyak_individu[idx].fitness / self.fitness_keseluruhan())
            if (kemungkinan > fitness_sementara):
                idx = idx + 1
        parent = [self.banyak_individu[idx]]
        idx2 = 0
        fitness_sementara = 0
        kemungkinan = random.uniform(-1,1)
        coba = 0
        while (kemungkinan > fitness_sementara):
            fitness_sementara = fitness_sementara + (self.banyak_individu[idx2].fitness / self.fitness_keseluruhan())
            if (kemungkinan > fitness_sementara):
                idx2 = idx2 + 1
            else:
                if(idx == idx2 & coba < 100):
                    kemungkinan = random.uniform(0,1)
                    fitness_sementara = 0
                    idx2 = 0
                    coba = coba + 1
        parent.append(self.banyak_individu[idx])
        return parent

#Main Program
besar_populasi =10
panjang_kromosom = 10
result = populasi(besar_populasi, panjang_kromosom)

x = 0
print("\n Generasi Ke-", x + 1)
solusi_sebelum = -111111
solusi = 0
generasi = 0
generasi_solusi = individu([], panjang_kromosom)
while ((abs(solusi - solusi_sebelum) > 0.00000001) or (generasi < 200)):

    for i in range(besar_populasi):
        print("kromosom ke-", i + 1, end = "\t: ")
        result.banyak_individu[i].buat_individu()
        print(result.banyak_individu[i].kromosom, end = "\nFitness : ")
        print(result.banyak_individu[i].fitness)
    print("\nKromosom Paling Fitness : ", result.fitness_terbesar().kromosom, end=" ")
    print("\nFitness : ", result.fitness_terbesar().fitness, end=" ")
    print("\nx1 = ", result.fitness_terbesar().fenox1, end=" ")
    print("\nx2 = ", result.fitness_terbesar().fenox2, end=" ")
    solusi_sebelum = solusi
    if (solusi <= result.fitness_terbesar().fitness) :
        solusi = result.fitness_terbesar().fitness
        generasi_solusi = result.fitness_terbesar()
    
    print("\nPemilihan Orang Tua =")
    orang_tua = result.pemilihan_orang_tua()
    for j in orang_tua:
        print(j.kromosom)

    print("Kromosom Terbaik =",generasi_solusi.kromosom)
    print("---Dekode Kromosom Terbaik---")
    print("x1 = ",generasi_solusi.fenox1)
    print("x2 = ",generasi_solusi.fenox2)

    result.populasi_baru(result.fitness_terbesar())
    x += 1
    generasi = generasi + 1
    if (abs(solusi - solusi_sebelum) > 0.00000001) or (generasi < 200):
        print("\n Generasi Ke-", x + 1)
    i=0
    
    