```mermaid
graph TB;
  actor[crm:E39_Actor]
  name[crm:E41_Appellation]
  name_type[crm:E55_Type]
  name_lbl[Marina Celsi]

  actor--crm:P1_is_identified_by-->name
  name--crm:P2_has_type-->name_type
  name--rdfs:label-->name_lbl

  style actor fill:#72005F,stroke:#333,color:#fff
```