"""Readable sequence-feature functions used by the workshop notebooks."""


def count_occurrences(word, letter):
    """Count exact occurrences of one character using a traceable loop."""
    if len(letter) != 1:
        raise ValueError("letter must contain exactly one character")

    occurrence_count = 0
    for character in word:
        if character == letter:
            occurrence_count += 1
    return occurrence_count


def st_frequency(sequence):
    """Return the whole-protein fraction of residues that are S or T."""
    if len(sequence) == 0:
        return None

    st_count = count_occurrences(sequence, "S")
    st_count += count_occurrences(sequence, "T")
    return st_count / len(sequence)


def sliding_st_frequencies(sequence, window_size=50):
    """Return S/T frequencies for all overlapping windows in start order."""
    if window_size <= 0:
        raise ValueError("window_size must be greater than zero")

    if len(sequence) == 0:
        return []

    if len(sequence) <= window_size:
        return [st_frequency(sequence)]

    frequencies = []
    last_start = len(sequence) - window_size
    for start in range(last_start + 1):
        window = sequence[start : start + window_size]
        st_count = window.count("S") + window.count("T")
        frequencies.append(st_count / window_size)

    return frequencies


def max_st_frequency_window(sequence, window_size=50):
    """Return the maximum sliding-window S/T frequency, or None if empty."""
    frequencies = sliding_st_frequencies(sequence, window_size)
    if len(frequencies) == 0:
        return None
    return max(frequencies)
