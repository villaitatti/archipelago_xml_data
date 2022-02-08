```mermaid
graph TB;
  bw[crm:E22_Man-Made_Object]
  production[crm:E12_Production]
  carried_out_by[crmpc:PC14_carried_out_by]
  actor[crm:E39_Actor]
  role[crm:E55_Type]
  actor_lbl[Baldassarre Longhena]
  role_lbl[Architect]
  
  bw--crm:P108i_was_produced_by-->production
  carried_out_by--crmpc:P01_has_domain-->production
  carried_out_by--crmpc:P02_has_range-->actor
  carried_out_by--crmpc:P14.1_in_the_role_of-->role

  actor--rdfs:label-->actor_lbl
  role--rdfs:label-->role_lbl



  style bw fill:#801401,stroke:#333,color:#fff

  style production fill:#3783A8,stroke:#333,color:#fff
  style carried_out_by fill:#D8D8D8,stroke:#333
  style actor fill:#72005F,stroke:#333,color:#fff
  style role fill:#F88C34,stroke:333,color:#fff

  style role_lbl fill:#fff,stroke:#fff
  style actor_lbl fill:#fff,stroke:#fff
```