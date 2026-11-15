import asyncio
import edge_tts
import base64
import os

os.makedirs('nasa_life_sciences_data/files', exist_ok=True)

# 7 Real 2026 Neural Characters
characters = [
    {
        "id": "case1",
        "name": "Commander Alex Vance (Nominal Baseline)",
        "voice": "en-US-BrianNeural",
        "rate": "+0%",
        "pitch": "-4Hz",
        "text": "Houston, this is Commander Vance on Mars Transit Day 142. Morning mental wellbeing check is green. Circadian entrainment is locked at 94 percent, cognitive reaction tests are sharp. Crew morale remains steady as Earth fades behind us. Ready for scheduled airlock inspection.",
        "file": "nasa_life_sciences_data/files/voice_case1_nominal_vance.mp3"
    },
    {
        "id": "case2",
        "name": "Specialist Elena Chen (Sensory Fatigue)",
        "voice": "en-US-AvaNeural",
        "rate": "-12%",
        "pitch": "-8Hz",
        "text": "Houston... Specialist Chen, Day 180. The cabin fan drone never stops... haven't slept a solid cycle in four days. Mind feels heavy, hard to hold onto the numbers on the navigation checklist. Just... feeling the weight of the dark out here. Standing by for task sequence.",
        "file": "nasa_life_sciences_data/files/voice_case2_fatigue_chen.mp3"
    },
    {
        "id": "case3",
        "name": "Flight Engineer Marco Rossi (EVA Acute Crisis)",
        "voice": "en-US-SteffanNeural",
        "rate": "+18%",
        "pitch": "+22Hz",
        "text": "Flight... Flight, this is Rossi in the airlock! Pulse is spiking... 135... chest is tight! Looking through the helmet visor into the infinite black void... experiencing acute sensory panic! Breathing is shallow, laryngeal strain is high! Requesting immediate 30-second acoustic grounding before hatch egress!",
        "file": "nasa_life_sciences_data/files/voice_case3_crisis_rossi.mp3"
    },
    {
        "id": "lovell",
        "name": "Jim Lovell (Apollo 13 Oral History)",
        "voice": "en-US-GuyNeural",
        "rate": "-5%",
        "pitch": "-6Hz",
        "text": "When the spacecraft service module exploded into total darkness, we realized panic would not improve a single gauge reading. Breathe deeply, focus entirely on the next single valve you can control.",
        "file": "nasa_life_sciences_data/files/heritage_lovell_apollo13.mp3"
    },
    {
        "id": "kinship_emma",
        "name": "Daughter Emma (8yo Child Voice)",
        "voice": "en-US-AnaNeural",
        "rate": "+8%",
        "pitch": "+15Hz",
        "text": "Daddy! Mom's hydrangeas in the backyard are blooming today! Leo and I recorded 10 seconds of the wind chimes and cicadas for you. Mom says you are taking photos of Mars right now—we are looking at the night sky finding your star!",
        "file": "nasa_life_sciences_data/files/kinship_emma.mp3"
    },
    {
        "id": "kinship_sarah",
        "name": "Sarah (Wife Tender Voice)",
        "voice": "en-US-JennyNeural",
        "rate": "-6%",
        "pitch": "-4Hz",
        "text": "Alex, we know you are pushing hard through long shifts. Don't carry the whole mission on your shoulders. I polished that little wooden glider you carved in the garage and hung it in the living room. We are thriving, so proud of you captain!",
        "file": "nasa_life_sciences_data/files/kinship_sarah.mp3"
    },
    {
        "id": "kinship_leo",
        "name": "Son Leo (10yo Boy Voice)",
        "voice": "en-US-ChristopherNeural",
        "rate": "+8%",
        "pitch": "+8Hz",
        "text": "Dad! I built a Mars lander with Lego and tested its heat shield with Mom's hairdryer—it passed! Tonight at 9 PM Houston time, Emma and I will shine our super flashlight toward Mars. Wave back if you are in the Cupola!",
        "file": "nasa_life_sciences_data/files/kinship_leo.mp3"
    }
]

async def generate_all():
    print("Starting generation of 7 ultra-realistic 2026 neural human voices...")
    b64_dict = {}
    for c in characters:
        print(f"Synthesizing [{c['name']}] using {c['voice']}...")
        comm = edge_tts.Communicate(c['text'], c['voice'], rate=c['rate'], pitch=c['pitch'])
        await comm.save(c['file'])
        with open(c['file'], 'rb') as f:
            b64_audio = 'data:audio/mp3;base64,' + base64.b64encode(f.read()).decode('utf-8')
            b64_dict[c['id']] = b64_audio
        print(f"✓ Generated {c['file']} ({os.path.getsize(c['file'])} bytes)")

    # Update astronaut_voices_data.js
    with open('astronaut_voices_data.js', 'w', encoding='utf-8') as f:
        f.write('// Auto-generated 2026 Deep Neural Network Audio Dataset (Ultra-realistic Human Voices)\n')
        f.write('window.ASTRONAUT_AUDIO_B64 = {\n')
        for k, v in b64_dict.items():
            f.write(f'  {k}: \'{v}\',\n')
        f.write('};\n')
    print("✓ Successfully updated astronaut_voices_data.js with all 7 neural voices!")

if __name__ == '__main__':
    asyncio.run(generate_all())
