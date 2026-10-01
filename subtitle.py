def format_timestamp(
    seconds
):

    milliseconds = int(
        round(
            seconds * 1000
        )
    )

    hours = (
        milliseconds //
        3600000
    )

    milliseconds %= 3600000

    minutes = (
        milliseconds //
        60000
    )

    milliseconds %= 60000

    seconds_value = (
        milliseconds //
        1000
    )

    milliseconds %= 1000

    return (
        f"{hours:02d}:"
        f"{minutes:02d}:"
        f"{seconds_value:02d},"
        f"{milliseconds:03d}"
    )


def create_srt(
    segments,
    output_path
):

    with open(
        output_path,
        "w",
        encoding="utf-8"
    ) as file:

        for index, segment in enumerate(
            segments,
            start=1
        ):

            start = format_timestamp(
                segment["start"]
            )

            end = format_timestamp(
                segment["end"]
            )

            text = (
                segment.get(
                    "translated_text",
                    segment.get(
                        "text",
                        ""
                    )
                )
            )

            file.write(
                f"{index}\n"
            )

            file.write(
                f"{start} --> {end}\n"
            )

            file.write(
                f"{text.strip()}\n\n"
            )


def create_translated_srt(
    segments,
    output_path
):

    create_srt(
        segments,
        output_path
    )
