# LJSpeech Dataset Structure

## Directory Layout

```plaintext
LJSpeech-1.1/
├── wavs/                      # Audio files (22050 Hz, 16-bit)
│   ├── LJ001-0001.wav
│   ├── LJ001-0002.wav
│   └── ...
└── metadata.csv               # Transcription metadata
```

## File Formats

### metadata.csv

The metadata file contains three fields separated by pipe (|) characters:

```csv
<file_id>|<transcription>|<normalized_transcription>
```

Example:

```csv
LJ001-0001|Printing, in the only sense with which we are at present concerned, differs from most if not from all the arts and crafts represented in the Exhibition|Printing, in the only sense with which we are at present concerned, differs from most if not from all the arts and crafts represented in the Exhibition
LJ001-0002|in being comparatively modern.|in being comparatively modern.
LJ001-0003|For although the Chinese took impressions from wood blocks engraved in relief for centuries before the woodcutters of the Netherlands, by a similar process|For although the Chinese took impressions from wood blocks engraved in relief for centuries before the woodcutters of the Netherlands, by a similar process
```

Fields:

- **file_id**: Unique identifier corresponding to the audio filename (without .wav extension)
- **transcription**: Original text transcription with capitalization and punctuation
- **normalized_transcription**: Normalized version of the transcription (all lowercase, some punctuation normalization)

### Audio Files (*.wav)

- 22050 Hz sample rate
- 16-bit PCM encoding
- Mono channel
- Approximately 13 hours of speech from a single female speaker

## Naming Convention

- Audio files: LJ[chapter]_[sentence].wav
  - [chapter]: Three-digit chapter number (e.g., 001)
  - [sentence]: Four-digit sentence number within chapter (e.g., 0001)
  - Example: LJ001-0001.wav
