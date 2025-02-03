# Tsync2 Dataset Structure

## Directory Layout

```plaintext
Tsync2/
├── wrd_ph/                     # Text transcriptions
│   ├── tsync2_noon_0_250.txt
│   └── ...
└── wav/                        # Audio files at 44.1k sample rates
    ├── tsync2_noon_0_250.wav
    └── ...
```

## File Formats

### Text Files (*.txt)

- One utterance per file
- UTF-8 encoded plain text
- Each file contains 3 lines in the following format:
  1. Word-level transcription with pipe (|) delimiters
  2. Word-level transcription with pipe (|) delimiters and spaces
  3. Phonetic representation with pipe (|) delimiters

Example:

```plaintext
มอบ|วัด|พระ|บาท|น้ำพุ|สร้าง|เตา|เผา|เอดส์|
มอบ|วัด|พระ|บาท|น้ำพุ|สร้าง|เตา|เผา|เอดส์
m-@@-p^-2|*w-a-t^-3|*phr-a-z^-3|*b-aa-t^-1|*n-a-m^-3|ph-u-z^-3|*s-aa-ng^-2|*t-a-w^-0|*ph-a-w^-4|*z-ee-t^-1|*
```

- Filename format: tsync2_noon_[Group]_[Number_in_group].txt

### Audio Files (*.wav)

- 44.1kHz sample rate
- Mono channel
- Filename format: tsync2_noon_[Group]_[Number_in_group].wav

## Naming Convention

- Files: tsync2_noon_[Group]_[Number_in_group].[extension]
  - Example: tsync2_noon_0_250.wav, tsync2_noon_0_250.txt
