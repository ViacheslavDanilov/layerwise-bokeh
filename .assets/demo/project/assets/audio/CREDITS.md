# Sound credits

Every sound in the video, where it came from, and the license it is used under.

| File | Source | License |
|---|---|---|
| `music.mp3` | The voice-over and the music bed, mixed: the voice is synthesized with Kokoro (`af_heart`), the bed is `bgm0.wav` | Voice: Apache 2.0. Bed: CC BY-NC 4.0 (see below) |
| `bgm0.wav` | A 30 s clip generated with MusicGen (`facebook/musicgen-small`); `music.mp3`'s bed is four copies of it | Weights: [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/) |
| `click.mp3` | `click-soft.mp3` from the HyperFrames sound-effect bundle | [Pixabay Content License](https://pixabay.com/service/license-summary/) |
| `whoosh-a.mp3` | `whoosh.mp3` from the HyperFrames sound-effect bundle | [Pixabay Content License](https://pixabay.com/service/license-summary/) |
| `whoosh-b.mp3` | `whoosh-a.mp3` pitched down about three semitones | [Pixabay Content License](https://pixabay.com/service/license-summary/) |

## Voice

The voice is `af_heart` of [Kokoro-82M](https://huggingface.co/hexgrad/Kokoro-82M), run
through [kokoro-onnx](https://github.com/thewh1teagle/kokoro-onnx) by the `hyperframes tts`
command. The model card lists the license as Apache 2.0 and says the model was trained on
permissive and non-copyrighted audio. It names two CC BY datasets in the training data of
v1.0: Koniwa `tnc` (CC BY 3.0) and SIWIS (CC BY 4.0). kokoro-onnx's own code is MIT, and its
README gives the Kokoro model as Apache 2.0. The files used are `kokoro-v1.0.onnx` and
`voices-v1.0.bin` from the kokoro-onnx release, which `../../tts.py` checks by SHA-256. The
script is `../../voice/lines.tsv`.

## Music

The bed is a clip generated with MusicGen, the model of Copet et al., "Simple and
Controllable Music Generation" (arXiv 2306.05284), in its `facebook/musicgen-small`
weights. The model card says the code is released under MIT and the model weights under
CC BY-NC 4.0, a license that does not allow commercial use. The data this repository
describes is for non-commercial research as well, and this video belongs to it. Any use of
the sound outside that is not covered here.

`bgm0.wav` is the 29.94 s clip, 32 kHz mono, SHA-256
`519fe0a6a0ad3b9935a0a4b3045689e9a95b62f8ff4687cd39cb9c46a4f00cf5`. `music.mp3` is made from
it in five steps (the commands are in `../../README.md`):

1. four copies are joined with 3 s crossfades, 110.76 s;
2. the bed is slowed to 95 % of its speed, 116.6 s;
3. it is brought to -25 LUFS and ducked by the voice, which stands about 10.6 dB over it on
   average, with a 1.2 s fade in and a fade out that ends 0.25 s before the film's end;
4. the voice, brought to -18 LUFS on its own, is added and the sum set so that the file
   measures -18 LUFS with the click and the whooshes over it;
5. the mix is encoded as MP3 at 192 kbit/s.

## Sound effects

The click and the whoosh come from the sound-effect bundle of HyperFrames' `media-use`
skill (`audio/assets/sfx`). The bundle credits all its sounds to
[Pixabay](https://pixabay.com/sound-effects/) under the Pixabay Content License, but
neither the bundle nor the files name the Pixabay page or the author of each sound, so they
cannot be traced further.

The license allows use without attribution and allows modifying the content, which is how
`whoosh-b.mp3` was made. It does not allow distributing the content on a standalone basis.
These files are here only as parts of this video's project.
