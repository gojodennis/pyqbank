
from datasets import load_dataset
import warnings

# Suppress warnings
warnings.filterwarnings("ignore")

def inspect():
    print("Loading dataset: Reja1/jee-neet-benchmark")
    # Load streaming to avoid full download
    ds = load_dataset("Reja1/jee-neet-benchmark", split="test", streaming=True)
    
    print("Dataset Features:")
    print(ds.features)
    
    print("\nFirst Example:")
    item = next(iter(ds))
    for key, value in item.items():
        if key == 'image':
            print(f"{key}: <Image Object>")
        else:
            print(f"{key}: {value}")

if __name__ == "__main__":
    inspect()
