V_PAD = '\n\n'
H_PAD = '     '
END_T = '<|endoftext|>'
TITLE_T = '<|title|>'


def title_fmt(title):
    # format input into title; NB must match training data format!
    return f'{END_T}\n{TITLE_T}{title}{TITLE_T}\n\n\n'


def output_fmt(text, trunc_first):
    if trunc_first:
        text = text.split(END_T)[0]
    padded = text.replace('\n', f'\n{H_PAD}')
    return padded.replace(END_T, f"{'=' * 80}{V_PAD}").replace(TITLE_T, "") + V_PAD


def _v_spacer(text):
    return V_PAD + "=" * 40 + f' {text} ' + "=" * 40 + V_PAD


def get_output(text, title=None, sample=None, trunc_first=False):
    start = _v_spacer(f"SAMPLE {str(sample)}") if sample is not None else ''

    if title:
        start += f'{H_PAD}{title}{V_PAD * 2}'

    return f'{V_PAD}{start}{output_fmt(text, trunc_first)}{V_PAD}{_v_spacer("END")}{V_PAD}'


def print_output(text, title=None, sample=None, trunc_first=False):
    print(get_output(text, title, sample, trunc_first))
