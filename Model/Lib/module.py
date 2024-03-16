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


def jsontocsv(csvFilename="./jsonoutput.csv", jsondata=None, jsonfilename="", mode="w"):
    if jsondata == None and jsonfilename == "":
        return print("please provide the json data")
    elif jsonfilename != "":
        jsondata = json.load(open(jsonfilename))
    with open(csvFilename, mode, newline="") as csvFile:
        csv_writer = csv.writer(csvFile)
        count = 0
        for data in jsondata:
            if mode != "a+" and count == 0:
                header = data.keys()
                csv_writer.writerow(header)
                count += 1
            csv_writer.writerow(data.values())
    return True


def csvtojson(filename=""):
    if filename == "":
        return print("please provide the csv data")
    with open(filename, mode="r") as file:
        csvFile = list(csv.reader(file))
        jsondata = []
        for lines in csvFile[1:]:
            temp = {}
            for title, element in zip(csvFile[0], lines):
                temp[title] = element
            jsondata.append(temp)
        return jsondata


def process_seq(string, organism, organism_group):
    temp = {}
    temp["cds ID"] = string.split("\n")[0].split(" ")[0]
    temp["sequence"] = "".join(string.split("\n")[1:])
    temp["organism"] = organism.split(".")[0]
    temp["organism-group"] = organism_group
    return temp


def calculate_seq(sequence):
    # gc_cunt, gc1, gc2, gc3 = GC123(sequence)
    # enc = calculate_enc(sequence)
    temp = codonAnalysis(sequence, choice=["GC", "GC1", "GC2", "GC3", "enc"])[0]
    return {
        "cds length": len(sequence),
        "GC%": temp["GC"] * 100,
        "ENc": temp["enc"],
        "GC1": temp["GC1"] * 100,
        "GC2": temp["GC2"] * 100,
        "GC3": temp["GC3"] * 100,
    }


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


def define_organism(path="./Data/raw_json"):
    organism_dirct = []
    for root, directories, files in os.walk(path):
        for file in files:
            organism_dirct.append(
                {
                    "path": os.path.join(root, file).replace("\\", "/"),
                }
            )
    return organism_dirct


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


# Read CSV file
# def load_csv_data(organism):
#     root = "./Data/csv"
#     csv.field_size_limit(500000000)

#     # List of sub-folders
#     sub_folders = ["Aves", "Crustacea", "Mammalia", "Molusca", "Osteichthyes"]
    
#     # Load all records from CSVs in sub-folders
#     all_records = []
#     for folder in sub_folders:
#         folder_path = os.path.join(root, folder)
#         csv_files = glob.glob(os.path.join(folder_path, "*.csv"))

#         for f in csv_files:
#             with open(f) as file:
#                 reader = csv.reader(file)
#                 records = list(reader)
#                 all_records.extend(records[1:])
#     return all_records

def load_csv_data(organism):
    root = "./Data/csv"
    all_records = []
    for file in os.listdir(f"{root}/{organism}"):
        with open(f"{root}/{organism}/{file}") as rf:
            reader = csv.reader(rf)
            records = list(reader)
            all_records.extend(records[1:])
    return all_records

# Extract features
def get_features(records, feature_cols, labels=-1):
    return (
        [[float(row[i]) for i in feature_cols] for row in records],
        [row[labels] for row in records if labels != -1],
    )
