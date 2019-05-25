V_PAD = '\n\n'
H_PAD = '     '


def title_fmt(title):
    return f'<|endoftext|>\n<|title|>{title}<|title|>\n\n\n'


def output_fmt(text):
    padded = text.replace('\n', f'\n{H_PAD}')
    return padded\
        .replace("<|endoftext|>", f"{'=' * 80}{V_PAD}")\
        .replace("<|title|>", "") + V_PAD


def _v_spacer(text):
    return V_PAD + "=" * 40 + f' {text} ' + "=" * 40 + V_PAD


def get_output(text, title=None, sample=None):
    start = _v_spacer(f"SAMPLE {str(sample)}") if sample is not None else ''

    if title:
        start += f'{H_PAD}{title}\n\n\n\n'

    return f'{V_PAD}{start}{output_fmt(text)}{V_PAD}{_v_spacer("END")}{V_PAD}'


def print_output(text, title=None, sample=None):
    print(get_output(text, title, sample))
