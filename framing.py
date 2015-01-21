import json
from pyld import jsonld

library = {
  "@context": {
    "dc": "http://purl.org/dc/elements/1.1/",
    "ex": "http://example.org/vocab#",
    "ex:contains": {
      "@type": "@id"
    }
  },
  "@graph": [
    {
      "@id": "http://example.org/library",
      "@type": "ex:Library",
      "ex:contains": "http://example.org/library/the-republic"
    },
    {
      "@id": "http://example.org/library/the-republic",
      "@type": "ex:Book",
      "dc:creator": "Plato",
      "dc:title": "The Republic",
      "ex:contains": "http://example.org/library/the-republic#introduction"
    },
    {
      "@id": "http://example.org/library/the-republic#introduction",
      "@type": "ex:Chapter",
      "dc:description": "An introductory chapter on The Republic.",
      "dc:title": "The Introduction"
    }
  ]
}

context = library['@context'].copy()

frame = {
  "@context": {
    "dc": "http://purl.org/dc/elements/1.1/",
    "ex": "http://example.org/vocab#"
  },
  "@type": "ex:Library",
  "ex:contains": {
    "@embed": '@last',
    "@type": "ex:Book",
    "ex:contains": {
      "@type": "ex:Chapter"
    }
  }
}

def format_json(d):
    return json.dumps(d, sort_keys=True, indent=4, separators=(',', ': '))

print "Input:"
print format_json(library)
print

print "Frame:",
print format_json(frame)
print

print "Framed:"
framed = jsonld.frame(library, frame)
print format_json(framed)
print

friendly_context = {
    "creator": "http://purl.org/dc/elements/1.1/creator",
    "title": "http://purl.org/dc/elements/1.1/title",
    "description": "http://purl.org/dc/elements/1.1/description",
    "contains": "http://example.org/vocab#contains",
}

print "Framed, compacted:"
compacted = jsonld.compact(framed, context)
print format_json(compacted)

print "Framed, compacted with friendly context"
compacted_friendly = jsonld.compact(framed, friendly_context)
print format_json(compacted_friendly)
