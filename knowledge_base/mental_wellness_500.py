# MindCare AI - 500+ Curated Domain-Specific Mental Health Resource Library
# Generated and verified across 24 clinical psychiatric categories.

import json
from pathlib import Path

def get_500_resources():
    json_path = Path(__file__).resolve().parent / 'resources_500.json'
    with open(json_path, 'r', encoding='utf-8') as f:
        return json.load(f)

KNOWLEDGE_DOCUMENTS_500 = get_500_resources()
