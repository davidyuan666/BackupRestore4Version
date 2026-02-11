"""
生成合成医疗数据用于实验
Generate synthetic medical data for experiments
"""
import random
import json
from datetime import datetime, timedelta
from pathlib import Path


def generate_patient_demographics(count: int) -> list:
    """生成患者人口统计数据"""
    patients = []
    for i in range(count):
        patient = {
            'patient_id': f'P{i:06d}',
            'name': f'Patient_{i}',
            'age': random.randint(18, 90),
            'gender': random.choice(['M', 'F']),
            'blood_type': random.choice(['A+', 'A-', 'B+', 'B-', 'O+', 'O-', 'AB+', 'AB-']),
            'phone': f'+86-{random.randint(13000000000, 18999999999)}',
            'address': f'Address_{i}',
            'created_at': (datetime.now() - timedelta(days=random.randint(0, 365))).isoformat()
        }
        patients.append(patient)
    return patients


def generate_imaging_studies(count: int, patient_count: int) -> list:
    """生成影像检查数据"""
    studies = []
    modalities = ['CT', 'MRI', 'X-Ray', 'Ultrasound', 'PET']
    body_parts = ['Head', 'Chest', 'Abdomen', 'Spine', 'Extremity']

    for i in range(count):
        study = {
            'study_id': f'S{i:08d}',
            'patient_id': f'P{random.randint(0, patient_count-1):06d}',
            'modality': random.choice(modalities),
            'body_part': random.choice(body_parts),
            'study_date': (datetime.now() - timedelta(days=random.randint(0, 180))).isoformat(),
            'description': f'Study_{i}',
            'status': random.choice(['Completed', 'In Progress', 'Pending'])
        }
        studies.append(study)
    return studies


def generate_dicom_metadata(count: int, study_count: int) -> list:
    """生成DICOM元数据"""
    metadata = []
    for i in range(count):
        meta = {
            'instance_id': f'I{i:08d}',
            'study_id': f'S{random.randint(0, study_count-1):08d}',
            'series_number': random.randint(1, 10),
            'instance_number': random.randint(1, 100),
            'slice_thickness': round(random.uniform(0.5, 5.0), 2),
            'pixel_spacing': f'{random.uniform(0.1, 1.0):.3f}',
            'rows': random.choice([512, 1024, 2048]),
            'columns': random.choice([512, 1024, 2048])
        }
        metadata.append(meta)
    return metadata


def main():
    """主函数"""
    output_dir = Path(__file__).parent.parent / 'data' / 'synthetic'
    output_dir.mkdir(parents=True, exist_ok=True)

    print("Generating synthetic medical data...")

    # 生成数据
    patients = generate_patient_demographics(5000)
    studies = generate_imaging_studies(15000, 5000)
    dicom_meta = generate_dicom_metadata(30000, 15000)

    # 保存数据
    with open(output_dir / 'patients.json', 'w') as f:
        json.dump(patients, f, indent=2)

    with open(output_dir / 'studies.json', 'w') as f:
        json.dump(studies, f, indent=2)

    with open(output_dir / 'dicom_metadata.json', 'w') as f:
        json.dump(dicom_meta, f, indent=2)

    print(f"Generated {len(patients)} patients")
    print(f"Generated {len(studies)} studies")
    print(f"Generated {len(dicom_meta)} DICOM instances")
    print(f"Data saved to {output_dir}")


if __name__ == '__main__':
    main()
