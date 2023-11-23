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
