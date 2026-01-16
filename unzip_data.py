import zipfile
import os

zip_files = [
    "api_data_aadhar_biometric.zip",
    "api_data_aadhar_demographic.zip",
    "api_data_aadhar_enrolment.zip"
]

base_dir = r"d:\UIDAI"

for zf in zip_files:
    path = os.path.join(base_dir, zf)
    if os.path.exists(path):
        print(f"Extracting {zf}...")
        try:
            with zipfile.ZipFile(path, 'r') as zip_ref:
                zip_ref.extractall(base_dir)
            print(f"Successfully extracted {zf}")
        except zipfile.BadZipFile:
            print(f"Error: {zf} is a bad zip file")
        except Exception as e:
            print(f"Failed to extract {zf}: {e}")
    else:
        print(f"File not found: {zf}")
