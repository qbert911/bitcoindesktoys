curl https://api.aleth.io/v1/accounts/0x8D82Fef0d77d79e5231AE7BFcFeBA2bAcF127E2B/tokenBalances   -u sk_main_a3c9a81b69187499: |jq .
curl https://api.aleth.io/v1/accounts/0x3041cbd36888becc7bbcbc0045e3b1f144466f5f/tokenBalances   -u sk_main_a3c9a81b69187499: |jq .
curl -s https://data-api.defipulse.com/api/v1/egs/api/ethgasAPI.json?api-key=7e586257575cab0b247acf0d2fddef28c0a9c537808cba24257a03c1ca3c | jq .average
