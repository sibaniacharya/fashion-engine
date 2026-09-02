import os
import shutil


def clean_stale_data():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    dirs_to_clean = [
        os.path.join(base_dir, "output"),
        os.path.join(base_dir, "data", "analyzed"),
    ]

    for d in dirs_to_clean:
        if os.path.exists(d):
            print(f"Cleaning directory: {d}")
            for filename in os.listdir(d):
                file_path = os.path.join(d, filename)
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                except Exception as e:
                    print(f"Failed to delete {file_path}. Reason: {e}")


if __name__ == "__main__":
    clean_stale_data()
