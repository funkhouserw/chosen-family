#### PERSON standard

This is the proposed JSON standard format for someone who will be added to the family tree.

```
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://example.com/product.schema.json",
  "title": "Person",
  "description": "Proposed Standard For a PERSON object on a family tree",
  "type": "object",
  "properties": {
    "name": {
      "description": "a NAME object. TODO for me to write NAME.md,
      "type": "object",
      $ref: "TODO NAME.md"
    },
    "gender": {
      "description": "a GENDER object. TODO to write GENDER.md",
      "type": "object"
      $ref: "TODO gender.md"
    },
    "family_memberships": {
      "description": "a collection of family ids to which this person is considered a family.", # more can be inferred later
      "type": "array",
      "items": {
        "type": "string"
       }
    },
    "vital_events": {
      "description": "A collection of birth, death, and burial dates and locations.",
      "type":"array",
      "items": {
        $ref: "TODO: link to schema/ VITAL_EVENT.md"
      }
    },
    "major_life_events": {
      "description": "A collection of major life events with dates, descriptions, and locations.",
      "type":"array",
      "items": {
        $ref: "TODO: link to schema/ MAJOR_LIFE_EVENT.md"
      }
    },
    "custom_kinship_titles": {
      "description": "A collection of any non-standard relationship titles, e.g. you are a male parent but don't want to be called 'father'",
      "type":"array",
      "items": {
        $ref: "TODO: standard relationship_title thing."
      }
    }
  },
  "required": [ "name","gender", ]
}
```
