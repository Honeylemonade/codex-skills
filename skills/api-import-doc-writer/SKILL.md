---
name: api-import-doc-writer
description: Generate import-ready API reference Markdown from source API handlers, route registration code, request builders, or existing API docs. Use when asked to inspect backend code and produce API documentation with method, URL, purpose, query/path/header/body/response fields, typed import JSON blocks, examples, and field descriptions for API import tools.
---

# API Import Doc Writer

## Overview

Create API reference documents that are accurate enough for humans and structured enough for API import tools. Prefer source handlers, route registration, schema definitions, request builders, and tests over memory or inferred conventions.

Use `references/example_byterec_api_reference.md` as a complete example of the expected output shape. Use `scripts/validate_api_doc.py` before delivering a generated document.

## Workflow

1. Locate source-of-truth code.
   - Find route registration, handler classes/functions, request parsing, schema/model/protobuf/dataclass definitions, response wrappers, and representative callers.
   - Record method and path from route registration, not just from client code.
   - For internal wrappers, distinguish public API path from helper/client function names.

2. Build one section per endpoint.
   - Title format: ``## `METHOD /path` ``.
   - Include: Purpose, Query Params, Path Params, Headers, Body Example or Body, Body Fields, Response Example, Response Fields.
   - Under every param/field group, include an `Import JSON` block even when empty.

3. Document common parameters under each API.
   - Repeat shared query params and headers inside each endpoint section, because import tools often work per endpoint.
   - Keep `fieldName` as the real parameter name, for example `caller_name`.
   - If the import tool needs a transport hint, put it in `description`, for example `http_query_params: caller_name`.

4. Model request bodies for import, not only for one example.
   - Include all supported body variants discovered from code, such as datasource types, schema modes, and region-specific dynamic keys.
   - If the backend expects dynamic top-level keys such as `eu` and `ttp`, document them as top-level fields, not under a scalar `region` field.
   - If the user limits allowed variants, remove the extra variants from both the field table and Import JSON.

5. Use only the target import tool's field types.
   - Allowed `type` values: `string`, `boolean`, `integer`, `object`, `map`, `array`.
   - Convert specific array spellings such as `array<object>` and `array<string>` to `array`.
   - Convert typed maps such as `object<string, object>` to `map`.
   - Model every array as exactly one child named `items`. If the array item is an object, put the item's fields under `items.children`.

6. Structure Import JSON for importer compatibility.
   - Each field item should use:
     ```json
     {
       "fieldName": "field_name",
       "type": "string",
       "description": "Field meaning.",
       "compliance_tag": {}
     }
     ```
   - For `object`, include non-empty `children`; do not emit an empty object field if the importer rejects empty objects.
   - For `array`, include exactly one child:
     ```json
     {
       "fieldName": "items",
       "type": "object",
       "description": "Array item.",
       "compliance_tag": null,
       "children": [
         {
           "fieldName": "name",
           "type": "string",
           "description": "Item field.",
           "compliance_tag": {}
         }
       ]
     }
     ```
     Replace `type` with `string`, `integer`, or another scalar type for scalar arrays, and omit `children` for scalar items.
   - For nested fields, prefer nested `children` over flat names like `data.uri` when importing body or response schemas.
   - Use `[]` for empty query/path/header/body groups.

7. Validate before final delivery.
   - Run:
     ```bash
     python3 scripts/validate_api_doc.py <generated-doc.md>
     ```
   - Fix invalid JSON, unsupported field types, and any `object` field without non-empty `children`.

## Output Contract

For each endpoint, produce this order:

````markdown
## `POST /example/path`

Purpose: One concise sentence.

### Query Params

| Field | Type | Required | Description |
|---|---|---|---|
| `caller_name` | `string` | Yes | http_query_params: caller_name |

Import JSON:

```json
[
  {
    "fieldName": "caller_name",
    "type": "string",
    "description": "http_query_params: caller_name",
    "compliance_tag": {}
  }
]
```
````

Repeat the same pattern for Path Params, Headers, Body Fields, and Response Fields.

## Field Description Rules

- Describe what the backend uses the field for, not just its English name.
- Mark requirement with practical values such as `Yes`, `No`, `For kafka`, `Sequence only`, or `Conditional`.
- For enum-like fields, list known values in the description.
- For response wrappers, document both wrapper fields such as `code` and nested payload fields such as `data.uri`.
- If source code returns generic errors through a common wrapper, document the success response and mention error behavior in the description.

## Common Pitfalls

- Do not invent routes from client wrapper names.
- Do not leave body variants out just because the sample request uses one region or type.
- Do not use unsupported import types like `array<object>` or `array<string>`.
- Do not place multiple children directly under an `array`; wrap them under one `items` child.
- Do not emit `object` fields without `children` in Import JSON.
- Do not flatten nested Import JSON fields if the importer expects `children`.
