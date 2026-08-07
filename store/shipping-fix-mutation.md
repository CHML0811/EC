# Ready-to-run: US shipping fix

Schema-validated against the Admin API (✅ VALID). Run it the moment the Shopify connector is
up — via `graphql_mutation`, or paste into **Admin → Apps → Shopify GraphiQL**.

**What it does:** deletes the two Brazilian-template zones and creates a **United States** zone
(free over $60, else $5.95) plus a **Rest of World** zone at $14.95.

⚠️ Amounts are in the **shop's** currency. Switch the store to USD **first** — then verify the
rates still read 5.95 / 60 / 14.95 afterwards and correct them if Shopify converted.

### Mutation
```graphql
mutation FixShipping($id: ID!, $profile: DeliveryProfileInput!) {
  deliveryProfileUpdate(id: $id, profile: $profile) {
    profile {
      id
      profileLocationGroups {
        locationGroupZones(first: 5) {
          edges {
            node {
              zone { id name }
              methodDefinitions(first: 5) {
                edges {
                  node {
                    id
                    name
                    active
                    rateProvider {
                      ... on DeliveryRateDefinition {
                        price { amount currencyCode }
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
    userErrors { field message }
  }
}
```

### Variables
```json
{
  "id": "gid://shopify/DeliveryProfile/105866887215",
  "profile": {
    "zonesToDelete": [
      "gid://shopify/DeliveryZone/414388682799",
      "gid://shopify/DeliveryZone/414388715567"
    ],
    "locationGroupsToUpdate": [
      {
        "id": "gid://shopify/DeliveryLocationGroup/106782064687",
        "zonesToCreate": [
          {
            "name": "United States",
            "countries": [{ "code": "US", "includeAllProvinces": true }],
            "methodDefinitionsToCreate": [
              {
                "name": "Standard shipping (3-5 days)",
                "active": true,
                "rateDefinition": { "price": { "amount": 5.95, "currencyCode": "USD" } },
                "priceConditionsToCreate": [
                  { "criteria": { "amount": 0, "currencyCode": "USD" }, "operator": "GREATER_THAN_OR_EQUAL_TO" },
                  { "criteria": { "amount": 59.99, "currencyCode": "USD" }, "operator": "LESS_THAN_OR_EQUAL_TO" }
                ]
              },
              {
                "name": "Free shipping (orders over $60)",
                "active": true,
                "rateDefinition": { "price": { "amount": 0, "currencyCode": "USD" } },
                "priceConditionsToCreate": [
                  { "criteria": { "amount": 60, "currencyCode": "USD" }, "operator": "GREATER_THAN_OR_EQUAL_TO" }
                ]
              }
            ]
          },
          {
            "name": "Rest of World",
            "countries": [{ "restOfWorld": true }],
            "methodDefinitionsToCreate": [
              {
                "name": "International shipping",
                "active": true,
                "rateDefinition": { "price": { "amount": 14.95, "currencyCode": "USD" } }
              }
            ]
          }
        ]
      }
    ]
  }
}
```

> If the store is still on HKD when you run this, swap every `"USD"` above for `"HKD"` —
> the API rejects a currency that isn't the shop's.

**Prefer clicking?** `store/us-market-setup.md` §3 has the same change as admin steps.

### Verify
```
[ ] Zones are "United States" and "Rest of World" only — no Brazil
[ ] US cart at $30 quotes $5.95   [ ] US cart at $65 quotes $0.00
```
