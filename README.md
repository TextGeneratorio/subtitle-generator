# subtitle-generator
Generate subtitles for youtube videos for free with https://text-generator.io



# Setup

clone this repo

```bash
git clone git@github.com:TextGeneratorio/subtitle-generator.git 
cd subtitle-generator
```

install dependencies

```bash
virtualenv .env
source .env/bin/activate
pip install -r requirements.txt
```


usage

```bash
TEXT_GENERATOR_API_KEY=YOUR_API_KEY_HERE python subtitle_generator.py --video_url "https://www.youtube.com/watch?v=uJgzCQYVv44&ab_channel=LeviTheGiant" --output_file output.srt
```
