from re import sub
from random import randint as rand

__author__ = 'Charlie'
codeBook = [["Alanine", "Arginine", "Asparagine", "Aspartate", "Cysteine", "Glutamate", "Glutamine", "Glycine",
             "Histidine", "Isoleucine", "Leucine", "Lysine", "Methionine", "Phenylalanine", "Proline", "Serine",
             "STOP", "Threonine", "Tryptophan", "Tyrosine", "Valine"],
            ["Ala", "Arg", "Asn", "Asp", "Cys", "Gln", "Glu", "Gly", "His", "Ile", "Leu", "Lys", "Met", "Phe", "Pro",
             "Ser", "STOP", "Thr", "Trp", "Tyr", "Val"],
            ["A", "R", "N", "D", "C", "Q", "E", "G", "H", "I", "L", "K", "M", "F", "P",
             "S", " ", "T", "W", "Y", "V"],
            [["CGA", "CGG", "CGT", "CGC"],
             ["GCA", "GCG", "GCT", "GCC", "TCT", "TCC"],
             ["TTA", "TTG"],
             ["CTA", "CTG"],
             ["ACA", "ACG"],
             ["CTT", "CTC"],
             ["GTT", "GTC"],
             ["CCA", "CCG", "CCT", "CCC"],
             ["GTA", "GTG"],
             ["TAA", "TAG", "TAT"],
             ["AAT", "AAC", "GAA", "GAG", "GAT", "GAC"],
             ["TTT", "TTC"],
             ["TAC"],
             ["AAA", "AAG"],
             ["GGA", "GGG", "GGT", "GGC"],
             ["AGA", "AGG", "AGT", "AGC", "TCA", "TCG"],
             ["ATG", "ATT", "ACT"],
             ["TGA", "TGG", "TGT", "TGC"],
             ["ACC"],
             ["ATA", "ATG"],
             ["CAA", "CAG", "CAT", "CAC"]]]

codeBook2 = {"T": {"T": {"T": "Phe", "C": "Phe", "A": "Leu", "G": "Leu"},
                   "C": {"T": "Ser", "C": "Ser", "A": "Ser", "G": "Ser"},
                   "A": {"T": "Tyr", "C": "Tyr", "A": "STOP", "G": "STOP"},
                   "G": {"T": "Cys", "C": "Cys", "A": "STOP", "G": "Trp"}},
             "C": {"T": {"T": "Leu", "C": "Leu", "A": "Leu", "G": "Leu"},
                   "C": {"T": "Pro", "C": "Pro", "A": "Pro", "G": "Pro"},
                   "A": {"T": "His", "C": "His", "A": "Gln", "G": "Gln"},
                   "G": {"T": "Arg", "C": "Arg", "A": "Arg", "G": "Arg"}},
             "A": {"T": {"T": "Ile", "C": "Ile", "A": "Ile", "G": "Met"},
                   "C": {"T": "Thr", "C": "Thr", "A": "Thr", "G": "Thr"},
                   "A": {"T": "Asn", "C": "Asn", "A": "Lys", "G": "Lys"},
                   "G": {"T": "Ser", "C": "Ser", "A": "Arg", "G": "Arg"}},
             "G": {"T": {"T": "Val", "C": "Val", "A": "Val", "G": "Val"},
                   "C": {"T": "Ala", "C": "Ala", "A": "Ala", "G": "Ala"},
                   "A": {"T": "Asp", "C": "Asp", "A": "Glu", "G": "Glu"},
                   "G": {"T": "Gly", "C": "Gly", "A": "Gly", "G": "Gly"}}}

while True:
    code = sub('[ ,]', "", input("Type DNA code\n>> ")).upper()
    if code == '#':
        code = ""
        for i in range(60):
            code += "ATCG"[rand(0,3)]
        print(code)
    codeLen = len(code)
    if len(sub('[ATCG]', "", code)) != 0 or codeLen < 3:
        print("Invalid DNA")
        continue
    else:
        trips = [code[i:i + 3] for i in range(0, codeLen, 3)]
        aminoOut = ""
        for trip in trips:
            if len(trip) == 3:
                aminoOut += codeBook[1][codeBook[1].index(codeBook2[trip[0]][trip[1]][trip[2]])] + " "
        print(aminoOut)
        muttno = input("Input mutation number\n>> ")
        try:
            muttno = int(muttno)
            if muttno <= 0:
                continue
        except:
            continue
        for i in range(1, muttno + 1):
            r1 = rand(0,10)
            if r1 <= 2:
                #substitution
                r2 = rand(0, len(code) - 1)
                rep = "ATCG"[rand(0,3)]
                print("%d: Substitute %d (%s) with %s" %(i, r2, code[r2], rep))
                code = code[:r2] + rep + code[r2+1:]
            elif r1 <= 4:
                #deletion
                r2 = rand(0, len(code) - 1)
                print("%d: Delete %d (%s)" %(i, r2, code[r2]))
                code = code[:r2] + code[r2+1:]
            elif r1 <= 6:
                #insertion
                r2 = rand(0, len(code) - 1)
                rep = "ATCG"[rand(0,3)]
                print("%d: Insert %s at %d" %(i, rep, r2))
                code = code[:r2] + rep + code[r2:]
            else:
                print("%d: No change" %(i))
            print(code)
            trips = [code[i:i + 3] for i in range(0, codeLen, 3)]
            aminoOut = ""
            for trip in trips:
                if len(trip) == 3:
                    aminoOut += codeBook[1][codeBook[1].index(codeBook2[trip[0]][trip[1]][trip[2]])] + " "
            print(aminoOut)