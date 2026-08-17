---
name: ai-music-generation
description: "AI music creation: songwriting craft, Suno/LMU prompt engineering, local model generation (HeartMuLa), and audio analysis (spectrograms, features)."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [music, audio, ai-music, songwriting, suno, heartmula, spectrogram, generation, lyrics]
---

# AI Music Generation

Everything for creating music with AI: songwriting craft, prompt engineering for AI music platforms, local model generation, and audio analysis.

## When to Use

- Writing song lyrics or adapting existing songs
- Generating music with Suno, HeartMuLa, or other AI music tools
- Analyzing audio files (spectrograms, features, visualization)
- Prompt engineering for AI music generation

---

## 1. Songwriting Craft

### Song Structure

```
ABABCB  Verse/Chorus/Verse/Chorus/Bridge/Chorus    (most pop/rock)
AABA    Verse/Verse/Bridge/Verse                    (jazz standards)
ABAB    Verse/Chorus alternating                    (simple, direct)
AAA     Verse/Verse/Verse (strophic)                (folk, storytelling)
```

Building blocks: Intro, Verse, Pre-Chorus, Chorus, Bridge, Outro. Mix as needed.

### Rhyme Types (tight to loose)

- Perfect: lean/mean
- Family: crate/braid
- Assonance: had/glass (same vowels)
- Consonance: scene/when
- Near/slant: enough to suggest connection

Mix them. All perfect rhymes sound nursery; all slant rhymes sound lazy.

### Emotional Arc

```
Intro: 2-3  |  Verse: 5-6  |  Pre-Chorus: 7
Chorus: 8-9  |  Bridge: varies  |  Final Chorus: 9-10
```

**The most powerful trick: CONTRAST.** Whisper before a scream. Sparse before dense. Silence is an instrument.

### Lyrics That Work

- **Show, don't tell:** "Your hoodie's still on the hook" > "I was sad"
- **The hook:** The line people remember. Place where it lands hardest.
- **Prosody:** Lyrics and music supporting each other. Stable feelings → settled melodies. Unstable → wandering melodies.

---

## 2. AI Music Prompt Engineering (Suno and similar)

### Style Description Formula

`Genre + Mood + Era + Instruments + Vocal Style + Production + Dynamics`

```
BAD:  "sad rock song"
GOOD: "Cinematic orchestral spy thriller, 1960s Cold War era, smoky
       sultry female vocalist, big band jazz, brass section with
       trumpets and french horns, sweeping strings, minor key,
       vintage analog warmth"
```

**Describe the JOURNEY, not just the genre.**

### Metatags (in [brackets] inside lyrics)

**Structure:** [Intro] [Verse] [Chorus] [Bridge] [Instrumental] [Outro]

**Performance:** [Whispered] [Belted] [Falsetto] [Powerful] [Raspy] [Staccato]

**Dynamics:** [High Energy] [Low Energy] [Building Energy] [Explosive]

**Atmosphere:** [Melancholic] [Euphoric] [Nostalgic] [Aggressive] [Dreamy]

Keep 5-8 tags per section max. Don't contradict ([Calm] + [Aggressive]).

### Phonetic Tricks for AI Singers

- Spell words as they SOUND: "through" → "thru"
- Hyphenate syllables: "Re-search", "bio-engineering"
- ALL CAPS = louder. Vowel extension: "lo-o-o-ove" = sustained.
- Spell out numbers: "24/7" → "twenty four seven"
- Space acronyms: "AI" → "A I"

### Parody and Adaptation

- Map original structure: syllable count, rhyme scheme, stress pattern
- Match stressed syllables to same beats
- On held notes, match the VOWEL SOUND
- Keep some original lines for recognizability

---

## 3. HeartMuLa — Local AI Music Generation

Open-source music foundation model (Apache-2.0). Generates full songs from lyrics + tags.

### Hardware

- **Minimum:** 8GB VRAM with `--lazy_load true`
- **Recommended:** 16GB+ VRAM
- **Multi-GPU:** `--mula_device cuda:0 --codec_device cuda:1`
- **CPU:** Possible but extremely slow (30-60+ min per song)

### Install

```bash
git clone https://github.com/HeartMuLa/heartlib.git && cd heartlib
uv venv --python 3.10 .venv && . .venv/bin/activate
uv pip install -e .
uv pip install --upgrade datasets transformers  # fix dep conflicts
```

### Download Models

```bash
hf download --local-dir './ckpt' 'HeartMuLa/HeartMuLaGen'
hf download --local-dir './ckpt/HeartMuLa-oss-3B' 'HeartMuLa/HeartMuLa-oss-3B-happy-new-year'
hf download --local-dir './ckpt/HeartCodec-oss' 'HeartMuLa/HeartCodec-oss-20260123'
```

### Generate

```bash
python ./examples/run_music_generation.py \
  --model_path=./ckpt --version="3B" \
  --lyrics="./assets/lyrics.txt" --tags="./assets/tags.txt" \
  --save_path="./assets/output.mp3" --lazy_load true
```

**Tags:** comma-separated, no spaces: `piano,happy,wedding,synthesizer`

**Lyrics:** Use structural tags: [Intro] [Verse] [Chorus] [Bridge] [Outro]

**Output:** MP3, 48kHz stereo, 128kbps. RTF ≈ 1.0 (4-min song ≈ 4 min to generate).

### Pitfalls

- Do NOT use bf16 for HeartCodec — degrades audio quality (use fp32)
- Tags may be ignored (known issue) — lyrics tend to dominate
- Triton not available on macOS — Linux/CUDA only
- Requires source code patches for transformers 5.x compatibility

---

## 4. Audio Analysis (songsee)

Generate spectrograms and audio feature visualizations.

### Install

```bash
go install github.com/steipete/songsee/cmd/songsee@latest
```

### Usage

```bash
songsee track.mp3                                          # Basic spectrogram
songsee track.mp3 --viz spectrogram,mel,chroma,hpss       # Multi-panel grid
songsee track.mp3 --start 12.5 --duration 8 -o slice.jpg  # Time slice
```

### Visualization Types

| Type | Description |
|------|-------------|
| `spectrogram` | Standard frequency spectrogram |
| `mel` | Mel-scaled spectrogram |
| `chroma` | Pitch class distribution |
| `hpss` | Harmonic/percussive separation |
| `selfsim` | Self-similarity matrix |
| `loudness` | Loudness over time |
| `tempogram` | Tempo estimation |
| `mfcc` | Mel-frequency cepstral coefficients |
| `flux` | Spectral flux (onset detection) |

Output images can be analyzed with `vision_analyze` for automated audio analysis.
