# ByteRec / DataCenter OpenAPI Reference

This document is based on handler code in `dep_repo/byterec_site`, especially:

- `yoda/subsys_data_center/view/data_source_service.py`
- `yoda/subsys_darwin/api_restful_darwin_api_config.py`
- `yoda/subsys_data_center/view/data_schema_service.py`
- `yoda/subsys_data_center/view/task_service.py`
- `yoda/subsys_data_center/view/dsl_service.py`


## `POST /openapi/subsys/data_center/data_source`

Purpose: Create a DataCenter datasource after duplicate-check has confirmed that creation is allowed.

### Query Params

| Field | Type | Required | Description |
|---|---|---|---|
| `caller_name` | `string` | Yes | http_query_params: caller_name |
| `caller_token` | `string` | Yes | http_query_params: caller_token |

Import JSON:

```json
[
  {
    "fieldName": "caller_name",
    "type": "string",
    "description": "http_query_params: caller_name"
  },
  {
    "fieldName": "caller_token",
    "type": "string",
    "description": "http_query_params: caller_token"
  }
]
```

### Path Params

None.

Import JSON:

```json
[]
```

### Headers

| Field | Type | Required | Description |
|---|---|---|---|
| `x-xcenter-entrance` | `string` | No | XCenter entrance URI. If provided, the backend derives the actual product from this entrance instead of trusting only the body `product`. |
| `Locale` | `string` | No | Language hint for localized error messages, for example `zh` or `en`. |
| `x-tt-env` | `string` | No | PPE environment routing header. Used only when the client intentionally calls a PPE environment. |
| `x-use-ppe` | `string` | No | PPE switch header. Usually set to `1` together with `x-tt-env` for PPE requests. |

Import JSON:

```json
[
  {
    "fieldName": "x-xcenter-entrance",
    "type": "string",
    "description": "XCenter entrance URI. If provided, the backend derives the actual product from this entrance instead of trusting only the body product."
  },
  {
    "fieldName": "Locale",
    "type": "string",
    "description": "Language hint for localized error messages, for example zh or en."
  },
  {
    "fieldName": "x-tt-env",
    "type": "string",
    "description": "PPE environment routing header. Used only when the client intentionally calls a PPE environment."
  },
  {
    "fieldName": "x-use-ppe",
    "type": "string",
    "description": "PPE switch header. Usually set to 1 together with x-tt-env for PPE requests."
  }
]
```

### Body Example

```json
{
  "product": "tiktok",
  "name": "bmq_cluster_topic_eu",
  "description": "bmq_cluster_topic_eu",
  "region": "eu",
  "type": "kafka",
  "staff_name": "user.name",
  "data_type": "pb",
  "schema_name": "com.example.Demo",
  "eu": {
    "kafka_config": {
      "cluster": "bmq_streaming_useast2a",
      "topic": "user_action_pb_topbuzz"
    },
    "extra_config": [
      {"name": "scan.startup.mode", "value": "group-offsets"}
    ]
  }
}
```

### Body Fields

Note: `eu` and `ttp` are top-level request body keys. They are not nested under the scalar `region` field.

| Field | Type | Required | Description |
|---|---|---|---|
| `product` | `string` | Yes | Product or DataCenter workspace that owns the datasource. If `x-xcenter-entrance` is set, the backend resolves product from that entrance. |
| `name` | `string` | Yes | DataCenter datasource name. It must be legal and unique in the relevant product/global namespace checks. |
| `description` | `string` | No | Human-readable datasource description stored on datasource metadata. |
| `region` | `string` | No | Target or display region used by datasource creation. Region-specific physical configs are still supplied as top-level region keys. |
| `type` | `string` | Yes | Datasource type. Supported backend values include `hive`, `kafka`, `rocketmq`, `rpc`, `abase`, `index_service`, `redis`, and `paimon`. |
| `staff_name` | `string` | OpenAPI | Owner/creator staff name. The OpenAPI create handler comments indicate this is required for OpenAPI callers. |
| `data_type` | `string` | Kafka/RocketMQ | Message payload format for Kafka or RocketMQ. Supported values are `json` and `pb`. |
| `schema_name` | `string` | Kafka/RocketMQ PB | Existing DataCenter schema name to bind to a PB Kafka or RocketMQ datasource. |
| `schema_product` | `string` | No | Product that owns `schema_name`; defaults to request `product` if omitted. |
| `fields` | `array` | Hive or PB | Field list used by Hive datasource creation or PB datasource binding. |
| `fields[].name` | `string` | When `fields` is used | Field name. |
| `fields[].data_type` | `string` | When `fields` is used | DataCenter/Monarch field type string. |
| `custom_fields` | `array` | Kafka/RocketMQ JSON | Flattened field list for JSON Kafka or RocketMQ datasources. |
| `custom_fields[].name` | `string` | When `custom_fields` is used | JSON field name. |
| `custom_fields[].data_type` | `string` | When `custom_fields` is used | DataCenter/Monarch field type string. |
| `request` | `array` | RPC optional | RPC request field schema. |
| `request[].name` | `string` | When `request` is used | RPC request field name. |
| `request[].data_type` | `string` | When `request` is used | RPC request field type. |
| `response` | `array` | RPC optional | RPC response field schema. |
| `response[].name` | `string` | When `response` is used | RPC response field name. |
| `response[].data_type` | `string` | When `response` is used | RPC response field type. |
| `eu` | `object` | Conditional | Region-specific physical configuration block for `eu`. This import template only includes `eu` and `ttp`. |
| `eu.kafka_config` | `object` | For `kafka` in `eu` | Kafka/BMQ physical config. |
| `eu.kafka_config.cluster` | `string` | For `kafka` in `eu` | Kafka/BMQ cluster name. |
| `eu.kafka_config.topic` | `string` | For `kafka` in `eu` | Kafka/BMQ topic name. |
| `eu.hive_config` | `object` | For `hive` in `eu` | Hive physical config. |
| `eu.hive_config.database` | `string` | For `hive` in `eu` | Hive database name. |
| `eu.hive_config.table` | `string` | For `hive` in `eu` | Hive table name. |
| `eu.rocketmq_config` | `object` | For `rocketmq` in `eu` | RocketMQ physical config. |
| `eu.rocketmq_config.cluster` | `string` | For `rocketmq` in `eu` | RocketMQ cluster name. |
| `eu.rocketmq_config.topic` | `string` | For `rocketmq` in `eu` | RocketMQ topic name. |
| `eu.rpc_config` | `object` | For `rpc` in `eu` | RPC physical config. |
| `eu.rpc_config.psm` | `string` | For `rpc` in `eu` | RPC PSM or consul identity. |
| `eu.rpc_config.service_class` | `string` | For `rpc` in `eu` | Thrift service class. |
| `eu.rpc_config.method` | `string` | For `rpc` in `eu` | Thrift method name. |
| `eu.rpc_config.cluster` | `string` | No | Optional RPC cluster. |
| `eu.abase_config` | `object` | For `abase` in `eu` | Abase physical config. |
| `eu.abase_config.psm` | `string` | For `abase` in `eu` | Abase PSM. |
| `eu.abase_config.table` | `string` | For `abase` in `eu` | Abase table name. |
| `eu.index_service_config` | `object` | For `index_service` in `eu` | IndexService physical config. |
| `eu.index_service_config.psm` | `string` | For `index_service` in `eu` | IndexService PSM. |
| `eu.index_service_config.index_name` | `string` | For `index_service` in `eu` | IndexService index name. |
| `eu.redis_config` | `object` | For `redis` in `eu` | Redis physical config. |
| `eu.redis_config.cluster` | `string` | For `redis` in `eu` | Redis cluster name. |
| `eu.paimon_config` | `object` | For `paimon` in `eu` | Paimon physical config. |
| `eu.paimon_config.database` | `string` | For `paimon` in `eu` | Paimon database name. |
| `eu.paimon_config.table` | `string` | For `paimon` in `eu` | Paimon table name. |
| `eu.extra_config` | `array` | No | Additional datasource options. Duplicate check compares these options when provided. |
| `eu.extra_config[].name` | `string` | No | Extra option key. |
| `eu.extra_config[].value` | `string` | No | Extra option value. |
| `ttp` | `object` | Conditional | Region-specific physical configuration block for `ttp`. This import template only includes `eu` and `ttp`. |
| `ttp.kafka_config` | `object` | For `kafka` in `ttp` | Kafka/BMQ physical config. |
| `ttp.kafka_config.cluster` | `string` | For `kafka` in `ttp` | Kafka/BMQ cluster name. |
| `ttp.kafka_config.topic` | `string` | For `kafka` in `ttp` | Kafka/BMQ topic name. |
| `ttp.hive_config` | `object` | For `hive` in `ttp` | Hive physical config. |
| `ttp.hive_config.database` | `string` | For `hive` in `ttp` | Hive database name. |
| `ttp.hive_config.table` | `string` | For `hive` in `ttp` | Hive table name. |
| `ttp.rocketmq_config` | `object` | For `rocketmq` in `ttp` | RocketMQ physical config. |
| `ttp.rocketmq_config.cluster` | `string` | For `rocketmq` in `ttp` | RocketMQ cluster name. |
| `ttp.rocketmq_config.topic` | `string` | For `rocketmq` in `ttp` | RocketMQ topic name. |
| `ttp.rpc_config` | `object` | For `rpc` in `ttp` | RPC physical config. |
| `ttp.rpc_config.psm` | `string` | For `rpc` in `ttp` | RPC PSM or consul identity. |
| `ttp.rpc_config.service_class` | `string` | For `rpc` in `ttp` | Thrift service class. |
| `ttp.rpc_config.method` | `string` | For `rpc` in `ttp` | Thrift method name. |
| `ttp.rpc_config.cluster` | `string` | No | Optional RPC cluster. |
| `ttp.abase_config` | `object` | For `abase` in `ttp` | Abase physical config. |
| `ttp.abase_config.psm` | `string` | For `abase` in `ttp` | Abase PSM. |
| `ttp.abase_config.table` | `string` | For `abase` in `ttp` | Abase table name. |
| `ttp.index_service_config` | `object` | For `index_service` in `ttp` | IndexService physical config. |
| `ttp.index_service_config.psm` | `string` | For `index_service` in `ttp` | IndexService PSM. |
| `ttp.index_service_config.index_name` | `string` | For `index_service` in `ttp` | IndexService index name. |
| `ttp.redis_config` | `object` | For `redis` in `ttp` | Redis physical config. |
| `ttp.redis_config.cluster` | `string` | For `redis` in `ttp` | Redis cluster name. |
| `ttp.paimon_config` | `object` | For `paimon` in `ttp` | Paimon physical config. |
| `ttp.paimon_config.database` | `string` | For `paimon` in `ttp` | Paimon database name. |
| `ttp.paimon_config.table` | `string` | For `paimon` in `ttp` | Paimon table name. |
| `ttp.extra_config` | `array` | No | Additional datasource options. Duplicate check compares these options when provided. |
| `ttp.extra_config[].name` | `string` | No | Extra option key. |
| `ttp.extra_config[].value` | `string` | No | Extra option value. |

Import JSON:

```json
[
  {
    "fieldName": "product",
    "type": "string",
    "description": "Product or DataCenter workspace that owns the datasource.",
    "compliance_tag": {}
  },
  {
    "fieldName": "name",
    "type": "string",
    "description": "DataCenter datasource name. It must be legal and unique in the relevant product/global namespace checks.",
    "compliance_tag": {}
  },
  {
    "fieldName": "description",
    "type": "string",
    "description": "Human-readable datasource description stored on datasource metadata.",
    "compliance_tag": {}
  },
  {
    "fieldName": "region",
    "type": "string",
    "description": "Target or display region used by datasource creation.",
    "compliance_tag": {}
  },
  {
    "fieldName": "type",
    "type": "string",
    "description": "Datasource type. Supported backend values include hive, kafka, rocketmq, rpc, abase, index_service, redis, and paimon.",
    "compliance_tag": {}
  },
  {
    "fieldName": "staff_name",
    "type": "string",
    "description": "Owner/creator staff name for OpenAPI creation requests.",
    "compliance_tag": {}
  },
  {
    "fieldName": "data_type",
    "type": "string",
    "description": "Message payload format for Kafka or RocketMQ. Supported values are json and pb.",
    "compliance_tag": {}
  },
  {
    "fieldName": "schema_name",
    "type": "string",
    "description": "Existing DataCenter schema name to bind to a PB Kafka or RocketMQ datasource.",
    "compliance_tag": {}
  },
  {
    "fieldName": "schema_product",
    "type": "string",
    "description": "Product that owns schema_name; defaults to request product if omitted.",
    "compliance_tag": {}
  },
  {
    "fieldName": "fields",
    "type": "array",
    "description": "Field list used by Hive datasource creation or PB datasource binding.",
    "compliance_tag": null,
    "children": [
      {
        "fieldName": "items",
        "type": "object",
        "description": "Array item for fields.",
        "compliance_tag": null,
        "children": [
          {
            "fieldName": "name",
            "type": "string",
            "description": "Field name.",
            "compliance_tag": {}
          },
          {
            "fieldName": "data_type",
            "type": "string",
            "description": "DataCenter/Monarch field type string.",
            "compliance_tag": {}
          }
        ]
      }
    ]
  },
  {
    "fieldName": "custom_fields",
    "type": "array",
    "description": "Flattened field list for JSON Kafka or RocketMQ datasources.",
    "compliance_tag": null,
    "children": [
      {
        "fieldName": "items",
        "type": "object",
        "description": "Array item for custom_fields.",
        "compliance_tag": null,
        "children": [
          {
            "fieldName": "name",
            "type": "string",
            "description": "Field name.",
            "compliance_tag": {}
          },
          {
            "fieldName": "data_type",
            "type": "string",
            "description": "DataCenter/Monarch field type string.",
            "compliance_tag": {}
          }
        ]
      }
    ]
  },
  {
    "fieldName": "request",
    "type": "array",
    "description": "RPC request field schema.",
    "compliance_tag": null,
    "children": [
      {
        "fieldName": "items",
        "type": "object",
        "description": "Array item for request.",
        "compliance_tag": null,
        "children": [
          {
            "fieldName": "name",
            "type": "string",
            "description": "RPC request field name.",
            "compliance_tag": {}
          },
          {
            "fieldName": "data_type",
            "type": "string",
            "description": "RPC request field type.",
            "compliance_tag": {}
          }
        ]
      }
    ]
  },
  {
    "fieldName": "response",
    "type": "array",
    "description": "RPC response field schema.",
    "compliance_tag": null,
    "children": [
      {
        "fieldName": "items",
        "type": "object",
        "description": "Array item for response.",
        "compliance_tag": null,
        "children": [
          {
            "fieldName": "name",
            "type": "string",
            "description": "RPC response field name.",
            "compliance_tag": {}
          },
          {
            "fieldName": "data_type",
            "type": "string",
            "description": "RPC response field type.",
            "compliance_tag": {}
          }
        ]
      }
    ]
  },
  {
    "fieldName": "eu",
    "type": "object",
    "description": "Region-specific physical configuration block for eu. Only eu and ttp are included in this import template.",
    "compliance_tag": null,
    "children": [
      {
        "fieldName": "kafka_config",
        "type": "object",
        "description": "Kafka/BMQ physical config. Used when type is kafka.",
        "compliance_tag": null,
        "children": [
          {
            "fieldName": "cluster",
            "type": "string",
            "description": "Kafka/BMQ cluster name.",
            "compliance_tag": {}
          },
          {
            "fieldName": "topic",
            "type": "string",
            "description": "Kafka/BMQ topic name.",
            "compliance_tag": {}
          }
        ]
      },
      {
        "fieldName": "hive_config",
        "type": "object",
        "description": "Hive physical config. Used when type is hive.",
        "compliance_tag": null,
        "children": [
          {
            "fieldName": "database",
            "type": "string",
            "description": "Hive database name.",
            "compliance_tag": {}
          },
          {
            "fieldName": "table",
            "type": "string",
            "description": "Hive table name.",
            "compliance_tag": {}
          }
        ]
      },
      {
        "fieldName": "rocketmq_config",
        "type": "object",
        "description": "RocketMQ physical config. Used when type is rocketmq.",
        "compliance_tag": null,
        "children": [
          {
            "fieldName": "cluster",
            "type": "string",
            "description": "RocketMQ cluster name.",
            "compliance_tag": {}
          },
          {
            "fieldName": "topic",
            "type": "string",
            "description": "RocketMQ topic name.",
            "compliance_tag": {}
          }
        ]
      },
      {
        "fieldName": "rpc_config",
        "type": "object",
        "description": "RPC physical config. Used when type is rpc.",
        "compliance_tag": null,
        "children": [
          {
            "fieldName": "psm",
            "type": "string",
            "description": "RPC PSM or consul identity.",
            "compliance_tag": {}
          },
          {
            "fieldName": "service_class",
            "type": "string",
            "description": "Thrift service class.",
            "compliance_tag": {}
          },
          {
            "fieldName": "method",
            "type": "string",
            "description": "Thrift method name.",
            "compliance_tag": {}
          },
          {
            "fieldName": "cluster",
            "type": "string",
            "description": "Optional RPC cluster.",
            "compliance_tag": {}
          }
        ]
      },
      {
        "fieldName": "abase_config",
        "type": "object",
        "description": "Abase physical config. Used when type is abase.",
        "compliance_tag": null,
        "children": [
          {
            "fieldName": "psm",
            "type": "string",
            "description": "Abase PSM.",
            "compliance_tag": {}
          },
          {
            "fieldName": "table",
            "type": "string",
            "description": "Abase table name.",
            "compliance_tag": {}
          }
        ]
      },
      {
        "fieldName": "index_service_config",
        "type": "object",
        "description": "IndexService physical config. Used when type is index_service.",
        "compliance_tag": null,
        "children": [
          {
            "fieldName": "psm",
            "type": "string",
            "description": "IndexService PSM.",
            "compliance_tag": {}
          },
          {
            "fieldName": "index_name",
            "type": "string",
            "description": "IndexService index name.",
            "compliance_tag": {}
          }
        ]
      },
      {
        "fieldName": "redis_config",
        "type": "object",
        "description": "Redis physical config. Used when type is redis.",
        "compliance_tag": null,
        "children": [
          {
            "fieldName": "cluster",
            "type": "string",
            "description": "Redis cluster name.",
            "compliance_tag": {}
          }
        ]
      },
      {
        "fieldName": "paimon_config",
        "type": "object",
        "description": "Paimon physical config. Used when type is paimon.",
        "compliance_tag": null,
        "children": [
          {
            "fieldName": "database",
            "type": "string",
            "description": "Paimon database name.",
            "compliance_tag": {}
          },
          {
            "fieldName": "table",
            "type": "string",
            "description": "Paimon table name.",
            "compliance_tag": {}
          }
        ]
      },
      {
        "fieldName": "extra_config",
        "type": "array",
        "description": "Additional datasource options stored on the datasource metadata.",
        "compliance_tag": null,
        "children": [
          {
            "fieldName": "items",
            "type": "object",
            "description": "Array item for extra_config.",
            "compliance_tag": null,
            "children": [
              {
                "fieldName": "name",
                "type": "string",
                "description": "Extra option key.",
                "compliance_tag": {}
              },
              {
                "fieldName": "value",
                "type": "string",
                "description": "Extra option value.",
                "compliance_tag": {}
              }
            ]
          }
        ]
      }
    ]
  },
  {
    "fieldName": "ttp",
    "type": "object",
    "description": "Region-specific physical configuration block for ttp. Only eu and ttp are included in this import template.",
    "compliance_tag": null,
    "children": [
      {
        "fieldName": "kafka_config",
        "type": "object",
        "description": "Kafka/BMQ physical config. Used when type is kafka.",
        "compliance_tag": null,
        "children": [
          {
            "fieldName": "cluster",
            "type": "string",
            "description": "Kafka/BMQ cluster name.",
            "compliance_tag": {}
          },
          {
            "fieldName": "topic",
            "type": "string",
            "description": "Kafka/BMQ topic name.",
            "compliance_tag": {}
          }
        ]
      },
      {
        "fieldName": "hive_config",
        "type": "object",
        "description": "Hive physical config. Used when type is hive.",
        "compliance_tag": null,
        "children": [
          {
            "fieldName": "database",
            "type": "string",
            "description": "Hive database name.",
            "compliance_tag": {}
          },
          {
            "fieldName": "table",
            "type": "string",
            "description": "Hive table name.",
            "compliance_tag": {}
          }
        ]
      },
      {
        "fieldName": "rocketmq_config",
        "type": "object",
        "description": "RocketMQ physical config. Used when type is rocketmq.",
        "compliance_tag": null,
        "children": [
          {
            "fieldName": "cluster",
            "type": "string",
            "description": "RocketMQ cluster name.",
            "compliance_tag": {}
          },
          {
            "fieldName": "topic",
            "type": "string",
            "description": "RocketMQ topic name.",
            "compliance_tag": {}
          }
        ]
      },
      {
        "fieldName": "rpc_config",
        "type": "object",
        "description": "RPC physical config. Used when type is rpc.",
        "compliance_tag": null,
        "children": [
          {
            "fieldName": "psm",
            "type": "string",
            "description": "RPC PSM or consul identity.",
            "compliance_tag": {}
          },
          {
            "fieldName": "service_class",
            "type": "string",
            "description": "Thrift service class.",
            "compliance_tag": {}
          },
          {
            "fieldName": "method",
            "type": "string",
            "description": "Thrift method name.",
            "compliance_tag": {}
          },
          {
            "fieldName": "cluster",
            "type": "string",
            "description": "Optional RPC cluster.",
            "compliance_tag": {}
          }
        ]
      },
      {
        "fieldName": "abase_config",
        "type": "object",
        "description": "Abase physical config. Used when type is abase.",
        "compliance_tag": null,
        "children": [
          {
            "fieldName": "psm",
            "type": "string",
            "description": "Abase PSM.",
            "compliance_tag": {}
          },
          {
            "fieldName": "table",
            "type": "string",
            "description": "Abase table name.",
            "compliance_tag": {}
          }
        ]
      },
      {
        "fieldName": "index_service_config",
        "type": "object",
        "description": "IndexService physical config. Used when type is index_service.",
        "compliance_tag": null,
        "children": [
          {
            "fieldName": "psm",
            "type": "string",
            "description": "IndexService PSM.",
            "compliance_tag": {}
          },
          {
            "fieldName": "index_name",
            "type": "string",
            "description": "IndexService index name.",
            "compliance_tag": {}
          }
        ]
      },
      {
        "fieldName": "redis_config",
        "type": "object",
        "description": "Redis physical config. Used when type is redis.",
        "compliance_tag": null,
        "children": [
          {
            "fieldName": "cluster",
            "type": "string",
            "description": "Redis cluster name.",
            "compliance_tag": {}
          }
        ]
      },
      {
        "fieldName": "paimon_config",
        "type": "object",
        "description": "Paimon physical config. Used when type is paimon.",
        "compliance_tag": null,
        "children": [
          {
            "fieldName": "database",
            "type": "string",
            "description": "Paimon database name.",
            "compliance_tag": {}
          },
          {
            "fieldName": "table",
            "type": "string",
            "description": "Paimon table name.",
            "compliance_tag": {}
          }
        ]
      },
      {
        "fieldName": "extra_config",
        "type": "array",
        "description": "Additional datasource options stored on the datasource metadata.",
        "compliance_tag": null,
        "children": [
          {
            "fieldName": "items",
            "type": "object",
            "description": "Array item for extra_config.",
            "compliance_tag": null,
            "children": [
              {
                "fieldName": "name",
                "type": "string",
                "description": "Extra option key.",
                "compliance_tag": {}
              },
              {
                "fieldName": "value",
                "type": "string",
                "description": "Extra option value.",
                "compliance_tag": {}
              }
            ]
          }
        ]
      }
    ]
  }
]
```

### Response Example

```json
{
  "code": 0,
  "data": {
    "uri": "meta_center_eu_ttp://unified_catalog_table/tiktok/bmq_cluster_topic_eu"
  },
  "isDataToTCC": false
}
```

### Response Fields

| Field | Type | Description |
|---|---|---|
| `code` | `integer` | Business status code returned by the ByteRec wrapper. `0` means the datasource was created successfully. |
| `data` | `object` | Created datasource response payload. |
| `data.uri` | `string` | MetaCenter URI of the created unified catalog datasource. |
| `isDataToTCC` | `boolean` | Wrapper flag indicating whether the response data is dynamic/TCC-style data. |

Import JSON:

```json
[
  {
    "fieldName": "code",
    "type": "integer",
    "description": "Business status code returned by the ByteRec wrapper. 0 means the datasource was created successfully.",
    "compliance_tag": {}
  },
  {
    "fieldName": "data",
    "type": "object",
    "description": "Created datasource response payload.",
    "compliance_tag": null,
    "children": [
      {
        "fieldName": "uri",
        "type": "string",
        "description": "MetaCenter URI of the created unified catalog datasource.",
        "compliance_tag": {}
      }
    ]
  },
  {
    "fieldName": "isDataToTCC",
    "type": "boolean",
    "description": "Wrapper flag indicating whether the response data is dynamic/TCC-style data.",
    "compliance_tag": {}
  }
]
```

## `POST /openapi/subsys/data_center/data_source_duplicate_check`

Purpose: Check whether a datasource name or physical datasource config already exists.

### Query Params

| Field | Type | Required | Description |
|---|---|---|---|
| `caller_name` | `string` | Yes | http_query_params: caller_name |
| `caller_token` | `string` | Yes | http_query_params: caller_token |

Import JSON:

```json
[
  {
    "fieldName": "caller_name",
    "type": "string",
    "description": "http_query_params: caller_name"
  },
  {
    "fieldName": "caller_token",
    "type": "string",
    "description": "http_query_params: caller_token"
  }
]
```

### Path Params

None.

Import JSON:

```json
[]
```

### Headers

| Field | Type | Required | Description |
|---|---|---|---|
| `x-xcenter-entrance` | `string` | No | XCenter entrance URI. If provided, the backend derives the actual product from this entrance instead of trusting only the body `product`. |
| `Locale` | `string` | No | Language hint for localized error messages, for example `zh` or `en`. |
| `x-tt-env` | `string` | No | PPE environment routing header. Used only when the client intentionally calls a PPE environment. |
| `x-use-ppe` | `string` | No | PPE switch header. Usually set to `1` together with `x-tt-env` for PPE requests. |

Import JSON:

```json
[
  {
    "fieldName": "x-xcenter-entrance",
    "type": "string",
    "description": "XCenter entrance URI. If provided, the backend derives the actual product from this entrance instead of trusting only the body product."
  },
  {
    "fieldName": "Locale",
    "type": "string",
    "description": "Language hint for localized error messages, for example zh or en."
  },
  {
    "fieldName": "x-tt-env",
    "type": "string",
    "description": "PPE environment routing header. Used only when the client intentionally calls a PPE environment."
  },
  {
    "fieldName": "x-use-ppe",
    "type": "string",
    "description": "PPE switch header. Usually set to 1 together with x-tt-env for PPE requests."
  }
]
```

### Body Example

```json
{
  "product": "tiktok",
  "name": "bmq_cluster_topic_eu",
  "type": "kafka",
  "eu": {
    "kafka_config": {
      "cluster": "bmq_streaming_useast2a",
      "topic": "user_action_pb_topbuzz"
    }
  }
}
```

### Body Fields

Note: `eu` and `ttp` are top-level request body keys. They are not nested under another `region` object.

| Field | Type | Required | Description |
|---|---|---|---|
| `product` | `string` | Yes | Product or DataCenter workspace that owns the datasource. If `x-xcenter-entrance` is set, the backend resolves product from that entrance. |
| `name` | `string` | Yes | DataCenter datasource name. It must be legal and unique in the relevant product/global namespace checks. |
| `type` | `string` | Yes | Datasource type. Supported backend values include `hive`, `kafka`, `rocketmq`, `rpc`, `abase`, `index_service`, `redis`, and `paimon`. |
| `data_type` | `string` | Kafka/RocketMQ | Message payload format for Kafka or RocketMQ. Supported values are `json` and `pb`. |
| `schema_name` | `string` | Kafka/RocketMQ PB | Existing DataCenter schema name to bind to a PB Kafka or RocketMQ datasource. |
| `schema_product` | `string` | No | Product that owns `schema_name`; defaults to request `product` if omitted. |
| `eu` | `object` | Conditional | Region-specific physical configuration block for `eu`. This import template only includes `eu` and `ttp`. |
| `eu.kafka_config` | `object` | For `kafka` in `eu` | Kafka/BMQ physical config. |
| `eu.kafka_config.cluster` | `string` | For `kafka` in `eu` | Kafka/BMQ cluster name. |
| `eu.kafka_config.topic` | `string` | For `kafka` in `eu` | Kafka/BMQ topic name. |
| `eu.hive_config` | `object` | For `hive` in `eu` | Hive physical config. |
| `eu.hive_config.database` | `string` | For `hive` in `eu` | Hive database name. |
| `eu.hive_config.table` | `string` | For `hive` in `eu` | Hive table name. |
| `eu.rocketmq_config` | `object` | For `rocketmq` in `eu` | RocketMQ physical config. |
| `eu.rocketmq_config.cluster` | `string` | For `rocketmq` in `eu` | RocketMQ cluster name. |
| `eu.rocketmq_config.topic` | `string` | For `rocketmq` in `eu` | RocketMQ topic name. |
| `eu.rpc_config` | `object` | For `rpc` in `eu` | RPC physical config. |
| `eu.rpc_config.psm` | `string` | For `rpc` in `eu` | RPC PSM or consul identity. |
| `eu.rpc_config.service_class` | `string` | For `rpc` in `eu` | Thrift service class. |
| `eu.rpc_config.method` | `string` | For `rpc` in `eu` | Thrift method name. |
| `eu.rpc_config.cluster` | `string` | No | Optional RPC cluster. |
| `eu.abase_config` | `object` | For `abase` in `eu` | Abase physical config. |
| `eu.abase_config.psm` | `string` | For `abase` in `eu` | Abase PSM. |
| `eu.abase_config.table` | `string` | For `abase` in `eu` | Abase table name. |
| `eu.index_service_config` | `object` | For `index_service` in `eu` | IndexService physical config. |
| `eu.index_service_config.psm` | `string` | For `index_service` in `eu` | IndexService PSM. |
| `eu.index_service_config.index_name` | `string` | For `index_service` in `eu` | IndexService index name. |
| `eu.redis_config` | `object` | For `redis` in `eu` | Redis physical config. |
| `eu.redis_config.cluster` | `string` | For `redis` in `eu` | Redis cluster name. |
| `eu.paimon_config` | `object` | For `paimon` in `eu` | Paimon physical config. |
| `eu.paimon_config.database` | `string` | For `paimon` in `eu` | Paimon database name. |
| `eu.paimon_config.table` | `string` | For `paimon` in `eu` | Paimon table name. |
| `eu.extra_config` | `array` | No | Additional datasource options. Duplicate check compares these options when provided. |
| `eu.extra_config[].name` | `string` | No | Extra option key. |
| `eu.extra_config[].value` | `string` | No | Extra option value. |
| `ttp` | `object` | Conditional | Region-specific physical configuration block for `ttp`. This import template only includes `eu` and `ttp`. |
| `ttp.kafka_config` | `object` | For `kafka` in `ttp` | Kafka/BMQ physical config. |
| `ttp.kafka_config.cluster` | `string` | For `kafka` in `ttp` | Kafka/BMQ cluster name. |
| `ttp.kafka_config.topic` | `string` | For `kafka` in `ttp` | Kafka/BMQ topic name. |
| `ttp.hive_config` | `object` | For `hive` in `ttp` | Hive physical config. |
| `ttp.hive_config.database` | `string` | For `hive` in `ttp` | Hive database name. |
| `ttp.hive_config.table` | `string` | For `hive` in `ttp` | Hive table name. |
| `ttp.rocketmq_config` | `object` | For `rocketmq` in `ttp` | RocketMQ physical config. |
| `ttp.rocketmq_config.cluster` | `string` | For `rocketmq` in `ttp` | RocketMQ cluster name. |
| `ttp.rocketmq_config.topic` | `string` | For `rocketmq` in `ttp` | RocketMQ topic name. |
| `ttp.rpc_config` | `object` | For `rpc` in `ttp` | RPC physical config. |
| `ttp.rpc_config.psm` | `string` | For `rpc` in `ttp` | RPC PSM or consul identity. |
| `ttp.rpc_config.service_class` | `string` | For `rpc` in `ttp` | Thrift service class. |
| `ttp.rpc_config.method` | `string` | For `rpc` in `ttp` | Thrift method name. |
| `ttp.rpc_config.cluster` | `string` | No | Optional RPC cluster. |
| `ttp.abase_config` | `object` | For `abase` in `ttp` | Abase physical config. |
| `ttp.abase_config.psm` | `string` | For `abase` in `ttp` | Abase PSM. |
| `ttp.abase_config.table` | `string` | For `abase` in `ttp` | Abase table name. |
| `ttp.index_service_config` | `object` | For `index_service` in `ttp` | IndexService physical config. |
| `ttp.index_service_config.psm` | `string` | For `index_service` in `ttp` | IndexService PSM. |
| `ttp.index_service_config.index_name` | `string` | For `index_service` in `ttp` | IndexService index name. |
| `ttp.redis_config` | `object` | For `redis` in `ttp` | Redis physical config. |
| `ttp.redis_config.cluster` | `string` | For `redis` in `ttp` | Redis cluster name. |
| `ttp.paimon_config` | `object` | For `paimon` in `ttp` | Paimon physical config. |
| `ttp.paimon_config.database` | `string` | For `paimon` in `ttp` | Paimon database name. |
| `ttp.paimon_config.table` | `string` | For `paimon` in `ttp` | Paimon table name. |
| `ttp.extra_config` | `array` | No | Additional datasource options. Duplicate check compares these options when provided. |
| `ttp.extra_config[].name` | `string` | No | Extra option key. |
| `ttp.extra_config[].value` | `string` | No | Extra option value. |

Import JSON:

```json
[
  {
    "fieldName": "product",
    "type": "string",
    "description": "Product or DataCenter workspace that owns the datasource.",
    "compliance_tag": {}
  },
  {
    "fieldName": "name",
    "type": "string",
    "description": "DataCenter datasource name. It must be legal and unique in the relevant product/global namespace checks.",
    "compliance_tag": {}
  },
  {
    "fieldName": "type",
    "type": "string",
    "description": "Datasource type. Supported backend values include hive, kafka, rocketmq, rpc, abase, index_service, redis, and paimon.",
    "compliance_tag": {}
  },
  {
    "fieldName": "data_type",
    "type": "string",
    "description": "Message payload format for Kafka or RocketMQ. Supported values are json and pb.",
    "compliance_tag": {}
  },
  {
    "fieldName": "schema_name",
    "type": "string",
    "description": "Existing DataCenter schema name to bind to a PB Kafka or RocketMQ datasource.",
    "compliance_tag": {}
  },
  {
    "fieldName": "schema_product",
    "type": "string",
    "description": "Product that owns schema_name; defaults to request product if omitted.",
    "compliance_tag": {}
  },
  {
    "fieldName": "eu",
    "type": "object",
    "description": "Region-specific physical configuration block for eu. Only eu and ttp are included in this import template.",
    "compliance_tag": null,
    "children": [
      {
        "fieldName": "kafka_config",
        "type": "object",
        "description": "Kafka/BMQ physical config. Used when type is kafka.",
        "compliance_tag": null,
        "children": [
          {
            "fieldName": "cluster",
            "type": "string",
            "description": "Kafka/BMQ cluster name.",
            "compliance_tag": {}
          },
          {
            "fieldName": "topic",
            "type": "string",
            "description": "Kafka/BMQ topic name.",
            "compliance_tag": {}
          }
        ]
      },
      {
        "fieldName": "hive_config",
        "type": "object",
        "description": "Hive physical config. Used when type is hive.",
        "compliance_tag": null,
        "children": [
          {
            "fieldName": "database",
            "type": "string",
            "description": "Hive database name.",
            "compliance_tag": {}
          },
          {
            "fieldName": "table",
            "type": "string",
            "description": "Hive table name.",
            "compliance_tag": {}
          }
        ]
      },
      {
        "fieldName": "rocketmq_config",
        "type": "object",
        "description": "RocketMQ physical config. Used when type is rocketmq.",
        "compliance_tag": null,
        "children": [
          {
            "fieldName": "cluster",
            "type": "string",
            "description": "RocketMQ cluster name.",
            "compliance_tag": {}
          },
          {
            "fieldName": "topic",
            "type": "string",
            "description": "RocketMQ topic name.",
            "compliance_tag": {}
          }
        ]
      },
      {
        "fieldName": "rpc_config",
        "type": "object",
        "description": "RPC physical config. Used when type is rpc.",
        "compliance_tag": null,
        "children": [
          {
            "fieldName": "psm",
            "type": "string",
            "description": "RPC PSM or consul identity.",
            "compliance_tag": {}
          },
          {
            "fieldName": "service_class",
            "type": "string",
            "description": "Thrift service class.",
            "compliance_tag": {}
          },
          {
            "fieldName": "method",
            "type": "string",
            "description": "Thrift method name.",
            "compliance_tag": {}
          },
          {
            "fieldName": "cluster",
            "type": "string",
            "description": "Optional RPC cluster.",
            "compliance_tag": {}
          }
        ]
      },
      {
        "fieldName": "abase_config",
        "type": "object",
        "description": "Abase physical config. Used when type is abase.",
        "compliance_tag": null,
        "children": [
          {
            "fieldName": "psm",
            "type": "string",
            "description": "Abase PSM.",
            "compliance_tag": {}
          },
          {
            "fieldName": "table",
            "type": "string",
            "description": "Abase table name.",
            "compliance_tag": {}
          }
        ]
      },
      {
        "fieldName": "index_service_config",
        "type": "object",
        "description": "IndexService physical config. Used when type is index_service.",
        "compliance_tag": null,
        "children": [
          {
            "fieldName": "psm",
            "type": "string",
            "description": "IndexService PSM.",
            "compliance_tag": {}
          },
          {
            "fieldName": "index_name",
            "type": "string",
            "description": "IndexService index name.",
            "compliance_tag": {}
          }
        ]
      },
      {
        "fieldName": "redis_config",
        "type": "object",
        "description": "Redis physical config. Used when type is redis.",
        "compliance_tag": null,
        "children": [
          {
            "fieldName": "cluster",
            "type": "string",
            "description": "Redis cluster name.",
            "compliance_tag": {}
          }
        ]
      },
      {
        "fieldName": "paimon_config",
        "type": "object",
        "description": "Paimon physical config. Used when type is paimon.",
        "compliance_tag": null,
        "children": [
          {
            "fieldName": "database",
            "type": "string",
            "description": "Paimon database name.",
            "compliance_tag": {}
          },
          {
            "fieldName": "table",
            "type": "string",
            "description": "Paimon table name.",
            "compliance_tag": {}
          }
        ]
      },
      {
        "fieldName": "extra_config",
        "type": "array",
        "description": "Additional datasource options. Duplicate check compares these options when provided.",
        "compliance_tag": null,
        "children": [
          {
            "fieldName": "items",
            "type": "object",
            "description": "Array item for extra_config.",
            "compliance_tag": null,
            "children": [
              {
                "fieldName": "name",
                "type": "string",
                "description": "Extra option key.",
                "compliance_tag": {}
              },
              {
                "fieldName": "value",
                "type": "string",
                "description": "Extra option value.",
                "compliance_tag": {}
              }
            ]
          }
        ]
      }
    ]
  },
  {
    "fieldName": "ttp",
    "type": "object",
    "description": "Region-specific physical configuration block for ttp. Only eu and ttp are included in this import template.",
    "compliance_tag": null,
    "children": [
      {
        "fieldName": "kafka_config",
        "type": "object",
        "description": "Kafka/BMQ physical config. Used when type is kafka.",
        "compliance_tag": null,
        "children": [
          {
            "fieldName": "cluster",
            "type": "string",
            "description": "Kafka/BMQ cluster name.",
            "compliance_tag": {}
          },
          {
            "fieldName": "topic",
            "type": "string",
            "description": "Kafka/BMQ topic name.",
            "compliance_tag": {}
          }
        ]
      },
      {
        "fieldName": "hive_config",
        "type": "object",
        "description": "Hive physical config. Used when type is hive.",
        "compliance_tag": null,
        "children": [
          {
            "fieldName": "database",
            "type": "string",
            "description": "Hive database name.",
            "compliance_tag": {}
          },
          {
            "fieldName": "table",
            "type": "string",
            "description": "Hive table name.",
            "compliance_tag": {}
          }
        ]
      },
      {
        "fieldName": "rocketmq_config",
        "type": "object",
        "description": "RocketMQ physical config. Used when type is rocketmq.",
        "compliance_tag": null,
        "children": [
          {
            "fieldName": "cluster",
            "type": "string",
            "description": "RocketMQ cluster name.",
            "compliance_tag": {}
          },
          {
            "fieldName": "topic",
            "type": "string",
            "description": "RocketMQ topic name.",
            "compliance_tag": {}
          }
        ]
      },
      {
        "fieldName": "rpc_config",
        "type": "object",
        "description": "RPC physical config. Used when type is rpc.",
        "compliance_tag": null,
        "children": [
          {
            "fieldName": "psm",
            "type": "string",
            "description": "RPC PSM or consul identity.",
            "compliance_tag": {}
          },
          {
            "fieldName": "service_class",
            "type": "string",
            "description": "Thrift service class.",
            "compliance_tag": {}
          },
          {
            "fieldName": "method",
            "type": "string",
            "description": "Thrift method name.",
            "compliance_tag": {}
          },
          {
            "fieldName": "cluster",
            "type": "string",
            "description": "Optional RPC cluster.",
            "compliance_tag": {}
          }
        ]
      },
      {
        "fieldName": "abase_config",
        "type": "object",
        "description": "Abase physical config. Used when type is abase.",
        "compliance_tag": null,
        "children": [
          {
            "fieldName": "psm",
            "type": "string",
            "description": "Abase PSM.",
            "compliance_tag": {}
          },
          {
            "fieldName": "table",
            "type": "string",
            "description": "Abase table name.",
            "compliance_tag": {}
          }
        ]
      },
      {
        "fieldName": "index_service_config",
        "type": "object",
        "description": "IndexService physical config. Used when type is index_service.",
        "compliance_tag": null,
        "children": [
          {
            "fieldName": "psm",
            "type": "string",
            "description": "IndexService PSM.",
            "compliance_tag": {}
          },
          {
            "fieldName": "index_name",
            "type": "string",
            "description": "IndexService index name.",
            "compliance_tag": {}
          }
        ]
      },
      {
        "fieldName": "redis_config",
        "type": "object",
        "description": "Redis physical config. Used when type is redis.",
        "compliance_tag": null,
        "children": [
          {
            "fieldName": "cluster",
            "type": "string",
            "description": "Redis cluster name.",
            "compliance_tag": {}
          }
        ]
      },
      {
        "fieldName": "paimon_config",
        "type": "object",
        "description": "Paimon physical config. Used when type is paimon.",
        "compliance_tag": null,
        "children": [
          {
            "fieldName": "database",
            "type": "string",
            "description": "Paimon database name.",
            "compliance_tag": {}
          },
          {
            "fieldName": "table",
            "type": "string",
            "description": "Paimon table name.",
            "compliance_tag": {}
          }
        ]
      },
      {
        "fieldName": "extra_config",
        "type": "array",
        "description": "Additional datasource options. Duplicate check compares these options when provided.",
        "compliance_tag": null,
        "children": [
          {
            "fieldName": "items",
            "type": "object",
            "description": "Array item for extra_config.",
            "compliance_tag": null,
            "children": [
              {
                "fieldName": "name",
                "type": "string",
                "description": "Extra option key.",
                "compliance_tag": {}
              },
              {
                "fieldName": "value",
                "type": "string",
                "description": "Extra option value.",
                "compliance_tag": {}
              }
            ]
          }
        ]
      }
    ]
  }
]
```

### Response Example

```json
{
  "code": 0,
  "data": {
    "has_duplicate": true,
    "duplicate_name": "existing_datasource_name"
  },
  "isDataToTCC": false
}
```

### Response Fields

| Field | Type | Description |
|---|---|---|
| `code` | `integer` | Business status code returned by the ByteRec wrapper. `0` means the request succeeded. |
| `data` | `object` | Duplicate-check result payload. |
| `data.has_duplicate` | `boolean` | `true` when another datasource in the same product has the same physical config and matching extra options. |
| `data.duplicate_name` | `string` | Name of the existing datasource to reuse when `has_duplicate` is `true`. This field may be absent when no duplicate exists. |
| `isDataToTCC` | `boolean` | Wrapper flag indicating whether the response data is dynamic/TCC-style data. |

Import JSON:

```json
[
  {
    "fieldName": "code",
    "type": "integer",
    "description": "Business status code returned by the ByteRec wrapper. 0 means the request succeeded.",
    "compliance_tag": {}
  },
  {
    "fieldName": "data",
    "type": "object",
    "description": "Duplicate-check result payload.",
    "compliance_tag": null,
    "children": [
      {
        "fieldName": "has_duplicate",
        "type": "boolean",
        "description": "Whether an existing datasource has the same physical config and matching extra options.",
        "compliance_tag": {}
      },
      {
        "fieldName": "duplicate_name",
        "type": "string",
        "description": "Name of the existing datasource to reuse when has_duplicate is true.",
        "compliance_tag": {}
      }
    ]
  },
  {
    "fieldName": "isDataToTCC",
    "type": "boolean",
    "description": "Wrapper flag indicating whether the response data is dynamic/TCC-style data.",
    "compliance_tag": {}
  }
]
```

## `GET /openapi/restful/darwin_api/group_config/diff`

Purpose: Return old/new generated Darwin platform config for a feature group.

### Query Params

| Field | Type | Required | Description |
|---|---|---|---|
| `caller_name` | `string` | Yes | http_query_params: caller_name |
| `caller_token` | `string` | Yes | http_query_params: caller_token |
| `group_name` | `string` | No | Darwin feature group name to inspect. Either `group_name` or a positive `group_id` must identify an existing task. |
| `group_id` | `integer` | No | Darwin feature group database id. Used as an alternative lookup key when `group_name` is not provided. |
| `op_region` | `string` | No | Region to generate config for. Supports comma-separated regions. If omitted, the task's `group_region` is used. |

Import JSON:

```json
[
  {
    "fieldName": "caller_name",
    "type": "string",
    "description": "http_query_params: caller_name"
  },
  {
    "fieldName": "caller_token",
    "type": "string",
    "description": "http_query_params: caller_token"
  },
  {
    "fieldName": "group_name",
    "type": "string",
    "description": "Darwin feature group name to inspect. Either group_name or a positive group_id must identify an existing task."
  },
  {
    "fieldName": "group_id",
    "type": "integer",
    "description": "Darwin feature group database id. Used as an alternative lookup key when group_name is not provided."
  },
  {
    "fieldName": "op_region",
    "type": "string",
    "description": "Region to generate config for. Supports comma-separated regions. If omitted, the task's group_region is used."
  }
]
```

### Path Params

None.

Import JSON:

```json
[]
```

### Headers

| Field | Type | Required | Description |
|---|---|---|---|
| `Locale` | `string` | No | Language hint for localized error messages, for example `zh` or `en`. |
| `x-tt-env` | `string` | No | PPE environment routing header. Used only when the client intentionally calls a PPE environment. |
| `x-use-ppe` | `string` | No | PPE switch header. Usually set to `1` together with `x-tt-env` for PPE requests. |

Import JSON:

```json
[
  {
    "fieldName": "Locale",
    "type": "string",
    "description": "Language hint for localized error messages, for example zh or en."
  },
  {
    "fieldName": "x-tt-env",
    "type": "string",
    "description": "PPE environment routing header. Used only when the client intentionally calls a PPE environment."
  },
  {
    "fieldName": "x-use-ppe",
    "type": "string",
    "description": "PPE switch header. Usually set to 1 together with x-tt-env for PPE requests."
  }
]
```

### Body

None.

Import JSON:

```json
[]
```

### Response Example

```json
{
  "code": 0,
  "data": {
    "eu": {
      "v1": "old yaml/config text",
      "v2": "new yaml/config text"
    }
  },
  "isDataToTCC": false
}
```

### Response Fields

| Field | Type | Description |
|---|---|---|
| `code` | `integer` | Business status code returned by the ByteRec wrapper. `0` means the request succeeded. |
| `data` | `map` | Map from region key to generated config diff for that region. |
| `data.<region>.v1` | `string` | Previously saved or latest started config. For `cli` and `dc_cli` tasks this may be an empty string. |
| `data.<region>.v2` | `string` | Newly generated platform config. For `cli` and `dc_cli` tasks this may be an empty string. |
| `isDataToTCC` | `boolean` | Wrapper flag indicating whether the response data is dynamic/TCC-style data. |

Import JSON:

```json
[
  {
    "fieldName": "code",
    "type": "integer",
    "description": "Business status code returned by the ByteRec wrapper. 0 means the request succeeded.",
    "compliance_tag": {}
  },
  {
    "fieldName": "data",
    "type": "object",
    "description": "Map from region key to generated config diff for that region. The example child uses eu as the region key.",
    "compliance_tag": null,
    "children": [
      {
        "fieldName": "eu",
        "type": "object",
        "description": "Example region config diff object. Replace eu with the actual region key.",
        "compliance_tag": null,
        "children": [
          {
            "fieldName": "v1",
            "type": "string",
            "description": "Previously saved or latest started config.",
            "compliance_tag": {}
          },
          {
            "fieldName": "v2",
            "type": "string",
            "description": "Newly generated platform config.",
            "compliance_tag": {}
          }
        ]
      }
    ]
  },
  {
    "fieldName": "isDataToTCC",
    "type": "boolean",
    "description": "Wrapper flag indicating whether the response data is dynamic/TCC-style data.",
    "compliance_tag": {}
  }
]
```

## `POST /openapi/subsys/data_center/data_schema`

Purpose: Create a DataCenter datasource schema. Current migration flow uses it for PB schema.

### Query Params

| Field | Type | Required | Description |
|---|---|---|---|
| `caller_name` | `string` | Yes | http_query_params: caller_name |
| `caller_token` | `string` | Yes | http_query_params: caller_token |

Import JSON:

```json
[
  {
    "fieldName": "caller_name",
    "type": "string",
    "description": "http_query_params: caller_name"
  },
  {
    "fieldName": "caller_token",
    "type": "string",
    "description": "http_query_params: caller_token"
  }
]
```

### Path Params

None.

Import JSON:

```json
[]
```

### Headers

| Field | Type | Required | Description |
|---|---|---|---|
| `x-xcenter-entrance` | `string` | No | XCenter entrance URI. If provided, the backend derives the actual product from this entrance instead of trusting only the body `product`. |
| `Locale` | `string` | No | Language hint for localized error messages, for example `zh` or `en`. |
| `x-tt-env` | `string` | No | PPE environment routing header. Used only when the client intentionally calls a PPE environment. |
| `x-use-ppe` | `string` | No | PPE switch header. Usually set to `1` together with `x-tt-env` for PPE requests. |

Import JSON:

```json
[
  {
    "fieldName": "x-xcenter-entrance",
    "type": "string",
    "description": "XCenter entrance URI. If provided, the backend derives the actual product from this entrance instead of trusting only the body product."
  },
  {
    "fieldName": "Locale",
    "type": "string",
    "description": "Language hint for localized error messages, for example zh or en."
  },
  {
    "fieldName": "x-tt-env",
    "type": "string",
    "description": "PPE environment routing header. Used only when the client intentionally calls a PPE environment."
  },
  {
    "fieldName": "x-use-ppe",
    "type": "string",
    "description": "PPE switch header. Usually set to 1 together with x-tt-env for PPE requests."
  }
]
```

### Body Example

```json
{
  "product": "tiktok",
  "name": "com.example.Demo",
  "type": "pb",
  "description": "Schema for datasource demo_source",
  "pb_config": {
    "enter_message": "com.example.Demo",
    "syntax": "proto2",
    "package": "com.example",
    "java_package": "com.example",
    "java_outer_class_name": "DemoOuterClass",
    "pb_content": "syntax = \"proto2\"; message Demo { optional string id = 1; }",
    "custom_fields": [
      {"name": "id", "data_type": "String"}
    ]
  }
}
```

### Body Fields

| Field | Type | Required | Description |
|---|---|---|---|
| `product` | `string` | Yes | Product or DataCenter workspace that owns the schema. If `x-xcenter-entrance` is set, the backend resolves product from that entrance. |
| `name` | `string` | Yes | DataCenter schema name. It must pass backend name validation and must not already exist in Darwin schema storage. |
| `type` | `string` | Yes | Schema type. The handler supports `pb` through `DataSchemaType.PB`. |
| `description` | `string` | No | Human-readable description stored with the schema metadata. |
| `pb_config` | `object` | For PB | Protobuf schema configuration used to create both DataCenter schema meta and synchronized Darwin schema. |
| `pb_config.enter_message` | `string` | Yes | Protobuf entry message class/name used as the root message for parsing fields. |
| `pb_config.syntax` | `string` | Yes | Protobuf syntax version, such as `proto2` or `proto3`. |
| `pb_config.package` | `string` | Yes | Protobuf package declared in the proto file. |
| `pb_config.java_package` | `string` | No | Java package option from the proto file. Stored as schema metadata. |
| `pb_config.java_outer_class_name` | `string` | No | Java outer class option from the proto file. Stored as schema metadata. |
| `pb_config.pb_content` | `string` | Yes | Raw `.proto` text. The backend uses it to create or synchronize Darwin schema fields. |
| `pb_config.custom_fields` | `array` | No | Flattened field list. The handler also accepts a map and converts it to this list format. |
| `pb_config.custom_fields[].name` | `string` | Yes | Flattened field name, for example `id` or `user.profile.age`. |
| `pb_config.custom_fields[].data_type` | `string` | Yes | DataCenter/Monarch field type string for the flattened field. |

Import JSON:

```json
[
  {
    "fieldName": "product",
    "type": "string",
    "description": "Product or DataCenter workspace that owns the schema.",
    "compliance_tag": {}
  },
  {
    "fieldName": "name",
    "type": "string",
    "description": "DataCenter schema name.",
    "compliance_tag": {}
  },
  {
    "fieldName": "type",
    "type": "string",
    "description": "Schema type. The handler supports pb.",
    "compliance_tag": {}
  },
  {
    "fieldName": "description",
    "type": "string",
    "description": "Human-readable description stored with the schema metadata.",
    "compliance_tag": {}
  },
  {
    "fieldName": "pb_config",
    "type": "object",
    "description": "Protobuf schema configuration.",
    "compliance_tag": null,
    "children": [
      {
        "fieldName": "enter_message",
        "type": "string",
        "description": "Protobuf entry message class/name used as the root message.",
        "compliance_tag": {}
      },
      {
        "fieldName": "syntax",
        "type": "string",
        "description": "Protobuf syntax version, such as proto2 or proto3.",
        "compliance_tag": {}
      },
      {
        "fieldName": "package",
        "type": "string",
        "description": "Protobuf package declared in the proto file.",
        "compliance_tag": {}
      },
      {
        "fieldName": "java_package",
        "type": "string",
        "description": "Java package option from the proto file.",
        "compliance_tag": {}
      },
      {
        "fieldName": "java_outer_class_name",
        "type": "string",
        "description": "Java outer class option from the proto file.",
        "compliance_tag": {}
      },
      {
        "fieldName": "pb_content",
        "type": "string",
        "description": "Raw .proto text.",
        "compliance_tag": {}
      },
      {
        "fieldName": "custom_fields",
        "type": "array",
        "description": "Flattened schema fields.",
        "compliance_tag": null,
        "children": [
          {
            "fieldName": "items",
            "type": "object",
            "description": "Array item for custom_fields.",
            "compliance_tag": null,
            "children": [
              {
                "fieldName": "name",
                "type": "string",
                "description": "Flattened field name.",
                "compliance_tag": {}
              },
              {
                "fieldName": "data_type",
                "type": "string",
                "description": "DataCenter/Monarch field type string.",
                "compliance_tag": {}
              }
            ]
          }
        ]
      }
    ]
  }
]
```

### Response Example

```json
{
  "code": 0,
  "data": {},
  "isDataToTCC": false
}
```

### Response Fields

| Field | Type | Description |
|---|---|---|
| `code` | `integer` | Business status code returned by the ByteRec wrapper. `0` means the schema was created successfully. |
| `data` | `object` | Empty object on success; errors are returned through the common error wrapper. |
| `isDataToTCC` | `boolean` | Wrapper flag indicating whether the response data is dynamic/TCC-style data. |

Import JSON:

```json
[
  {
    "fieldName": "code",
    "type": "integer",
    "description": "Business status code returned by the ByteRec wrapper. 0 means the schema was created successfully.",
    "compliance_tag": {}
  },
  {
    "fieldName": "isDataToTCC",
    "type": "boolean",
    "description": "Wrapper flag indicating whether the response data is dynamic/TCC-style data.",
    "compliance_tag": {}
  }
]
```

## `POST /openapi/subsys/data_center/task`

Purpose: Create a DataCenter task metadata object.

### Query Params

| Field | Type | Required | Description |
|---|---|---|---|
| `caller_name` | `string` | Yes | http_query_params: caller_name |
| `caller_token` | `string` | Yes | http_query_params: caller_token |

Import JSON:

```json
[
  {
    "fieldName": "caller_name",
    "type": "string",
    "description": "http_query_params: caller_name"
  },
  {
    "fieldName": "caller_token",
    "type": "string",
    "description": "http_query_params: caller_token"
  }
]
```

### Path Params

None.

Import JSON:

```json
[]
```

### Headers

| Field | Type | Required | Description |
|---|---|---|---|
| `x-xcenter-entrance` | `string` | No | XCenter entrance URI. If provided, the backend derives the actual product from this entrance instead of trusting only the body `product`. |
| `Locale` | `string` | No | Language hint for localized error messages, for example `zh` or `en`. |
| `x-tt-env` | `string` | No | PPE environment routing header. Used only when the client intentionally calls a PPE environment. |
| `x-use-ppe` | `string` | No | PPE switch header. Usually set to `1` together with `x-tt-env` for PPE requests. |

Import JSON:

```json
[
  {
    "fieldName": "x-xcenter-entrance",
    "type": "string",
    "description": "XCenter entrance URI. If provided, the backend derives the actual product from this entrance instead of trusting only the body product."
  },
  {
    "fieldName": "Locale",
    "type": "string",
    "description": "Language hint for localized error messages, for example zh or en."
  },
  {
    "fieldName": "x-tt-env",
    "type": "string",
    "description": "PPE environment routing header. Used only when the client intentionally calls a PPE environment."
  },
  {
    "fieldName": "x-use-ppe",
    "type": "string",
    "description": "PPE switch header. Usually set to 1 together with x-tt-env for PPE requests."
  }
]
```

### Body Example

```json
{
  "product": "tiktok",
  "task_name": "lemon8_demo_task_dc",
  "task_type": "stream_window",
  "profile_type": "group",
  "entity_uri": "meta_center_eu_ttp://entity/tiktok/tiktok_lemon8article",
  "description": "Migrated from Darwin: lemon8_demo_task",
  "region": "eu",
  "owners": ["user.name"],
  "business_line": "lemon8_rec",
  "doc_url": "",
  "update_mode": "upsert"
}
```

### Body Fields

| Field | Type | Required | Description |
|---|---|---|---|
| `product` | `string` | Yes | Product or DataCenter workspace that owns the task. If `x-xcenter-entrance` is set, the backend resolves product from that entrance. |
| `task_name` | `string` | Yes | New DataCenter task name. It must be legal, globally unique, and not already present in DataCenter/Darwin where checked. |
| `task_type` | `string` | Yes | DataCenter task type. The backend stores this in `spec.type` and uses it to choose task behavior. |
| `profile_type` | `string` | Usually | Serving/profile mode stored in `spec.serving_modes`. Required for non-specific entrances. |
| `entity_uri` | `string` | Yes | MetaCenter entity URI. The backend validates that this entity meta exists before creating the task. |
| `description` | `string` | Yes | Human-readable task description stored on the DataCenter DSL meta. |
| `region` | `string` | No | Initial task region. For standard tasks, it initializes `multi_region_running_status` and `multi_region_info`. |
| `owners` | `array` | No | Task owner names. If the request context has no username, the first owner can be used as creator fallback. |
| `business_line` | `string` | No | Business line tag stored in `spec.business_line` for filtering and ownership context. |
| `doc_url` | `string` | No | Documentation URL stored in `spec.doc_url`. |
| `sequence_config` | `object` | Sequence only | Additional config required only when `task_type` is `user_behavior_sequence`. |
| `sequence_config.sequence_production_type` | `string` | Sequence only | Sequence production mode. The backend validates this against `SequenceProductionType` enum names. |
| `sequence_config.target_entities` | `array` | Sequence only | Target entity list for a user behavior sequence task. |
| `operator_lib_uri` | `string` | No | Operator library URI for external-access operators; stored in metadata tags when provided. |
| `update_mode` | `string` | No | Data write mode stored in `spec.update_mode`; handler accepts `upsert` and `overwrite`. |

Import JSON:

```json
[
  {
    "fieldName": "product",
    "type": "string",
    "description": "Product or DataCenter workspace that owns the task.",
    "compliance_tag": {}
  },
  {
    "fieldName": "task_name",
    "type": "string",
    "description": "New DataCenter task name.",
    "compliance_tag": {}
  },
  {
    "fieldName": "task_type",
    "type": "string",
    "description": "DataCenter task type.",
    "compliance_tag": {}
  },
  {
    "fieldName": "profile_type",
    "type": "string",
    "description": "Serving/profile mode stored in spec.serving_modes.",
    "compliance_tag": {}
  },
  {
    "fieldName": "entity_uri",
    "type": "string",
    "description": "MetaCenter entity URI.",
    "compliance_tag": {}
  },
  {
    "fieldName": "description",
    "type": "string",
    "description": "Human-readable task description.",
    "compliance_tag": {}
  },
  {
    "fieldName": "region",
    "type": "string",
    "description": "Initial task region.",
    "compliance_tag": {}
  },
  {
    "fieldName": "owners",
    "type": "array",
    "description": "Task owner names.",
    "compliance_tag": null,
    "children": [
      {
        "fieldName": "items",
        "type": "string",
        "description": "Owner name item.",
        "compliance_tag": {}
      }
    ]
  },
  {
    "fieldName": "business_line",
    "type": "string",
    "description": "Business line tag stored in spec.business_line.",
    "compliance_tag": {}
  },
  {
    "fieldName": "doc_url",
    "type": "string",
    "description": "Documentation URL stored in spec.doc_url.",
    "compliance_tag": {}
  },
  {
    "fieldName": "sequence_config",
    "type": "object",
    "description": "Additional config required only for user_behavior_sequence tasks.",
    "compliance_tag": null,
    "children": [
      {
        "fieldName": "sequence_production_type",
        "type": "string",
        "description": "Sequence production mode. The backend validates this against SequenceProductionType enum names.",
        "compliance_tag": {}
      },
      {
        "fieldName": "target_entities",
        "type": "array",
        "description": "Target entity list for a user behavior sequence task.",
        "compliance_tag": null,
        "children": [
          {
            "fieldName": "items",
            "type": "string",
            "description": "Target entity item.",
            "compliance_tag": {}
          }
        ]
      }
    ]
  },
  {
    "fieldName": "operator_lib_uri",
    "type": "string",
    "description": "Operator library URI for external-access operators.",
    "compliance_tag": {}
  },
  {
    "fieldName": "update_mode",
    "type": "string",
    "description": "Data write mode. Supports upsert and overwrite.",
    "compliance_tag": {}
  }
]
```

### Response Example

```json
{
  "code": 0,
  "data": {
    "name": "lemon8_demo_task_dc",
    "product": "tiktok",
    "type": "data_center_dsl",
    "description": "Migrated from Darwin: lemon8_demo_task",
    "owners": ["user.name"],
    "uri": "meta_center_eu_ttp://data_center_dsl/tiktok/lemon8_demo_task_dc",
    "version": 1,
    "status": "",
    "spec": {
      "type": "stream_window",
      "entity_uri": "meta_center_eu_ttp://entity/tiktok/tiktok_lemon8article",
      "serving_modes": ["group"],
      "business_line": "lemon8_rec",
      "task_status": "draft",
      "publish_status": "no_ticket",
      "update_mode": "upsert"
    }
  },
  "isDataToTCC": false
}
```

### Response Fields

| Field | Type | Description |
|---|---|---|
| `code` | `integer` | Business status code returned by the ByteRec wrapper. `0` means the task was created successfully. |
| `data` | `object` | Created DataCenter DSL metadata object returned by the meta resource manager. |
| `data.name` | `string` | Created task name. |
| `data.product` | `string` | Product/workspace that owns the task. |
| `data.type` | `string` | Meta resource type. For DataCenter tasks this is usually `data_center_dsl`. |
| `data.description` | `string` | Description stored on the task metadata. |
| `data.owners` | `array` | Owners stored on the task metadata. |
| `data.uri` | `string` | MetaCenter URI of the created DataCenter DSL resource. |
| `data.version` | `integer` | Meta resource version assigned by the metadata system. |
| `data.status` | `string` | Metadata status field from the resource manager. |
| `data.spec` | `object` | DataCenter DSL specification containing task behavior and runtime metadata. |
| `data.spec.type` | `string` | Task type copied from request `task_type`. |
| `data.spec.entity_uri` | `string` | Entity URI copied from the request after validation. |
| `data.spec.serving_modes` | `array` | Serving/profile modes derived from request `profile_type`. |
| `data.spec.business_line` | `string` | Business line copied from the request. |
| `data.spec.task_status` | `string` | DataCenter task lifecycle status initialized by the backend, usually draft. |
| `data.spec.publish_status` | `string` | Publish/workflow status initialized by the backend, usually no-ticket/no-publish state. |
| `data.spec.update_mode` | `string` | Data write mode copied from request `update_mode`. |
| `isDataToTCC` | `boolean` | Wrapper flag indicating whether the response data is dynamic/TCC-style data. |

Import JSON:

```json
[
  {
    "fieldName": "code",
    "type": "integer",
    "description": "Business status code returned by the ByteRec wrapper. 0 means the task was created successfully.",
    "compliance_tag": {}
  },
  {
    "fieldName": "data",
    "type": "object",
    "description": "Created DataCenter DSL metadata object returned by the meta resource manager.",
    "compliance_tag": null,
    "children": [
      {
        "fieldName": "name",
        "type": "string",
        "description": "Created task name.",
        "compliance_tag": {}
      },
      {
        "fieldName": "product",
        "type": "string",
        "description": "Product/workspace that owns the task.",
        "compliance_tag": {}
      },
      {
        "fieldName": "type",
        "type": "string",
        "description": "Meta resource type, usually data_center_dsl.",
        "compliance_tag": {}
      },
      {
        "fieldName": "description",
        "type": "string",
        "description": "Description stored on the task metadata.",
        "compliance_tag": {}
      },
      {
        "fieldName": "owners",
        "type": "array",
        "description": "Owners stored on the task metadata.",
        "compliance_tag": null,
        "children": [
          {
            "fieldName": "items",
            "type": "string",
            "description": "Owner name item.",
            "compliance_tag": {}
          }
        ]
      },
      {
        "fieldName": "uri",
        "type": "string",
        "description": "MetaCenter URI of the created DataCenter DSL resource.",
        "compliance_tag": {}
      },
      {
        "fieldName": "version",
        "type": "integer",
        "description": "Meta resource version assigned by the metadata system.",
        "compliance_tag": {}
      },
      {
        "fieldName": "status",
        "type": "string",
        "description": "Metadata status field from the resource manager.",
        "compliance_tag": {}
      },
      {
        "fieldName": "spec",
        "type": "object",
        "description": "DataCenter DSL specification containing task behavior and runtime metadata.",
        "compliance_tag": null,
        "children": [
          {
            "fieldName": "type",
            "type": "string",
            "description": "Task type copied from request task_type.",
            "compliance_tag": {}
          },
          {
            "fieldName": "entity_uri",
            "type": "string",
            "description": "Entity URI copied from the request after validation.",
            "compliance_tag": {}
          },
          {
            "fieldName": "serving_modes",
            "type": "array",
            "description": "Serving/profile modes derived from request profile_type.",
            "compliance_tag": null,
            "children": [
              {
                "fieldName": "items",
                "type": "string",
                "description": "Serving/profile mode item.",
                "compliance_tag": {}
              }
            ]
          },
          {
            "fieldName": "business_line",
            "type": "string",
            "description": "Business line copied from the request.",
            "compliance_tag": {}
          },
          {
            "fieldName": "task_status",
            "type": "string",
            "description": "DataCenter task lifecycle status initialized by the backend.",
            "compliance_tag": {}
          },
          {
            "fieldName": "publish_status",
            "type": "string",
            "description": "Publish/workflow status initialized by the backend.",
            "compliance_tag": {}
          },
          {
            "fieldName": "update_mode",
            "type": "string",
            "description": "Data write mode copied from request update_mode.",
            "compliance_tag": {}
          }
        ]
      }
    ]
  },
  {
    "fieldName": "isDataToTCC",
    "type": "boolean",
    "description": "Wrapper flag indicating whether the response data is dynamic/TCC-style data.",
    "compliance_tag": {}
  }
]
```

## `POST /openapi/subsys/data_center/dsl`

Purpose: Save DSL source code for a DataCenter task.

### Query Params

| Field | Type | Required | Description |
|---|---|---|---|
| `caller_name` | `string` | Yes | http_query_params: caller_name |
| `caller_token` | `string` | Yes | http_query_params: caller_token |

Import JSON:

```json
[
  {
    "fieldName": "caller_name",
    "type": "string",
    "description": "http_query_params: caller_name"
  },
  {
    "fieldName": "caller_token",
    "type": "string",
    "description": "http_query_params: caller_token"
  }
]
```

### Path Params

None.

Import JSON:

```json
[]
```

### Headers

| Field | Type | Required | Description |
|---|---|---|---|
| `Locale` | `string` | No | Language hint for localized error messages, for example `zh` or `en`. |
| `x-tt-env` | `string` | No | PPE environment routing header. Used only when the client intentionally calls a PPE environment. |
| `x-use-ppe` | `string` | No | PPE switch header. Usually set to `1` together with `x-tt-env` for PPE requests. |

Import JSON:

```json
[
  {
    "fieldName": "Locale",
    "type": "string",
    "description": "Language hint for localized error messages, for example zh or en."
  },
  {
    "fieldName": "x-tt-env",
    "type": "string",
    "description": "PPE environment routing header. Used only when the client intentionally calls a PPE environment."
  },
  {
    "fieldName": "x-use-ppe",
    "type": "string",
    "description": "PPE switch header. Usually set to 1 together with x-tt-env for PPE requests."
  }
]
```

### Body Example

```json
{
  "product": "tiktok",
  "name": "lemon8_demo_task_dc",
  "type": "biz",
  "region": "eu",
  "code": "from monarch.framework import ...\n"
}
```

### Body Fields

| Field | Type | Required | Description |
|---|---|---|---|
| `product` | `string` | Yes | Product or DataCenter workspace that owns the task and DSL file. |
| `name` | `string` | Yes | DataCenter task name. The backend uses `product + name` to locate the task when `uri` is not provided. |
| `uri` | `string` | No | DataCenter DSL meta URI. This can be used as an alternative lookup key to `product + name`. |
| `type` | `string` | Yes | DSL file type. The handler writes the content to `{product}/{type}.py`; common values are `biz` and `arch`. |
| `region` | `string` | No | Region-specific DSL workspace/context. When provided, the code is saved for that region's draft DSL. |
| `code` | `string` | Yes | Full Python DSL source code to save into the target DSL file. |

Import JSON:

```json
[
  {
    "fieldName": "product",
    "type": "string",
    "description": "Product or DataCenter workspace that owns the task and DSL file.",
    "compliance_tag": {}
  },
  {
    "fieldName": "name",
    "type": "string",
    "description": "DataCenter task name.",
    "compliance_tag": {}
  },
  {
    "fieldName": "uri",
    "type": "string",
    "description": "DataCenter DSL meta URI alternative to product plus name.",
    "compliance_tag": {}
  },
  {
    "fieldName": "type",
    "type": "string",
    "description": "DSL file type. Common values are biz and arch.",
    "compliance_tag": {}
  },
  {
    "fieldName": "region",
    "type": "string",
    "description": "Region-specific DSL workspace/context.",
    "compliance_tag": {}
  },
  {
    "fieldName": "code",
    "type": "string",
    "description": "Full Python DSL source code to save.",
    "compliance_tag": {}
  }
]
```

### Response Example

```json
{
  "code": 0,
  "data": {},
  "isDataToTCC": false
}
```

### Response Fields

| Field | Type | Description |
|---|---|---|
| `code` | `integer` | Business status code returned by the ByteRec wrapper. `0` means the DSL file was saved successfully. |
| `data` | `object` | Empty object on success; edit errors are returned through the common error wrapper. |
| `isDataToTCC` | `boolean` | Wrapper flag indicating whether the response data is dynamic/TCC-style data. |

Import JSON:

```json
[
  {
    "fieldName": "code",
    "type": "integer",
    "description": "Business status code returned by the ByteRec wrapper. 0 means the DSL file was saved successfully.",
    "compliance_tag": {}
  },
  {
    "fieldName": "isDataToTCC",
    "type": "boolean",
    "description": "Wrapper flag indicating whether the response data is dynamic/TCC-style data.",
    "compliance_tag": {}
  }
]
```
