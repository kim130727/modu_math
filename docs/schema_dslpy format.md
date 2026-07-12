semantic

{
  "type": "object",
  "properties": {
    "problem_id": {"type": "string"},
    "problem_type": {"type": "string"},
    "metadata": {"type": "object"},
    "domain": {
      "type": "object",
      "properties": {
        "objects": {"type": "array"},
        "relations": {"type": "array"}
      }
    },
    "answer": {"type": "object"}
  },
  "required": ["problem_id", "problem_type", "domain", "answer"]
}


layout

{
  "type": "object",
  "properties": {
    "schema": {
      "type": "string",
      "const": "modu.layout.v1"
    },
    "problem_id": {
      "type": "string"
    },
    "title": {
      "type": "string"
    },
    "canvas": {
      "type": "object",
      "properties": {
        "width": {
          "type": "number"
        },
        "height": {
          "type": "number"
        },
        "coordinate_mode": {
          "type": "string"
        },
        "background": {
          "type": "string"
        }
      },
      "required": [
        "width",
        "height"
      ]
    },
    "regions": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "id": {
            "type": "string"
          },
          "role": {
            "type": "string"
          },
          "flow": {
            "type": "string"
          },
          "slot_ids": {
            "type": "array",
            "items": {
              "type": "string"
            }
          }
        },
        "required": [
          "id",
          "role",
          "flow",
          "slot_ids"
        ]
      }
    },
    "slots": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "id": {
            "type": "string"
          },
          "kind": {
            "type": "string"
          },
          "prompt": {
            "type": "string"
          },
          "content": {
            "type": "object"
          }
        },
        "required": [
          "id",
          "kind",
          "prompt",
          "content"
        ]
      }
    },
    "groups": {
      "type": "array",
      "items": {
        "type": "object"
      }
    },
    "constraints": {
      "type": "array",
      "items": {
        "type": "object"
      }
    },
    "diagrams": {
      "type": "array",
      "items": {
        "type": "object"
      }
    },
    "reading_order": {
      "type": "array",
      "items": {
        "type": "string"
      }
    }
  },
  "required": [
    "schema",
    "problem_id",
    "canvas",
    "regions",
    "slots",
    "groups",
    "constraints",
    "diagrams",
    "reading_order"
  ]
}

renderer

{
  "type": "object",
  "properties": {
    "problem_id": {
      "type": "string"
    },
    "view_box": {
      "type": "object",
      "properties": {
        "width": {
          "type": "number"
        },
        "height": {
          "type": "number"
        },
        "background": {
          "type": "string"
        }
      },
      "required": [
        "width",
        "height"
      ]
    },
    "elements": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "id": {
            "type": "string"
          },
          "type": {
            "type": "string"
          },
          "attributes": {
            "type": "object"
          },
          "text": {
            "type": "string"
          },
          "elements": {
            "type": "array"
          }
        },
        "required": [
          "id",
          "type",
          "attributes"
        ]
      }
    }
  },
  "required": [
    "problem_id",
    "view_box",
    "elements"
  ]
}

solvable

{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "modu.solvable.v1.1.schema.json",
  "title": "Modu Solvable Schema v1.1",
  "type": "object",
  "additionalProperties": false,
  "properties": {
    "schema": {
      "type": "string",
      "const": "modu.solvable.v1.1"
    },
    "problem_id": {
      "type": "string"
    },
    "problem_type": {
      "type": "string"
    },

    "inputs": {
      "type": "object",
      "description": "풀이에 필요한 정규화된 입력값. 문제 유형별 필드를 허용한다.",
      "additionalProperties": true,
      "properties": {
        "target_label": {
          "type": "string",
          "description": "구해야 하는 대상의 사람이 읽을 수 있는 이름"
        },
        "unit": {
          "type": "string",
          "description": "정답 단위. 단위가 없으면 빈 문자열"
        },

        "total_ticks": {
          "type": "number",
          "description": "눈금/전체 개수/전체 길이 계열 문제에서의 전체값"
        },
        "target_ticks": {
          "type": "number",
          "description": "눈금/길이 계열 문제에서 목표 대상의 눈금 수"
        },
        "target_count": {
          "type": "number",
          "description": "개수 세기 계열 문제에서 목표 대상의 개수"
        },

        "sequence_cycle": {
          "type": "array",
          "description": "반복 수열의 한 주기",
          "items": {
            "type": ["number", "string"]
          }
        },
        "cycle_length": {
          "type": "integer",
          "minimum": 1,
          "description": "반복 주기의 길이"
        },
        "target_positions": {
          "type": "array",
          "description": "구해야 하는 항의 위치들",
          "items": {
            "type": "integer",
            "minimum": 1
          }
        },

        "quantities": {
          "type": "object",
          "description": "문장제에서 등장하는 수량값 모음",
          "additionalProperties": {
            "type": ["number", "string", "boolean", "array", "object", "null"]
          }
        },
        "conditions": {
          "type": "array",
          "description": "풀이에 필요한 조건 목록",
          "items": {
            "type": "string"
          }
        }
      },
      "required": [
        "target_label",
        "unit"
      ]
    },

    "given": {
      "type": "array",
      "description": "semantic domain 객체/관계와 연결되는 주어진 정보",
      "items": {
        "type": "object",
        "additionalProperties": false,
        "properties": {
          "ref": {
            "type": "string"
          },
          "value": {}
        },
        "required": [
          "ref",
          "value"
        ]
      }
    },

    "target": {
      "type": "object",
      "description": "구해야 하는 대상",
      "additionalProperties": false,
      "properties": {
        "ref": {
          "type": "string"
        },
        "type": {
          "type": "string"
        }
      },
      "required": [
        "ref",
        "type"
      ]
    },

    "method": {
      "type": "string",
      "description": "대표 풀이 방법"
    },

    "plan": {
      "type": "array",
      "description": "풀이 계획",
      "items": {
        "type": "string"
      }
    },

    "steps": {
      "type": "array",
      "description": "실제 풀이 단계",
      "items": {
        "type": "object",
        "additionalProperties": false,
        "properties": {
          "id": {
            "type": "string"
          },
          "expr": {
            "type": "string"
          },
          "value": {},
          "explanation": {
            "type": "string"
          }
        },
        "required": [
          "id",
          "expr",
          "value"
        ]
      }
    },

    "checks": {
      "type": "array",
      "description": "검산 또는 정합성 체크",
      "items": {
        "type": "object",
        "additionalProperties": false,
        "properties": {
          "id": {
            "type": "string"
          },
          "expr": {
            "type": "string"
          },
          "expected": {},
          "actual": {},
          "pass": {
            "type": "boolean"
          }
        },
        "required": [
          "id",
          "expr",
          "expected",
          "actual",
          "pass"
        ]
      }
    },

    "answer": {
      "type": "object",
      "description": "최종 정답",
      "additionalProperties": true,
      "properties": {
        "value": {},
        "unit": {
          "type": "string"
        }
      },
      "required": [
        "value",
        "unit"
      ]
    }
  },

  "required": [
    "schema",
    "problem_id",
    "problem_type",
    "inputs",
    "given",
    "target",
    "method",
    "plan",
    "steps",
    "checks",
    "answer"
  ]
}
