import re

# Ticket pattern
ticket_regex = r"(CVE\-[0-9]+\-[0-9]+)|([A-Z]+\-[0-9]{3,})"

def add_to_results(results, key, val):
    if key in results:
        results[key].append(val)
    else:
        results[key] = [val]
    return val

def ticket_matcher(text, results):
    def match(m):
        return add_to_results(results, "tickets", m.group(0))
    text = re.sub(ticket_regex, match, text, flags=re.MULTILINE)
    return text