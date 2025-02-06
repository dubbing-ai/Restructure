# Speech Dataset Format Converter

A toolkit for converting between different speech dataset formats and processing audio files.

## Project Structure

```plaintext
.
├── analysis/                     # Dataset analysis notebooks
│   ├── commonvoice-analysis      # Thai CommonVoice statistics 
│   └── Tsync2-analysis           # TSync2 dataset analysis
├── converter/                    # Format conversion scripts
│   ├── commonvoice-to-vctk       # Convert CommonVoice to VCTK format
│   ├── TSync2-to-gigaspeech      # Convert TSync2 to GigaSpeech format
│   └── TSync2-to-vctk            # Convert TSync2 to VCTK format
│   └── TSync2-to-vctk-ph         # Convert TSync2 to VCTK format with phonemes as text
├── data/
│   ├── converted/                # Output directory for converted datasets
│   └── raw/                      # Input directory for original datasets
├── docs/                         # Dataset format documentation
│   ├── commonvoice_format.md
│   ├── GigaSpeech_format.md
│   ├── TSync2_format.md
│   └── vctk_format.md
└── utils/                        # Utility scripts
    ├── audio_util.py             # Audio processing utilities
    └── file_util.py              # File handling utilities
```

## Supported Format Conversions

| From \ To                                 | [VCTK](docs/VCTK_format.md) | [CommonVoice](docs/CommonVoice_format.md) | [TSync2](docs/TSync2_format.md) | [GigaSpeech](docs/GigaSpeech_format.md) |
| ----------------------------------------- | --------------------------- | ----------------------------------------- | ------------------------------- | --------------------------------------- |
| [VCTK](docs/vctk_format.md)               | -                           |                                           |                                 |                                         |
| [CommonVoice](docs/CommonVoice_format.md) | ✓                           | -                                         |                                 |                                         |
| [TSync2](docs/TSync2_format.md)           | ✓                           |                                           | -                               | ✓                                       |
| [GigaSpeech](docs/GigaSpeech_format.md)   |                             |                                           |                                 | -                                       |

## Features

### Audio Processing

- Audio format conversion (WAV/MP3 to FLAC)
- Resampling to different sample rates
- Silence trimming using Voice Activity Detection (VAD)
- Volume normalization
- Multi-threaded processing support

### Dataset Conversion

Convert between the following formats:

- CommonVoice → VCTK
- TSync2 → VCTK
- TSync2 → GigaSpeech

### Analysis Tools

- Audio duration statistics
- Speaker distribution analysis
- Text analysis and character set extraction
- Quality assessment utilities

### Python Dependencies

- Python 3.9+
- pandas
- tqdm
- pydub
- shutil
- TTS
- torch
- datasets
- soundfile
= python-dotenv
- huggingface_hub
- ffmpeg-normalize
- [transliterate](https://github.com/dubbing-ai/Transliterate.git)

### External Tools

- ffmpeg (for audio processing)

## Usage

### Dataset Conversion

1. Place source dataset in `data/raw/`
2. Run analysis notebook to examine dataset statistics
3. Execute conversion script for desired format
4. Access converted dataset in `data/converted/`

## Contributing

To add support for new dataset formats:

1. Add format documentation in `docs/`
2. Create conversion script in `converter/`
3. Update analysis tools as needed
