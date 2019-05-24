V_PAD = '\n\n'
H_PAD = '     '


def title_fmt(title):
    return f'<|endoftext|>\n<|title|>{title}<|title|>\n\n\n'


def output_fmt(text):
    padded = text.replace('\n', f'\n{H_PAD}')
    return padded.replace("<|endoftext|>", f"{'=' * 80}{V_PAD}").replace("<|title|>", "")


def get_output(text, title=None, sample=None):
    start = V_PAD + "=" * 40 + " SAMPLE " + str(sample) + " " + "=" * 40 + V_PAD if sample is not None else ''

    if title:
        start += f'{H_PAD}{title}\n\n\n\n'

    return f'{V_PAD}{"=" * 80}{V_PAD}{start}' + output_fmt(text)


def print_output(text, title=None, sample=None):
    print(get_output(text, title, sample))
