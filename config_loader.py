import yaml
from typing import List, TypedDict

class ConfigDict(TypedDict):
    bucket_name: str
    prefix_list: List[str]

def load_config(path: str = 'config.yaml') -> ConfigDict:
    """Load config.yaml and return config dict."""
    with open(path, 'r') as f:
        config: ConfigDict = yaml.safe_load(f)
    return config
