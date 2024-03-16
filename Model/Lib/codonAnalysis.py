from Lib import codon
def GC123(seq):
    d = {}
    for nt in ["A", "T", "G", "C"]: d[nt] = [0, 0, 0]

    for i in range(0, len(seq), 3):
        codon = seq[i : i + 3]
        if len(codon) < 3: codon += "  "
        for pos in range(3):
            for nt in ["A", "T", "G", "C"]:
                if codon[pos] == nt or codon[pos] == nt.lower(): d[nt][pos] += 1
    gc = {}
    gcall = 0
    nall = 0
    for i in range(3):
        try:
            n = d["G"][i] + d["C"][i] + d["T"][i] + d["A"][i]
            gc[i] = (d["G"][i] + d["C"][i]) * 100.0 / n
        except Exception: gc[i] = 0
        gcall = gcall + d["G"][i] + d["C"][i]
        nall = nall + n
    
    gcall = 100.0 * gcall / nall if nall != 0 else 0
    return gcall, gc[0], gc[1], gc[2]

def calculate_enc(dna_sequence):
    rscu_values = {
        'AAA': 0.6, 'AAC': 0.8, 'AAG': 1.2, 'AAT': 0.7,
        'ACA': 0.9, 'ACC': 1.0, 'ACG': 1.1, 'ACT': 0.5,
        'AGA': 1.3, 'AGC': 0.7, 'AGG': 1.5, 'AGT': 0.8,
        'ATA': 0.6, 'ATC': 1.2, 'ATG': 1.0, 'ATT': 0.9,
        'CAA': 0.8, 'CAC': 1.0, 'CAG': 1.2, 'CAT': 0.7,
        'CCA': 0.9, 'CCC': 1.0, 'CCG': 1.1, 'CCT': 0.5,
        'CGA': 1.3, 'CGC': 0.7, 'CGG': 1.5, 'CGT': 0.8,
        'CTA': 0.6, 'CTC': 1.2, 'CTG': 1.0, 'CTT': 0.9,
        'GAA': 0.8, 'GAC': 1.0, 'GAG': 1.2, 'GAT': 0.7,
        'GCA': 0.9, 'GCC': 1.0, 'GCG': 1.1, 'GCT': 0.5,
        'GGA': 1.3, 'GGC': 0.7, 'GGG': 1.5, 'GGT': 0.8,
        'GTA': 0.6, 'GTC': 1.2, 'GTG': 1.0, 'GTT': 0.9,
        'TAA': 0.5, 'TAC': 1.1, 'TAG': 0.6, 'TAT': 0.8,
        'TCA': 0.9, 'TCC': 1.0, 'TCG': 1.2, 'TCT': 0.7,
        'TGA': 0.6, 'TGC': 1.0, 'TGG': 1.4, 'TGT': 0.8,
        'TTA': 0.7, 'TTC': 1.1, 'TTG': 1.3, 'TTT': 0.9
    }
    codon_counts = {}
    for i in range(0, len(dna_sequence) - 2, 3):
        codon = dna_sequence[i:i + 3]
        codon_counts[codon] = codon_counts.get(codon, 0) + 1
    sum_rscu_squared = sum(rscu_values[codon] ** 2 if codon in rscu_values else 0 for codon in codon_counts)
    sum_rscu = sum(rscu_values[codon] if codon in rscu_values else 0 for codon in codon_counts)
    enc = sum_rscu_squared / (2 * sum_rscu)
    return enc

def codonAnalysis(sequence, choice=["T3s", "C3s", "A3s", "G3s", "cai", "cbi", "fop", "enc", "GC3s", "GC", "Len_sym", "Len_aa", "hydropathy", "aromaticity"]):
    cseq = codon.CodonSeq(sequence)
    temp = cseq.silent_base_usage()
    data = {i: temp[i] for i in temp.index}
    temp = cseq.bases2()
    data = data | {i: temp[i] for i in temp.index}
    data["enc"] = cseq.enc()
    return ({i: round(data[i], 5) for i in choice}, data)