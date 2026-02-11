"""
Data Mapper - 数据映射器

负责在不同版本的 schema 之间进行数据映射和转换
实现论文中描述的三阶段自动映射算法
"""
from typing import Dict, List, Any, Optional, Set
from dataclasses import dataclass
from .schema_manager import SchemaVersion, TableDefinition, FieldDefinition


@dataclass
class FieldMapping:
    """字段映射规则"""
    source_field: str
    target_field: str
    transform: Optional[str] = None  # 转换函数名
    default_value: Any = None
    mapping_type: str = "direct"  # direct, cast, default, computed


@dataclass
class TableMapping:
    """表映射规则"""
    source_table: str
    target_table: str
    field_mappings: List[FieldMapping]
    condition: Optional[str] = None  # 过滤条件


class DataMapper:
    """数据映射器 - 实现自动字段映射算法

    实现论文中描述的三阶段映射算法：
    Phase 1: Direct Mapping - 类型兼容的字段直接映射
    Phase 2: Deprecated Fields - 源版本独有字段标记为跳过
    Phase 3: New Fields - 目标版本新增字段使用默认值或转换规则
    """

    def __init__(self, source_schema: 'SchemaVersion', target_schema: 'SchemaVersion'):
        self.source_schema = source_schema
        self.target_schema = target_schema
        self.mappings: Dict[str, TableMapping] = {}
        self.auto_generated_count = 0
        self.manual_count = 0
        self.transformation_rules: Dict[str, callable] = {}

    def generate_automatic_mapping(self, table_name: str) -> TableMapping:
        """自动生成表映射规则 - 实现论文Algorithm 1"""
        source_table = self.source_schema.tables.get(table_name)
        target_table = self.target_schema.tables.get(table_name)

        if not source_table or not target_table:
            raise ValueError(f"Table {table_name} not found in source or target schema")

        field_mappings = []

        # Phase 1: Direct Mapping - 处理共同字段
        source_fields = {f.name: f for f in source_table.fields}
        target_fields = {f.name: f for f in target_table.fields}

        common_fields = set(source_fields.keys()) & set(target_fields.keys())
        for field_name in common_fields:
            source_field = source_fields[field_name]
            target_field = target_fields[field_name]

            if self._is_type_compatible(source_field.type, target_field.type):
                # 直接映射
                field_mappings.append(FieldMapping(
                    source_field=field_name,
                    target_field=field_name,
                    mapping_type="direct"
                ))
                self.auto_generated_count += 1
            else:
                # 需要类型转换
                field_mappings.append(FieldMapping(
                    source_field=field_name,
                    target_field=field_name,
                    transform=self._get_type_cast(source_field.type, target_field.type),
                    mapping_type="cast"
                ))
                self.auto_generated_count += 1

        # Phase 2: Deprecated Fields - 源版本独有字段标记为跳过
        removed_fields = set(source_fields.keys()) - set(target_fields.keys())
        # 这些字段不需要添加到映射中，会被自动忽略

        # Phase 3: New Fields - 目标版本新增字段
        added_fields = set(target_fields.keys()) - set(source_fields.keys())
        for field_name in added_fields:
            target_field = target_fields[field_name]

            if target_field.default is not None:
                # 使用默认值
                field_mappings.append(FieldMapping(
                    source_field=None,
                    target_field=field_name,
                    default_value=target_field.default,
                    mapping_type="default"
                ))
                self.auto_generated_count += 1
            elif field_name in self.transformation_rules:
                # 使用转换规则
                field_mappings.append(FieldMapping(
                    source_field=None,
                    target_field=field_name,
                    transform=field_name,
                    mapping_type="computed"
                ))
                self.auto_generated_count += 1
            else:
                # 设置为NULL（如果允许）
                if target_field.nullable:
                    field_mappings.append(FieldMapping(
                        source_field=None,
                        target_field=field_name,
                        default_value=None,
                        mapping_type="default"
                    ))
                    self.auto_generated_count += 1
                else:
                    # 需要手动指定
                    self.manual_count += 1

        return TableMapping(
            source_table=table_name,
            target_table=table_name,
            field_mappings=field_mappings
        )

    def _is_type_compatible(self, source_type: str, target_type: str) -> bool:
        """检查类型是否兼容"""
        if source_type == target_type:
            return True

        # 定义兼容的类型转换
        compatible_types = {
            ('INT', 'BIGINT'),
            ('FLOAT', 'DOUBLE'),
            ('VARCHAR', 'TEXT'),
            ('DATE', 'DATETIME'),
        }

        return (source_type, target_type) in compatible_types

    def _get_type_cast(self, source_type: str, target_type: str) -> str:
        """获取类型转换函数名"""
        type_cast_map = {
            ('INT', 'BIGINT'): 'to_bigint',
            ('FLOAT', 'DOUBLE'): 'to_double',
            ('VARCHAR', 'TEXT'): 'to_text',
            ('DATE', 'DATETIME'): 'to_datetime',
        }
        return type_cast_map.get((source_type, target_type), 'identity')


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
