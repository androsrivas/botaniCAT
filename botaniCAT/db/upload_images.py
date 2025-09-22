import os
import glob
import csv
from pathlib import Path
from botaniCAT.cloudinary.utils import upload_image
from botaniCAT.db.repository import get_connection, insert_plant_image, Transaction

IMAGE_FOLDER = Path("data/img") 
LOG_CSV = "data/logs/upload_images_log.csv"
VALID_EXTENSIONS = [".jpg", ".jpeg", ".png"]

def filename_to_taxon(filename):
    name = filename.stem
    if "_" in name and name.split("_")[-1].isdigit():
        name = "_".join(name.split("_")[:-1])
    taxon = name.replace('_', ' ')
    return taxon.strip()

def main():
    conn = get_connection()

    images = [f for f in IMAGE_FOLDER.iterdir() if f.suffix.lower() in VALID_EXTENSIONS]
    
    not_found_taxon = []
    plant_counters = {}

    with open(LOG_CSV, mode="w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["plant_id", "filename", "public_id", "image_url"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        with Transaction(conn) as cur:
            for path in images:
                taxon = filename_to_taxon(path)

                cur.execute("SELECT id, taxon FROM Plants WHERE taxon LIKE ? COLLATE NOCASE", (f"%{taxon}%",))
                rows = cur.fetchall()

                if not rows:
                    print(f"Plant not found for taxon {taxon} - skipping")
                    not_found_taxon.append(taxon)
                    continue

                if len(rows) > 1:
                    print(f"Warning: multiple matches found for taxon {taxon}. Using first match.")
                    

                plant_id = rows[0][0]

                count = plant_counters.get(plant_id, 0) + 1
                plant_counters[plant_id] = count

                base_name = os.path.splitext(os.path.basename(path))[0]
                public_id = f"plant_{plant_id}_{count}_{base_name}"

                print(f"Uploading {path} for plant_id {plant_id}, taxon {taxon}, and public_id {public_id}")

                res = upload_image(str(path), public_id=public_id, folder="botaniCAT/plants")
                image_url = res.get("secure_url")

                insert_plant_image(conn, plant_id, image_url, public_id)

                writer.writerow({
                    "plant_id" : plant_id,
                    "filename" : os.path.basename(path),
                    "public_id" : public_id,
                    "image_url" : image_url
                })

    if not_found_taxon:
        print("\nThe following taxon was not found in the database:")
        for taxon in not_found_taxon:
            print(f"- {taxon}")

    conn.close()
    print(f"All done! Log saved to {LOG_CSV}")

if __name__ == "__main__":
    main()