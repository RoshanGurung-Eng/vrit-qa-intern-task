"""
Data Loader Utility - Load test data from CSV, JSON, or Excel files.
Perfect for data-driven testing and parameterization.
"""
import json
import csv
from pathlib import Path
from typing import List, Dict, Union, Optional
from dataclasses import dataclass, asdict, fields
import pandas as pd

from utils.logger import logger
from exceptions.automation_errors import AutomationError


@dataclass
class TestData:
    """Base dataclass for test data validation."""
    
    @classmethod
    def from_dict(cls,  dict):
        """Create instance from dictionary, ignoring extra keys."""
        valid_keys = {f.name for f in fields(cls)}
        filtered = {k: v for k, v in data.items() if k in valid_keys}
        return cls(**filtered)
    
    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return asdict(self)


class DataLoaderError(AutomationError):
    """Raised when data loading fails."""
    pass


class DataLoader:
    """
    Unified loader for test data from multiple formats.
    
    Supports:
    - CSV files (with headers)
    - JSON files (list of objects or single object)
    - Excel files (.xlsx, .xls)
    - Python dictionaries (for dynamic data)
    """
    
    SUPPORTED_EXTENSIONS = {'.csv', '.json', '.xlsx', '.xls'}
    
    def __init__(self, base_path: Optional[Union[str, Path]] = None):
        self.base_path = Path(base_path) if base_path else Path("data")
        self.base_path.mkdir(parents=True, exist_ok=True)
    
    def load(self, filename: str, data_class: Optional[type] = None) -> Union[List[Dict], List[TestData]]:
        """
        Auto-detect format and load data.
        
        Args:
            filename: Name of the file (with extension)
            data_class: Optional dataclass to cast each row to
            
        Returns:
            List of dictionaries or dataclass instances
        """
        filepath = self.base_path / filename
        
        if not filepath.exists():
            raise DataLoaderError(f"File not found: {filepath}")
        
        ext = filepath.suffix.lower()
        logger.info(f"Loading data from {filepath} ({ext} format)")
        
        try:
            if ext == '.csv':
                records = self._load_csv(filepath)
            elif ext == '.json':
                records = self._load_json(filepath)
            elif ext in {'.xlsx', '.xls'}:
                records = self._load_excel(filepath)
            else:
                raise DataLoaderError(f"Unsupported format: {ext}")
            
            # Cast to dataclass if specified
            if data_class and issubclass(data_class, TestData):
                return [data_class.from_dict(r) for r in records]
            
            return records
            
        except Exception as e:
            raise DataLoaderError(f"Failed to load {filename}: {e}")
    
    def _load_csv(self, filepath: Path) -> List[Dict]:
        """Load CSV file with UTF-8 support."""
        with open(filepath, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            return list(reader)
    
    def _load_json(self, filepath: Path) -> List[Dict]:
        """Load JSON file (supports array or single object)."""
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data if isinstance(data, list) else [data]
    
    def _load_excel(self, filepath: Path, sheet_name: Optional[str] = None) -> List[Dict]:
        """Load Excel file using pandas."""
        df = pd.read_excel(filepath, sheet_name=sheet_name)
        # Replace NaN with None for cleaner data
        return df.where(pd.notna(df), None).to_dict(orient='records')
    
    def save(self, filename: str, data: Union[List[Dict], List[TestData]], format: str = 'json') -> Path:
        """
        Save data to file.
        
        Args:
            filename: Output filename
             List of dicts or dataclass instances
            format: 'csv', 'json', or 'excel'
            
        Returns:
            Path to saved file
        """
        filepath = self.base_path / filename
        records = [d.to_dict() if hasattr(d, 'to_dict') else d for d in data]
        
        logger.info(f"Saving {len(records)} records to {filepath}")
        
        if format == 'json':
            with open(filepath.with_suffix('.json'), 'w', encoding='utf-8') as f:
                json.dump(records, f, indent=2, ensure_ascii=False)
                
        elif format == 'csv':
            if not records:
                raise DataLoaderError("Cannot save empty data to CSV")
            with open(filepath.with_suffix('.csv'), 'w', encoding='utf-8', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=records[0].keys())
                writer.writeheader()
                writer.writerows(records)
                
        elif format == 'excel':
            df = pd.DataFrame(records)
            df.to_excel(filepath.with_suffix('.xlsx'), index=False)
        else:
            raise DataLoaderError(f"Unsupported save format: {format}")
        
        return filepath
    
    def generate_combinations(self, base_ Dict, variations: Dict[str, List]) -> List[Dict]:
        """
        Generate test data combinations (cartesian product).
        
        Example:
            base = {"firstName": "Roshan", "lastName": "Gurung"}
            variations = {"country": ["Nepal", "India"], "experience": ["1-2", "3-5"]}
            → Returns 4 combinations with all variations
        """
        from itertools import product
        
        keys = list(variations.keys())
        values = list(variations.values())
        combinations = []
        
        for combo in product(*values):
            record = base_data.copy()
            record.update(dict(zip(keys, combo)))
            combinations.append(record)
        
        logger.info(f"Generated {len(combinations)} test combinations")
        return combinations