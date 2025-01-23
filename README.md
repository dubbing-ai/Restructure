# Speech Dataset Format Converter

A toolkit for converting between different speech dataset formats.

## Project Structure

```plaintext
.
├── analysis/               # Dataset analysis notebooks
├── converter/              # Format conversion scripts
├── data/
│   ├── converted/          # Output directory for converted datasets
│   └── raw/                # Input directory for original datasets
├── docs/                   # Dataset format documentation
└── README.md               # Project README
```

## Supported Format Conversions

| From \ To                                 | [VCTK](docs/vctk_format.md) | [CommonVoice](docs/commonvoice_format.md) |
| ----------------------------------------- | --------------------------- | ----------------------------------------- |
| [VCTK](docs/vctk_format.md)               | -                           |                                           |
| [CommonVoice](docs/commonvoice_format.md) | ✓                           | -                                         |

## Features

- Conversion between supported dataset formats
- Dataset statistics and analysis tools

## Requirements

- Python 3.9+
- pandas
- tqdm
- shutil

## Usage

1. Place source dataset in `data/raw/`
2. Run analysis notebook to examine dataset statistics
3. Execute conversion script for desired format
4. Access converted dataset in `data/converted/`

## Contributing

To add support for new dataset formats:

1. Add format documentation in `docs/`
2. Create conversion script in `converter/`
3. Update analysis tools as needed
