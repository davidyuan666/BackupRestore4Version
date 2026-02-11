"""
Restore Engine - 恢复引擎

负责从备份文件恢复数据，支持跨版本恢复
"""
import json
from pathlib import Path
from typing import Dict, List
from .mapper import DataMapper


class RestoreEngine:
    """恢复引擎"""

    def __init__(self, target_version: str, mapper: DataMapper = None):
        self.target_version = target_version
        self.mapper = mapper

    def restore_from_file(self, backup_file: Path) -> List[Dict]:
        """从备份文件恢复数据"""
        with open(backup_file, 'r', encoding='utf-8') as f:
            backup_data = json.load(f)

        source_version = backup_data['schema_version']
        table_name = backup_data['table_name']
        rows = backup_data['data']

        # 如果版本相同，直接返回
        if source_version == self.target_version:
            return rows

        # 如果版本不同，使用 mapper 进行转换
        if self.mapper:
            return [self.mapper.map_row(table_name, row) for row in rows]

        return rows
