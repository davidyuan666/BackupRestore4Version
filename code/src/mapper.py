"""
Data Mapper - 数据映射器

负责在不同版本的 schema 之间进行数据映射和转换
"""
from typing import Dict, List, Any, Optional
from dataclasses import dataclass


@dataclass
class FieldMapping:
    """字段映射规则"""
    source_field: str
    target_field: str
    transform: Optional[str] = None  # 转换函数名
    default_value: Any = None


@dataclass
class TableMapping:
    """表映射规则"""
    source_table: str
    target_table: str
    field_mappings: List[FieldMapping]
    condition: Optional[str] = None  # 过滤条件


class DataMapper:
    """数据映射器"""

    def __init__(self, source_version: str, target_version: str):
        self.source_version = source_version
        self.target_version = target_version
        self.mappings: Dict[str, TableMapping] = {}

    def add_table_mapping(self, mapping: TableMapping):
        """添加表映射"""
        self.mappings[mapping.source_table] = mapping

    def map_row(self, table_name: str, source_row: Dict) -> Dict:
        """映射单行数据"""
        if table_name not in self.mappings:
            return source_row

        mapping = self.mappings[table_name]
        target_row = {}

        for field_mapping in mapping.field_mappings:
            source_value = source_row.get(field_mapping.source_field)

            if source_value is None and field_mapping.default_value is not None:
                target_row[field_mapping.target_field] = field_mapping.default_value
            elif field_mapping.transform:
                target_row[field_mapping.target_field] = self._apply_transform(
                    source_value, field_mapping.transform
                )
            else:
                target_row[field_mapping.target_field] = source_value

        return target_row

    def _apply_transform(self, value: Any, transform: str) -> Any:
        """应用转换函数"""
        # 这里可以扩展支持各种转换
        if transform == 'to_string':
            return str(value) if value is not None else None
        elif transform == 'to_int':
            return int(value) if value is not None else None
        return value
