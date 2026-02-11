"""
Backup Engine - 备份引擎

负责执行数据库备份操作，只备份数据不备份 schema
"""
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any


class BackupEngine:
    """备份引擎"""

    def __init__(self, schema_version: str, output_dir: Path):
        self.schema_version = schema_version
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

    def backup_table(self, table_name: str, rows: List[Dict]) -> Path:
        """备份单个表的数据"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = self.output_dir / f"{table_name}_{timestamp}.json"

        backup_data = {
            'schema_version': self.schema_version,
            'table_name': table_name,
            'timestamp': timestamp,
            'row_count': len(rows),
            'data': rows
        }

        with open(backup_file, 'w', encoding='utf-8') as f:
            json.dump(backup_data, f, indent=2, ensure_ascii=False)

        return backup_file
