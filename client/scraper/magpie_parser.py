from HTMLParser import HTMLParser

class MagpieParser(HTMLParser):
    json_return = ""
    prop_map = {}

    def handle_starttag(self, tag, attrs):
        if tag == 'meta' and len(attrs) > 1:
            key = attrs[0][1]
            self.prop_map[key] = attrs[1][1]
