# CommonVoice Dataset Structure

## Directory Layout

```plaintext
cv-corpus-[version]/[lang]/
├── clips/                      # Audio clip MP3 files
├── clip_durations.tsv          # Audio duration information
├── validated.tsv               # Verified audio samples
├── invalidated.tsv             # Invalid/rejected samples
├── train.tsv                   # Training dataset split
├── dev.tsv                     # Validation dataset split  
├── test.tsv                    # Testing dataset split
├── other.tsv                   # Additional valid samples
├── reported.tsv                # Flagged content
├── validated_sentences.tsv     # Verified sentence prompts
└── unvalidated_sentences.tsv   # Pending sentence prompts
```

## File Formats

### clip_durations.tsv

```plaintext
clip                           duration[ms]
common_voice_th_41859605.mp3  2448
```

### validated.tsv / invalidated.tsv / train.tsv / dev.tsv / test.tsv / other.tsv

```tsv
client_id | path | sentence_id | sentence | sentence_domain | up_votes | down_votes | age | gender | accents | variant | locale | segment
```

### reported.tsv

```tsv
sentence_id | sentence | locale | reason
```

### validated_sentences.tsv

```tsv
sentence_id | sentence | sentence_domain | source | is_used | clips_count
```

### unvalidated_sentences.tsv

```tsv
sentence_id | sentence | sentence_domain | source
```

### Naming Convention

Audio files: `common_voice_[lang]_[id].mp3`