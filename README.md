# SE-Bridge-TTS

<p align="center">
  <strong>Bridging the Stability-Expressivity Gap</strong><br>
  <span>Synthetic Data Scaling and Preference Alignment for Low-Resource Spoken Language Models</span><br>
  <span>ICML 2026</span>
</p>

<p align="center">
  <a href="https://piedpiperg.github.io/SE-Bridge-TTS/">
    <img alt="Project page" src="https://img.shields.io/badge/Project_Page-Open_Demo-0f766e?style=for-the-badge">
  </a>
  <a href="https://arxiv.org/abs/2605.27383">
    <img alt="arXiv paper" src="https://img.shields.io/badge/Paper-arXiv_2605.27383-b31b1b?style=for-the-badge">
  </a>
  <a href="https://huggingface.co/isabeth/SE-Bridge-TTS">
    <img alt="Hugging Face weights" src="https://img.shields.io/badge/Weights-Hugging_Face-f59e0b?style=for-the-badge">
  </a>
  <a href="https://github.com/piedpiperG/SE-Bridge-TTS">
    <img alt="GitHub repository" src="https://img.shields.io/badge/Code-GitHub-24292f?style=for-the-badge">
  </a>
</p>

<p align="center">
  <img src="assets/figures/dgsa.png" alt="SE-Bridge-TTS DGSA method overview" width="860">
</p>

SE-Bridge-TTS studies a core trade-off in low-resource spoken language modeling: synthetic data improves phonetic stability, but excessive scaling can flatten prosody and speaker expressivity. The project introduces two self-alignment frameworks for expressive Thai and Lao speech synthesis:

- **DGSA**: disentanglement-guided self-alignment for Thai, using prosody-timbre separation to recover expressive speech while preserving stability.
- **TDSC**: temperature-driven self-critique for Lao, using pure-synthetic candidates as pseudo-real anchors when authentic references are scarce.

## Links

| Resource | Link |
| --- | --- |
| Project homepage and full audio browser | https://piedpiperg.github.io/SE-Bridge-TTS/ |
| Paper | https://arxiv.org/abs/2605.27383 |
| Public Thai and Lao weights | https://huggingface.co/isabeth/SE-Bridge-TTS |
| Demo metadata | `assets/data/demo-data.json` |

## Result Snapshot

| Setting | Metric | Result | Note |
| --- | ---: | ---: | --- |
| Thai standard TTS | NMOS | 4.51 | DGSA achieves the strongest naturalness score among tested systems. |
| Lao standard TTS | WER / NMOS | 29.8 / 4.53 | TDSC improves intelligibility and naturalness in a pure-synthetic setting. |
| Thai zero-shot cloning | SIM / SMOS | 0.84 / 4.51 | Higher speaker similarity than the compared commercial baseline. |
| Lao cloning demo | SIM / SMOS | 0.81 / 4.32 | Public release checkpoint should be used with cross-lingual inference. |

## Featured Audio Demos

The full interactive demo browser is on the [project homepage](https://piedpiperg.github.io/SE-Bridge-TTS/#audio-demo). A few representative examples are linked below for quick inspection.

| Demo | What to compare | Audio links |
| --- | --- | --- |
| Thai benchmark | DGSA against commercial and open-source systems on the same Thai text. | [Ours DGSA](assets/audio/benchmarks/thai/ours-dgsa-sample1.wav)<br>[ElevenLabs-v3](assets/audio/benchmarks/thai/elevenlabs-sample1.mp3)<br>[Azure](assets/audio/benchmarks/thai/azure-sample1.wav)<br>[MMS-TTS](assets/audio/benchmarks/thai/mms-sample1.wav) |
| Lao benchmark | TDSC against Lao-capable commercial and open-source systems. | [Ours TDSC](assets/audio/benchmarks/lao/ours-tdsc-sample1.wav)<br>[Google](assets/audio/benchmarks/lao/google-sample1.mp3)<br>[Azure](assets/audio/benchmarks/lao/azure-sample1.wav)<br>[MMS-TTS](assets/audio/benchmarks/lao/mms-sample1.wav) |
| Synthetic erosion | The sweet spot between unstable speech and over-smoothed high-synthetic speech. | [Reference](assets/audio/erosion/en3/reference-en3.wav)<br>[alpha = 0](assets/audio/erosion/en3/alpha-0.wav)<br>[alpha = 50](assets/audio/erosion/en3/alpha-50.wav)<br>[alpha = 80](assets/audio/erosion/en3/alpha-80.wav) |
| DGSA alignment | Baseline alignment versus DGSA on the same Thai text. | [Azure reference](assets/audio/dgsa/azure-sample1.wav)<br>[SFT](assets/audio/dgsa/sft-sample1.wav)<br>[DPO](assets/audio/dgsa/dpo-sample1.wav)<br>[DGSA](assets/audio/dgsa/dgsa-sample1.wav) |
| TDSC self-critique | Lao pure-synthetic self-improvement across SFT, self-training, and TDSC. | [Reference](assets/audio/tdsc/reference-sample1.wav)<br>[Azure](assets/audio/tdsc/azure-sample1.wav)<br>[SFT](assets/audio/tdsc/sft-sample1.wav)<br>[Self-train](assets/audio/tdsc/self-train-sample1.wav)<br>[TDSC](assets/audio/tdsc/tdsc-sample1.wav) |
| Voice cloning | Reference-conditioned synthesis for unseen speakers. | [Thai reference](assets/audio/cloning/thai/reference-th-9804.wav)<br>[Thai ours](assets/audio/cloning/thai/ours-th-9804.wav)<br>[ElevenLabs-v3](assets/audio/cloning/thai/elevenlabs-th-9804.mp3)<br>[Lao reference](assets/audio/cloning/lao/reference-common-voice-lo.wav)<br>[Lao ours](assets/audio/cloning/lao/ours-common-voice-lo.wav) |

## Public Weights

The selected release checkpoints are hosted on Hugging Face:

https://huggingface.co/isabeth/SE-Bridge-TTS

| Checkpoint | Language | Recommended inference |
| --- | --- | --- |
| `thai_tts.pt` | Thai | Zero-shot inference with CosyVoice2. |
| `lao_tts.pt` | Lao | Cross-lingual inference only with CosyVoice2. |

The Hugging Face model card includes the current CosyVoice2 loading example. The release package is sanitized and intentionally omits internal server paths, private data paths, and per-stage checkpoint construction details.

## Repository Layout

- `index.html`: academic project homepage and selected audio demo browser.
- `assets/data/demo-data.json`: paper metadata, headline results, figure references, and audio sample lists.
- `assets/audio/`: curated benchmark, cloning, synthetic erosion, DGSA, and TDSC audio examples.
- `assets/figures/`: DGSA and TDSC method diagrams.
- `tests/`: lightweight static-site checks for required sections and asset references.

## Citation

```bibtex
@inproceedings{geng2026bridging,
  title = {Bridging the Stability-Expressivity Gap: Synthetic Data Scaling and Preference Alignment for Low-Resource Spoken Language Models},
  author = {Geng, Yizhong and Li, Yanliang and Yang, Jinghan and Jiang, Tianhan and An, Boxun and Li, Ya and Shen, Xiaoyu},
  booktitle = {Proceedings of the 43rd International Conference on Machine Learning},
  year = {2026}
}
```

## Status

Project code will be added here later.
