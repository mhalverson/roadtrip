from datetime import timedelta

def format_date_range(first, last, sep=' to '):
    # collapse the range, joining with sep
    if first == last:
        return '{}'.format(first)
    else:
        return '{}{}{}'.format(first, sep, last)

def break_into_ranges(dates):
    '''Given a list of datetime.dates, returns a list of lists of consecutive dates.
    '''
    # break into non-consecutive ranges
    ranges = []
    # pick your start
    first = dates[0]
    last = dates[0]
    for d in dates[1:]:
        # chew through consecutive ones
        if d - last == timedelta(1):
            last = d
            continue

        # we found the start of a new range!
        ranges.append((first, last))
        first = d
        last = d
    ranges.append((first, last))
    return ranges

def format_date_ranges(ranges, sep=', ', inner_sep=' to '):
    formatted_elems = [format_date_range(first,last,sep=inner_sep) for (first, last) in ranges]
    return sep.join(formatted_elems)

def collapse_date_ranges(dates, sep=', ', inner_sep=' to '):
    '''Given a list of datetime.dates, returns a string with consecutive dates collapsed into ranges (first - last).
    If there are multiple ranges, they will be separated by sep.
    '''
    # early return
    if not dates:
        return ''
    if len(dates) == 1:
        return str(dates[0])

    ranges = break_into_ranges(dates)
    return format_date_ranges(ranges, sep=sep, inner_sep=inner_sep)
