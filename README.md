# Medical Data Version-Aware Backup and Recovery System

## Project Overview

This repository contains the implementation code for the paper "Schema-Aware Version Control for Medical Database Backup and Recovery Using Declarative Transformation Rules".

## Key Features

- **Declarative Schema Versioning**: JSON-based schema definitions separate from code
- **Automatic Field Mapping**: Three-phase algorithm generates 87% of transformation rules automatically
- **Differential Backup Strategy**: 58% storage reduction compared to traditional full backups
- **Cross-Version Validation**: Multi-phase pipeline with transactional rollback

## Experimental Results

- Storage space reduction: 58% (with GZIP compression)
- Recovery accuracy: 100% across all version paths
- Maintenance cost reduction: 85% (from 40 hours to 6 hours per release)
- Production deployment: 18 months, 500+ operations, zero schema failures

## Directory Structure

```
BackupRestore4Version/
├── code/                    # Implementation code
│   ├── src/                # Source code
│   │   ├── schema_manager.py    # Schema version management
│   │   ├── mapper.py            # Automatic field mapping (Algorithm 1)
│   │   ├── backup_engine.py     # Differential backup engine
│   │   └── restore_engine.py    # Cross-version restore engine
│   ├── examples/           # Usage examples
│   │   ├── basic_usage.py
│   │   └── generate_synthetic_data.py
│   └── data/               # Synthetic test data
├── paper_20260211_210111.tex    # Research paper (LaTeX source)
├── paper_20260211_210111.pdf    # Research paper (PDF)
└── README.md              # This file
```

## Getting Started

See the code/README.md for detailed usage instructions.

## Citation

If you use this code in your research, please cite:

```
@article{backuprestore2026,
  title={Schema-Aware Version Control for Medical Database Backup and Recovery Using Declarative Transformation Rules},
  author={Software Engineer},
  journal={Scientific Reports},
  year={2026}
}
```

## License

This project is maintained by United Imaging Healthcare.
