# SQL Query Agent

## This AI Agent transforms natural language query into SQL and returns the values in model-json format

### How to use

```
> python -m venv .venv && source ./venv/bin/activate

> pip install -r requiremnts.txt

> python db_agent.py
```

### Performance Estimates

```
Database: SqlLite
Scan: Full Table (10 rows)

Single Table:

Query Generation:   1.75s
Database Call:      2.7s

Table Join:

Query Generation:   1.5s
Database Call:      3.5s
```

### Cost Estimation (model=chatgpt-4o-mini)

```
Single Table:

Task                Input Token     Input Cost      Output Token        OutputCost      Total Cost

Query Generation:   511             $.0075          31                  $.0001          
Database Call:      738             $.001           161                 $.001
                                                                                        $.002/query


Table Join:
Task                Input Token     Input Cost      Output Token        OutputCost      Total Cost

Query Generation:   574             $.008           31                  $.0001          
Database Call:      800             $.001           240                 $.001
                                                                                        $.0021/query
```
