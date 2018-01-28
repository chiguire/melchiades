import math

def render_lines(f, text, w, h):
    all_fit = False
    text_partitions = [text]
    while not all_fit:
        all_fit, surfaces_or_partitions = render_partitions(text, text_partitions, f, w)
        if not all_fit:
            text_partitions = surfaces_or_partitions
        else:
            surfaces = surfaces_or_partitions
    return [(surface, calculate_position(surface, w, h, i, len(surfaces))) for i, surface in enumerate(surfaces)]

def calculate_position(srf, w, h, i, n):
    rect = srf.get_rect()
    whole_text_height = rect.height*n
    return ((w - rect.width)/2.0, (h - whole_text_height-60)/2.0 + rect.height*i)

def render_partitions(text, text_partitions, f, w):
    tsfs = []

    for partition in text_partitions:
        tsf = f.render(partition, True, (255, 127, 0), None)
        if tsf.get_width() > w:
            return (False, partition_text(text, len(text_partitions) + 1))
        tsfs.append(tsf)
    return (True, tsfs)

def chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i+n]

def partition_text(text, n):
    words = text.split()
    words_chunked = chunks(words, int(math.ceil(len(words)/n)))
    return [' '.join(words) for words in words_chunked]
    
