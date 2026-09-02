import inquirer
import requests
from pathlib import Path
from tqdm import tqdm

MRI_DOWNLOADS = {
    "Original T2-weighted MRI": (
        "https://ftp.ebi.ac.uk/biostudies/fire/S-BIAD/939/S-BIAD1939/Files/EBB/sub-01/ses-02/anat/sub-01_ses-02_T2w.nii.gz",
        "sub-01_ses-02_T2w.nii.gz",
    ),
    "Masked T2-weighted MRI": (
        "https://ftp.ebi.ac.uk/biostudies/fire/S-BIAD/939/S-BIAD1939/Files/EBB/derivatives/sub-01/ses-02/anat/sub-01_ses-02_desc-masked_T2w.nii.gz",
        "sub-01_ses-02_desc-masked_T2w.nii.gz",
    ),
}


def main():
    answer = inquirer.list_input(
        "Which MRI would you like to download?",
        choices=list(MRI_DOWNLOADS.keys()),
    )
    url, filename = MRI_DOWNLOADS[answer]
    output_path = Path(inquirer.text(
        "Output path",
        default=str(Path("../data") / filename),
    ))

    head = requests.head(url, allow_redirects=True)
    size_mb = int(head.headers.get("content-length", 0)) / (1024 * 1024)

    if not inquirer.confirm(
        f"This will download {size_mb:.1f} MB to {output_path}. Continue?",
        default=True,
    ):
        print("Aborted.")
        return

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with requests.get(url, stream=True) as response:
        response.raise_for_status()
        total_bytes = int(response.headers.get("content-length", 0))
        with open(output_path, "wb") as f, tqdm(
            total=total_bytes, unit="B", unit_scale=True, unit_divisor=1024, desc=output_path.name,
        ) as progress:
            for chunk in response.iter_content(chunk_size=1024 * 1024):
                f.write(chunk)
                progress.update(len(chunk))

    print(f"Saved to {output_path}")


if __name__ == "__main__":
    main()
