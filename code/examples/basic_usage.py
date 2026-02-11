"""
使用示例：演示如何使用版本化备份恢复系统
"""
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent / 'src'))

from schema_manager import SchemaManager, SchemaVersion, TableDefinition, FieldDefinition
from backup_engine import BackupEngine
from restore_engine import RestoreEngine
from mapper import DataMapper, TableMapping, FieldMapping


def example_backup():
    """示例：备份数据"""
    print("=== 备份示例 ===")

    # 创建备份引擎
    backup_engine = BackupEngine(
        schema_version="1.0.0",
        output_dir=Path("./backups")
    )

    # 模拟患者表数据
    patient_data = [
        {"id": 1, "name": "张三", "age": 45, "gender": "M"},
        {"id": 2, "name": "李四", "age": 32, "gender": "F"}
    ]

    # 执行备份
    backup_file = backup_engine.backup_table("patients", patient_data)
    print(f"备份完成: {backup_file}")


def example_restore_same_version():
    """示例：同版本恢复"""
    print("\n=== 同版本恢复示例 ===")

    restore_engine = RestoreEngine(target_version="1.0.0")
    backup_file = Path("./backups/patients_20240206_120000.json")

    if backup_file.exists():
        restored_data = restore_engine.restore_from_file(backup_file)
        print(f"恢复 {len(restored_data)} 条记录")


if __name__ == "__main__":
    example_backup()
    example_restore_same_version()
