# Speech Dataset Format Converter

A toolkit for converting between different speech dataset formats and processing audio files.

## Project Structure

```plaintext
.
├── analysis/               # Dataset analysis notebooks
├── converter/              # Format conversion scripts
├── data/
│   ├── converted/          # Output directory for converted datasets
│   └── raw/                # Input directory for original datasets
├── docs/                   # Dataset format documentation
├── utils/                  # Utility scripts
│   └── trimmer.py          # Audio silence trimming utility
└── README.md               # Project README
```

## Supported Format Conversions

| From \ To                                 | [VCTK](docs/VCTK_format.md) | [CommonVoice](docs/CommonVoice_format.md) | [TSync2](docs/TSync2_format.md) | [GigaSpeech](docs/GigaSpeech_format.md) |
| ----------------------------------------- | --------------------------- | ----------------------------------------- | ------------------------------ | -------------------------------------- |
| [VCTK](docs/vctk_format.md)               | -                           |                                           |                                |                                      |
| [CommonVoice](docs/CommonVoice_format.md) | ✓                           | -                                         |                                |                                      |
| [TSync2](docs/TSync2_format.md)           | ✓                           |                                           | -                              | ✓                                    |
| [GigaSpeech](docs/GigaSpeech_format.md)   |                             |                                           |                                | -                                    |


## Features

- Conversion between supported dataset formats
- Dataset statistics and analysis tools
- Audio processing utilities including silence trimming

## Requirements

- Python 3.9+
- pandas
- tqdm
- pydub
- shutil
- TTS

## Usage

### Dataset Conversion

1. Place source dataset in `data/raw/`
2. Run analysis notebook to examine dataset statistics
3. Execute conversion script for desired format
4. Access converted dataset in `data/converted/`

### Audio Silence Trimming

The `trimmer.py` utility removes silence from the beginning and end of audio files:

```bash
python utils/trimmer.py /path/to/audio/folder
```

Features:

- Recursively processes all audio files in the input directory
- Supports multiple audio formats (MP3, WAV, OGG, FLAC, M4A, WMA)
- Preserves directory structure in output
- Shows progress bar and processing statistics
- Outputs trimmed files in WAV format

Output will be created in a new directory with '_silence_trimmed' suffix:

```plaintext
input_folder/ → input_folder_silence_trimmed/
```

## Contributing

To add support for new dataset formats:

1. Add format documentation in `docs/`
2. Create conversion script in `converter/`
3. Update analysis tools as needed
