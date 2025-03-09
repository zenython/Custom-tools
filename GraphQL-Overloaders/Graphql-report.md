## Brief/Intro

GraphQL is a powerful query language for APIs that allows clients to request precisely the data they need. However, its flexibility can introduce security vulnerabilities if not properly managed. One such issue is Denial of Service (DoS) attacks via Alias Overloading and Array-based Query Batching. Attackers exploit these techniques to overwhelm GraphQL servers, leading to degraded performance or complete service failure.

## Vulnerability Details

### Alias Overloading
Alias overloading occurs when an attacker uses GraphQL aliases to send numerous requests within a single query. GraphQL allows clients to rename fields in a query using aliases, which can be exploited to execute multiple expensive operations within a single request. This bypasses traditional rate-limiting mechanisms that typically monitor query counts per request.

#### Example of Alias Overloading:
```graphql
query {
  user1: getUser(id: "1") { name email }
  user2: getUser(id: "2") { name email }
  user3: getUser(id: "3") { name email }
  ... (thousands more requests)
}
```
Here, a single request can trigger thousands of user fetch operations, overloading the backend.

### Array-based Query Batching
Query batching is a GraphQL feature that allows multiple queries to be combined into a single request for efficiency. Attackers can abuse this by sending large batched requests, each containing multiple complex queries. This can significantly increase server processing time, memory usage, and database load, leading to service degradation or downtime.

#### Example of Array-based Query Batching:
```json
[
  { "query": "{ getUser(id: \"1\") { name email } }" },
  { "query": "{ getUser(id: \"2\") { name email } }" },
  ... (thousands more requests)
]
```
Since GraphQL servers process all queries within a batch in a single execution cycle, excessive batching can exhaust server resources.

## Steps To Reproduce

- **Step-1:** visit the URL `https://subgraph.sovryn.app/subgraphs/name/DistributedCollective/sovryn-subgraph/graphql?query=`  OR  `https://zero-subgraph.sovryn.app/subgraphs/name/DistributedCollective/zero-subgraph/graphql?query=`  This Both Urls Are Only Vulnerable To Alias Batching . and the `https://wiki.sovryn.com` Url Is Vulnerable to Both Alias Overloading and Array-based Query Batching as well as directive overloading. And ALL URLS Are Vulnerable To Introspection.

- **Step-2:** Intercept the Request Into Burpsuite And Perform The Query Attacks In Repeater And Perform The Alias Overloading and Array-based Query Batching Payloads.

- **Step-3:** I Have Created Multiple Payloads Of Alias Overloading and Array-based Query Batching And Also Attached Them With The Burpsuite Request Itself In The Attachments 

- **Step-4:** Just Download The Requests And Copy And Paste It Into Burpsuite Repeater And Send The Requests As The Number of file name increases The Number Of Request Also Increases In The File for eg. Alias 1 has 50 payloads , Alias 2 has 100 payloads And Alias 3 has 500 Payloads Same For The Query Batching 

- **Step-5:** Now After Sending The Request You Will Notice The Size And The Time Increases As The Query Increases So, `AS AN ATTACKER I CAN`  Write A Simple Python Script In Order To Take Down The Entire API Service As Well As The Application Take Down.

- **Step-6:** The Screen Short Has Been Provided In The Attachments Of Gists As Well As The Python Script `IF YOU WANT TO TEST`

- **Step-7:** How To use the Tool `Copy the Code From The Gist` Make The File And Run this command `python3 script.py -u $URL    -a $Aliases or -r For Recursive -p $PATH` if You want to test single single go for Aliases And If You want to do recursive Do -r and Path here refers to the directory eg. /graphql or /v1/graphql and with -o you can save the output in text file.`All POSSIBLE Ddos ATTACK TYPE CODES HAS BEEN UPLOADED IN MY GIST LINK`

## Impact Details

If exploited, these vulnerabilities can cause severe performance issues and potentially take down a GraphQL API. The impacts include:
- **Increased Server Load:** High CPU and memory usage can slow down or crash the server.
- **Database Strain:** Excessive queries can overload the database, leading to performance degradation.
- **Denial of Service:** Legitimate users may be unable to access the service due to resource exhaustion.
- **Monetary Loss:** Cloud-based APIs with pay-per-resource billing can face high costs due to excessive processing and database queries.

## References

- [GraphQL Security Best Practices](https://graphql.org/learn/security/)
- [OWASP GraphQL Security Cheatsheet](https://cheatsheetseries.owasp.org/cheatsheets/GraphQL_Security_Cheat_Sheet.html)
- [Mitigating GraphQL DoS Attacks](https://www.apollographql.com/blog/graphql/security/)
- [GraphQL Query Cost Analysis](https://blog.apollographql.com/optimizing-graphql-performance-and-security-3503f0fda1d4)

By implementing proper security measures such as query complexity analysis, depth limiting, and rate limiting, organizations can mitigate these vulnerabilities and protect their GraphQL APIs from DoS attacks.

GIST LINK = `https://gist.github.com/zenython/9f47cef06f957633a911b72e53c4ace4`