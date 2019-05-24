def title_fmt(title):
    return f'<|endoftext|>\n<|title|>{title}<|title|>\n\n\n'


def output_fmt(text):
    return text.replace("<|endoftext|>", f"{'=' * 80}\n\n").replace("<|title|>", "")


def get_output(text, title=None, sample=None):
    start = "=" * 40 + " SAMPLE " + str(sample) + " " + "=" * 40 + '\n\n' if sample is not None else ''

    if title:
        start += f'{title}\n\n\n\n'

    return f'\n\n{"=" * 80}\n\n{start}' + output_fmt(text)


def print_output(text, title=None, sample=None):
    print(get_output(text, title, sample))
