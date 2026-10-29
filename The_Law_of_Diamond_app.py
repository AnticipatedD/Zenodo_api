import requests, json, sys

ACCESS_TOKEN = sys.argv[2]
FILE_PATH = sys.argv[4]
METADATA = json.load(open(sys.argv[6]))

headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}

# Create a new deposition
r = requests.post("https://zenodo.org/api/deposit/depositions",
                  headers=headers, json={"metadata": METADATA})
deposition = r.json()

# Upload file
bucket_url = deposition["links"]["bucket"]
with open(FILE_PATH, "rb") as fp:
    requests.put(f"{bucket_url}/release.tar.gz",
                 data=fp, headers=headers)
