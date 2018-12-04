"""Extract no. of genes and bp included in de 
novo assembly by trinity.  
"""

__author__ = "Sarah Hazell Pickering (sarah.pickering@anu.edu.au)"
__date__ = "2018-09-27"

def getTrinityStats(path):
    f = open(path, 'r')
    for line in f:
        line = line.strip()
        if line.startswith("Total trinity 'genes':"):
            genes = int(line.split()[-1])
        elif line.startswith("Total assembled bases"):
            bp = int (line.split()[-1])
            break
    f.close()
    collate = [genes, bp]
    return collate

if __name__ == '__main__':
    getTrinityStats("/home/sarah/packages/necklace/t-test06/de_novo_assembly/demo_de_novo.fa.stats")
