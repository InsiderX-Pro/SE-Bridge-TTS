# FLEURS Lao/Thai Multilingual Prompt Evaluation

This directory publishes the protocol and compact result tables for a
reproducible FLEURS evaluation of SE-Bridge-TTS against three recent
open multilingual speech synthesis systems:

- Higgs Audio v3
- OmniVoice
- X-Voice Stage1
- SE-Bridge-TTS

The benchmark was run on 2026-06-11. It evaluates whether public
SE-Bridge-TTS weights can synthesize Lao and Thai speech while preserving
speaker identity from Lao, Thai, Chinese, or English reference prompts.

## Why This Evaluation

SE-Bridge-TTS was developed before these newer open multilingual TTS
systems were released. This benchmark checks whether the released
Thai/Lao checkpoints remain competitive under a shared modern
zero-shot/prompted synthesis protocol. The key result is that
SE-Bridge-TTS reaches the best overall calibrated accuracy in the
Chinese/English prompt -> Lao/Thai target setting while remaining
competitive on speaker similarity.

## Files

| File | Description |
| --- | --- |
| `results.json` | Machine-readable benchmark metadata and compact results. |
| `summary_same_language.csv` | Lao->Lao and Thai->Thai prompt results by model/language. |
| `summary_cross_prompt_by_model.csv` | Chinese/English prompt -> Lao/Thai target aggregate by model. |
| `summary_cross_prompt_by_direction.csv` | Direction-level Chinese/English prompt results, including unsupported directions. |
| `scripts/render_results.py` | Prints Markdown tables from `results.json`. |

## Dataset Protocol

The source data is the FLEURS test split.

Main target set:

- Target languages: Lao (`lo_la`) and Thai (`th_th`).
- Paired sentence IDs: 255 shared Lao/Thai sentence IDs.
- Target samples: 255 Lao + 255 Thai = 510 target utterances.
- Target selection: for each language and shared sentence ID, choose the
  utterance whose duration is closest to 5 seconds.
- Target duration filter: 1.5 to 30 seconds.

Same-language prompt setting:

- Directions: Lao->Lao and Thai->Thai.
- Prompt language matches target language.
- Prompt must use a different sentence ID from the target.
- Prompt duration filter: 3 to 8 seconds.
- Prefer same-gender prompts when available.
- Prompt reuse is balanced deterministically.

Cross-language prompt setting:

- Directions: Chinese->Lao, English->Lao, Chinese->Thai, English->Thai.
- The target text is still Lao or Thai.
- Chinese and English are used only as reference prompt languages.
- Each direction has 255 samples, so models with full Lao/Thai support
  run 1,020 generated samples.

## Deterministic Prompt Selection

For same-language prompts, sort candidates by:

```text
(current_reuse_count, sha256(target_uid + "::" + prompt_uid), prompt_uid)
```

For Chinese/English cross-language prompts, sort candidates by:

```text
(current_reuse_count,
 sha256(prompt_lang + "::" + target_lang + "::" + pair_id + "::" + target_uid + "::" + prompt_uid),
 prompt_uid)
```

The first candidate after sorting is selected. This avoids runtime
randomness and prevents a small number of prompts from dominating the
benchmark.

## Reproduction Checklist

1. Prepare a FLEURS test manifest JSONL with one row per utterance. Each
   row should contain at least:

   ```json
   {
     "language": "lo_la",
     "uid": "fleurs-utterance-id",
     "sentence_id": "123",
     "duration_seconds": 5.0,
     "gender": "MALE",
     "text": "transcript",
     "audio_path": "/path/to/audio.wav"
   }
   ```

2. Construct the same-language and Chinese/English prompt manifests
   using the selection rules above.
3. Run each model with identical `target_text`, `prompt_audio`, and
   `prompt_text` for each sample. Store one generation manifest per
   model with `sample_id`, `output`, `ok`, `error`, and the copied sample
   metadata.
4. Transcribe generated audio and original FLEURS target audio. Use
   Dolphin small `lo-LA` for Lao and faster-whisper large-v3 for Thai.
5. Compute CER, ground-truth CER, calibrated CER, and speaker similarity
   against the prompt audio.
6. Aggregate by model, target language, and clone direction. Missing
   language support should be reported as coverage failure and excluded
   from quality means.

## Model Input Protocol

Every model receives the same fields for each sample:

- `target_text`
- `prompt_audio`
- `prompt_text`
- `target_language_id`
- `prompt_language_id`

SE-Bridge-TTS uses the released Hugging Face checkpoints:

- `thai_tts.pt`
- `lao_tts.pt`

For the Chinese/English prompt setting, SE-Bridge-TTS uses the
CosyVoice2 cross-lingual inference API for both target languages.

X-Voice Stage1 did not support Lao in the evaluated project language
table. Lao generations are therefore reported as coverage failures and
are not converted into artificial zero-quality samples.

## Metrics

Only the public result tables in this repository report:

- **Accuracy:** `1 - calibrated_cer_mean`
- **Speaker similarity:** cosine similarity from
  `speechbrain/spkrec-ecapa-voxceleb`

The calibrated CER is:

```text
calibrated_cer = max(0, generated_cer - ground_truth_cer)
```

This subtracts the ASR error observed on the original FLEURS target
audio, so the reported accuracy better reflects the degradation caused
by synthesis rather than the recognizer's baseline error.

ASR configuration used for CER:

| Language | ASR |
| --- | --- |
| Lao | Dolphin small `lo-LA` |
| Thai | faster-whisper large-v3 |

Speaker similarity compares the generated audio against the per-sample
prompt audio. In the cross-language prompt setting, this means generated
Lao/Thai speech is compared to the Chinese or English reference speaker.

Latency, RTF, and GPU memory were measured in the internal run but are
not reported here because this release focuses on synthesis quality and
speaker preservation.

## Published Result Tables

Generate the Markdown tables used for public reporting:

```bash
python3 evaluation/fleurs-lo-th-255pair/scripts/render_results.py
```

The most compact comparison is the Chinese/English prompt -> Lao/Thai
aggregate:

| Model | Supported samples | Accuracy | Speaker similarity |
| --- | ---: | ---: | ---: |
| Higgs Audio v3 | 1020/1020 | 78.2% | 0.520 |
| OmniVoice | 1020/1020 | 75.9% | 0.645 |
| SE-Bridge-TTS | 1020/1020 | **83.4%** | 0.593 |
| X-Voice Stage1 | 510/1020 | 53.7% | 0.361 |

Unsupported languages are shown in the coverage denominator but are not
included in quality averages.
