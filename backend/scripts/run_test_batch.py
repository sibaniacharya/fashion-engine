import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from ai.batch_processor import BatchProcessor

if __name__ == "__main__":
    processor = BatchProcessor()
    print("Running test batch of 3 records...")
    result = processor.process_all(batch_size=3)
    print("Test batch result:", result)
