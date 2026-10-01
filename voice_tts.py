import asyncio
from pathlib import Path

import edge_tts

from voice_profiles import get_voice


async def generate_voice(
    text,
    language,
    gender,
    output_path,
    rate="+0%",
    pitch="+0Hz",
    volume="+0%"
):

    voice = get_voice(
        language,
        gender
    )

    output_path = Path(output_path)

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    communicate = edge_tts.Communicate(
        text=text,
        voice=voice,
        rate=rate,
        pitch=pitch,
        volume=volume
    )

    await communicate.save(
        str(output_path)
    )

    if not output_path.exists():

        raise RuntimeError(
            "Voice generation failed."
        )

    if output_path.stat().st_size == 0:

        raise RuntimeError(
            "Generated audio is empty."
        )

    return output_path


def generate_voice_sync(
    text,
    language,
    gender,
    output_path,
    rate="+0%",
    pitch="+0Hz",
    volume="+0%"
):

    return asyncio.run(
        generate_voice(
            text=text,
            language=language,
            gender=gender,
            output_path=output_path,
            rate=rate,
            pitch=pitch,
            volume=volume
        )
    )


async def get_available_voices():

    return await edge_tts.list_voices()
