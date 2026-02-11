"""
Schema Manager - 数据库 Schema 版本管理器

负责管理不同版本的数据库 schema 定义，检测版本间的差异
"""
import json
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict


@dataclass
class FieldDefinition:
    """字段定义"""
    name: str
    type: str
    nullable: bool = True
    default: Optional[str] = None


@dataclass
class TableDefinition:
    """表定义"""
    name: str
    fields: List[FieldDefinition]
    primary_key: List[str]
    foreign_keys: Dict[str, str] = None  # {field: referenced_table.field}

    def __post_init__(self):
        if self.foreign_keys is None:
            self.foreign_keys = {}


@dataclass
class SchemaVersion:
    """Schema 版本"""
    version: str
    tables: Dict[str, TableDefinition]
    description: str = ""

    def to_dict(self):
        """转换为字典"""
        return {
            'version': self.version,
            'description': self.description,
            'tables': {
                name: {
                    'name': table.name,
                    'fields': [asdict(f) for f in table.fields],
                    'primary_key': table.primary_key,
                    'foreign_keys': table.foreign_keys
                }
                for name, table in self.tables.items()
            }
        }


class SchemaManager:
    """Schema 版本管理器"""

    def __init__(self, schema_dir: Path):
        self.schema_dir = Path(schema_dir)
        self.schema_dir.mkdir(exist_ok=True)
        self.versions: Dict[str, SchemaVersion] = {}
        self._load_versions()

    def _load_versions(self):
        """加载所有版本的 schema"""
        for schema_file in self.schema_dir.glob("*.json"):
            with open(schema_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                version = data['version']
                self.versions[version] = self._parse_schema(data)

    def _parse_schema(self, data: dict) -> SchemaVersion:
        """解析 schema 数据"""
        tables = {}
        for table_name, table_data in data['tables'].items():
            # 解析字段定义
            fields = []
            for field_name, field_info in table_data['fields'].items():
                fields.append(FieldDefinition(
                    name=field_name,
                    type=field_info['type'],
                    nullable=field_info.get('nullable', True),
                    default=field_info.get('default')
                ))

            # 提取主键
            primary_keys = [field_name for field_name, field_info in table_data['fields'].items()
                          if field_info.get('primary_key', False)]

            tables[table_name] = TableDefinition(
                name=table_name,
                fields=fields,
                primary_key=primary_keys,
                foreign_keys=table_data.get('foreign_keys', {})
            )
        return SchemaVersion(
            version=data['version'],
            tables=tables,
            description=data.get('description', '')
        )

    def get_version(self, version: str) -> Optional[SchemaVersion]:
        """获取指定版本的 schema"""
        return self.versions.get(version)

    def list_versions(self) -> List[str]:
        """列出所有版本"""
        return sorted(self.versions.keys())

    def compare_versions(self, v1: str, v2: str) -> Dict:
        """比较两个版本的差异"""
        schema1 = self.versions.get(v1)
        schema2 = self.versions.get(v2)

        if not schema1 or not schema2:
            raise ValueError(f"Version not found: {v1 if not schema1 else v2}")

        differences = {
            'added_tables': [],
            'removed_tables': [],
            'modified_tables': {}
        }

        # 检测新增和删除的表
        tables1 = set(schema1.tables.keys())
        tables2 = set(schema2.tables.keys())

        differences['added_tables'] = list(tables2 - tables1)
        differences['removed_tables'] = list(tables1 - tables2)

        # 检测修改的表
        common_tables = tables1 & tables2
        for table_name in common_tables:
            table_diff = self._compare_tables(
                schema1.tables[table_name],
                schema2.tables[table_name]
            )
            if table_diff:
                differences['modified_tables'][table_name] = table_diff

        return differences

    def _compare_tables(self, table1: TableDefinition, table2: TableDefinition) -> Dict:
        """比较两个表的差异"""
        diff = {
            'added_fields': [],
            'removed_fields': [],
            'modified_fields': {}
        }

        # 获取字段名集合
        fields1 = {f.name: f for f in table1.fields}
        fields2 = {f.name: f for f in table2.fields}

        # 检测新增和删除的字段
        diff['added_fields'] = list(set(fields2.keys()) - set(fields1.keys()))
        diff['removed_fields'] = list(set(fields1.keys()) - set(fields2.keys()))

        # 检测修改的字段
        common_fields = set(fields1.keys()) & set(fields2.keys())
        for field_name in common_fields:
            f1, f2 = fields1[field_name], fields2[field_name]
            if f1.type != f2.type or f1.nullable != f2.nullable:
                diff['modified_fields'][field_name] = {
                    'old': {'type': f1.type, 'nullable': f1.nullable},
                    'new': {'type': f2.type, 'nullable': f2.nullable}
                }

        # 如果没有差异，返回 None
        if not any([diff['added_fields'], diff['removed_fields'], diff['modified_fields']]):
            return None

        return diff
