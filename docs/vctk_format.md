# VCTK Dataset Structure

## Directory Layout

```plaintext
VCTK-Corpus-[version]/
├── txt/                        # Text transcriptions
│   ├── p225/                   # Speaker-specific transcripts
│   │   ├── p225_001.txt
│   │   └── ...
│   └── p226/
├── wav[XX]/                    # Audio files at different sampling rates (16/32/48 kHz)
│   ├── p225/                   # Speaker-specific recordings
│   │   ├── p225_001_mic1.flac  # Recordings from microphone 1
│   │   ├── p225_001_mic2.flac  # Recordings from microphone 2
│   │   └── ...
│   └── p226/
└── speaker-info.txt            # Speaker metadata
```

## File Formats

### Text Files (*.txt)

- One utterance per file
- UTF-8 encoded plain text
- Contains only the transcription text
- Filename format: p[speaker_id]_[utterance_number].txt

### Audio Files (*.wav)

- 48kHz sampling rate
- 16-bit PCM encoding
- Mono channel
- Filename format: p[speaker_id]_[utterance_number].wav

### speaker-info.txt

```plaintext
ID | AGE | GENDER | ACCENT | REGION | OTHER_INFO
p225 | 23 | F | English | Southern | ...
p226 | 22 | M | English | Surrey | ...
```

## Naming Convention

- Speaker IDs: p[number] (e.g., p225, p226)
- Files: p[speaker_id]_[utterance_number].[extension]
  - Example: p225_001.wav, p225_001.txt