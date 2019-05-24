def title_fmt(title):
    return f'<|endoftext|>\n<|title|>{title}<|title|>\n\n\n'


def output_fmt(text):
    return text.replace("<|endoftext|>", f"{'=' * 80}\n\n").replace("<|title|>", "")


def print_output(text, title=None):
    if title:
        start = f'{title}\n\n\n\n'
    else:
        start = ''

    print(f'\n\n{"=" * 80}\n\n{start}' + output_fmt(text))
