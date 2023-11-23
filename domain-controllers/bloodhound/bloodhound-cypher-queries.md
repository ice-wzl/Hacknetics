# Bloodhound Cypher Queries

#### Return all users&#x20;

```
MATCH (u:User) RETURN u 
```

#### Return all computers&#x20;

```
MATCH (c:Computer) RETURN c
```

#### Return the users with the name containing "ADMIN"

```
MATCH (u:User) WHERE u.name =~ ".ADMIN." RETURN u.name
```

#### Return all the users and the computer they are admin to

```
MATCH p = (u:User)-[:AdminTo]->(c:Computer) RETURN p
```

#### Return the users with the name containing "ADMIN" and the computer they are admin to

```
MATCH p = (u:User)-[:AdminTo]->(c:Computer) WHERE u.name =~ ".ADMIN." RETURN p 
MATCH p=shortestPath((c {owned: true})-[*1..3]->(s)) WHERE NOT c = s RETURN p 
MATCH p=shortestPath((u {highvalue: false})-[1..]->(g:Group {name: 'DOMAIN ADMINS@RASTALABS.LOCAL'})) WHERE NOT (u)-[:MemberOf1..]->(:Group {highvalue: true}) RETURN p
```

#### List all owned users&#x20;

```
MATCH (m:User) WHERE m.owned=TRUE RETURN m
```

#### List all owned computers&#x20;

```
MATCH (m:Computer) WHERE m.owned=TRUE RETURN m
```

#### List all owned groups&#x20;

```
MATCH (m.Group) WHERE m.owned=TRUE RETURN m
```

#### List all high value targets&#x20;

```
MATCH (m) WHERE m.highvalue=TRUE RETURN M
```

#### List the groups of all owned users

```
MATCH (m.User) WHERE m.owned=TRUE WITH m MATCH p=(m) - [:MemberOf*1..] - > (n:Group) RETURN p
```

#### Find all Kerberostable Users

```
MATCH (n:User) WHERE n.hasspn=true RETURN n
```

#### Find all users with an SPN/find all kerberostable users with passwords last set less than 5 years ago&#x20;

```
MATCH (u:User) WHERE u.hasspn=true AND u.pwdlastset < (datetime().epochseconds - (1825 * 86400)) AND NOT u.pwdlastset IN [-1.0, 0.0] RETURN u.name, u.pwdlastset order by u.pwdlastset
```

#### Find kerberostable users with a path to DA

```
MATCH (u:User {hasspn:true}) MATCH (g:Group) WHERE g.objectid ENDS WITH '-512' MATCH p=shortestPath( (u)-[*1..]->(g) ) RETURN p
```

#### Find machines Domain Users can RDP into&#x20;

```
match p(g:Group)-[:CanRDP]->(c:Computer) where g.objectid ENDS WITH '-513' return p
```
