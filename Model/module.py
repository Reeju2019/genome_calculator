import json, csv, os, sys, requests, gzip, glob
from io import BytesIO
from .codonAnalysis import codonAnalysis


def download_and_unzip(url, output_directory):
    response = requests.get(url)
    if response.status_code == 200:
        # Get the file name from the URL
        file_name = url.split("/")[-1].split(".")[0] + ".fa"
        file_path = os.path.join(output_directory, file_name.replace(".gz", ""))

        # Write the decompressed data to a file
        with gzip.open(BytesIO(response.content), "rb") as f_in, open(
            file_path, "wb"
        ) as f_out:
            f_out.write(f_in.read())

        return file_path
    else:
        print(f"Failed to download {url}")
        return None


def process_file(path, saveindex=100):
    codonfile = json.load(open(path, "r"))
    analysisfile = json.load(open(path.replace("raw_json", "process_json"), "r"))
    for index, codon in enumerate(codonfile):
        if "cds length" not in analysisfile[index].keys():
            try:
                analysisfile[index] = analysisfile[index] | calculate_seq(
                    codon["sequence"]
                )
            except:
                pass
            sys.stdout.write(
                "\r"
                + f'{path.split("/")[-1].split(".")[0]} >> [{index + 1} | {len(codonfile)}] || ({codon["cds ID"]}) Processing'
            )
            sys.stdout.flush()
            if index % saveindex == 0:
                with open(path.replace("raw_json", "process_json"), "w") as wf:
                    wf.write(json.dumps(analysisfile, indent=4))
                jsontocsv(
                    csvFilename=path.replace(".json", ".csv").replace(
                        "raw_json", "csv"
                    ),
                    jsondata=analysisfile,
                )
        else:
            sys.stdout.write(
                "\r"
                + f'{path.split("/")[-1].split(".")[0]} >> [{index + 1} | {len(codonfile)}] || ({codon["cds ID"]}) Done'
            )
            sys.stdout.flush()
    with open(path.replace("raw_json", "process_json"), "w") as wf:
        wf.write(json.dumps(analysisfile, indent=4))
    jsontocsv(
        csvFilename=path.replace(".json", ".csv").replace("raw_json", "csv"),
        jsondata=analysisfile,
    )


def process_seq(string, organism, organism_group):
    temp = {}
    temp["cds ID"] = string.split("\n")[0].split(" ")[0]
    temp["sequence"] = "".join(string.split("\n")[1:])
    temp["organism"] = organism.split(".")[0]
    temp["organism-group"] = organism_group
    return temp


def fastatojson(filepath=""):
    organism = filepath.split("/")[4]
    organism_group = filepath.split("/")[3]
    fileobj = open(filepath, "r").read().replace("->", " ")
    codonSeq, codonDetails = [], []
    for codon in fileobj.split(">"):
        if codon != "":
            temp = process_seq(codon, organism, organism_group)
            codonSeq.append(
                {
                    "cds ID": temp["cds ID"],
                    "sequence": temp["sequence"],
                }
            )
            codonDetails.append(
                {
                    "cds ID": temp["cds ID"],
                    "organism": temp["organism"],
                    "organism-group": temp["organism-group"],
                }
            )
    with open(
        filepath.replace("fasta", "raw_json")
        .replace(".fa", ".json")
        .replace(".txt", ".json"),
        mode="w",
    ) as file:
        file.write(json.dumps(codonSeq, indent=4))
    with open(
        filepath.replace("fasta", "process_json")
        .replace(".fa", ".json")
        .replace(".txt", ".json"),
        mode="w",
    ) as file:
        file.write(json.dumps(codonDetails, indent=4))
    return filepath.replace("fasta", "raw_json").replace(".fa", ".json")
