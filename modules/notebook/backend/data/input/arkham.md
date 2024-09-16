# Arkham Fetcher

### Next Steps
- implement superfast scraper
- analyze holders on bybit
- figure out if its possible to calculate x-payload [y]
- if the same x-payload can be used for multiple tokens [n]
  - within a time window of say 1 minute
  - unfortunately no
- https://eciwdnbu5zh.larksuite.com/docx/EOendq0Bbo9dKPxtwpAuJknlsef

### Design up Front: Pseudocode
- fetch all holders of the current day
- fetch all portfolios of the current day

### Portfolio API Requests
- two requests were sent
  - `/portfolio/entity/vitalik-buterin?time=1717164000000`
  - `/portfolio/entity/vitalik-buterin?time=1717768800000`
```
curl 'https://api.arkhamintelligence.com/portfolio/entity/vitalik-buterin?time=1717164000000' \
  -H 'accept: application/json, text/plain, */*' \
  -H 'accept-language: en-US,en;q=0.9' \
  -H 'cache-control: no-cache' \
  -H 'origin: https://platform.arkhamintelligence.com' \
  -H 'pragma: no-cache' \
  -H 'priority: u=1, i' \
  -H 'referer: https://platform.arkhamintelligence.com/' \
  -H 'sec-ch-ua: "Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-platform: "macOS"' \
  -H 'sec-fetch-dest: empty' \
  -H 'sec-fetch-mode: cors' \
  -H 'sec-fetch-site: same-site' \
  -H 'user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36' \
  -H 'x-payload: 2858f2b7d1382374263d38d4dc36a6153ed48b3b91a5e4e722b8610c60d50610' \
  -H 'x-timestamp: 1717839443'
```
```
curl 'https://api.arkhamintelligence.com/portfolio/entity/vitalik-buterin?time=1717768800000' \
  -H 'accept: application/json, text/plain, */*' \
  -H 'accept-language: en-US,en;q=0.9' \
  -H 'cache-control: no-cache' \
  -H 'origin: https://platform.arkhamintelligence.com' \
  -H 'pragma: no-cache' \
  -H 'priority: u=1, i' \
  -H 'referer: https://platform.arkhamintelligence.com/' \
  -H 'sec-ch-ua: "Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-platform: "macOS"' \
  -H 'sec-fetch-dest: empty' \
  -H 'sec-fetch-mode: cors' \
  -H 'sec-fetch-site: same-site' \
  -H 'user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36' \
  -H 'x-payload: 2858f2b7d1382374263d38d4dc36a6153ed48b3b91a5e4e722b8610c60d50610' \
  -H 'x-timestamp: 1717839443'
```


### AIO HTTP
- https://docs.aiohttp.org/en/stable/
- https://docs.aiohttp.org/en/stable/client_advanced.html

### Client Key `gh67j345kl6hj5k432` TODO

### Headers of the Base Page
```
curl 'https://platform.arkhamintelligence.com/explorer/token/bittensor' \
  -H 'accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7' \
  -H 'accept-language: en-US,en;q=0.9' \
  -H 'cache-control: no-cache' \
  -H 'cookie: _gcl_au=1.1.1038380352.1716684635; _ga=GA1.1.1278395108.1716684635; _fbp=fb.1.1716684635261.1609392723; _ga_P74N755GGG=deleted; cf_clearance=_reGgm8hBKwTGwnfAzATCuLKusvflDz4f3TkY4Z6T1Y-1717836845-1.0.1.1-Cj5mZvLaRL0KselO.G1Mleilq5OwNSOCIK7gzBebThhNA2QlVnnK5N9.pYSwFHLL37FC8MlfQUtNFb7SYGtHog; mp_f32068aad7a42457f4470f3e023dd36f_mixpanel=%7B%22distinct_id%22%3A%20%2218fb260b52d2dde-08bb2e3b25b3ab-1b525637-13c680-18fb260b52e1f67%22%2C%22%24device_id%22%3A%20%2218fb260b52d2dde-08bb2e3b25b3ab-1b525637-13c680-18fb260b52e1f67%22%2C%22%24initial_referrer%22%3A%20%22%24direct%22%2C%22%24initial_referring_domain%22%3A%20%22%24direct%22%7D; _ga_P74N755GGG=GS1.1.1717836847.10.1.1717838291.0.0.0' \
  -H 'pragma: no-cache' \
  -H 'priority: u=0, i' \
  -H 'sec-ch-ua: "Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-platform: "macOS"' \
  -H 'sec-fetch-dest: document' \
  -H 'sec-fetch-mode: navigate' \
  -H 'sec-fetch-site: same-origin' \
  -H 'sec-fetch-user: ?1' \
  -H 'upgrade-insecure-requests: 1' \
  -H 'user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
```

### Coins to Observe

### Valid CURL Command for Token Holders
curl 'https://api.arkhamintelligence.com/token/holders/render-token?groupByEntity=false' \
  -H 'accept: application/json, text/plain, */*' \
  -H 'accept-language: en-US,en;q=0.9' \
  -H 'cache-control: no-cache' \
  -H 'origin: https://platform.arkhamintelligence.com' \
  -H 'pragma: no-cache' \
  -H 'priority: u=1, i' \
  -H 'referer: https://platform.arkhamintelligence.com/' \
  -H 'sec-ch-ua: "Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-platform: "macOS"' \
  -H 'sec-fetch-dest: empty' \
  -H 'sec-fetch-mode: cors' \
  -H 'sec-fetch-site: same-site' \
  -H 'user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36' \
  -H 'x-payload: 33a7830556905936df44a413c23ebcd577886ef29106c3e30322a71affe204e1' \
  -H 'x-timestamp: 1717205067'

### Arkham Web Page Analysis
- "clientKey":"gh67j345kl6hj5k432" in .html
- ty = 1717223361
- ???
- tv = 9c8a10f4f7420f95f423e9ab360f618453f6c8f78bef28acb03a248d8cc8b003
- tr =
  - "https://api.arkhamintelligence.com/user/cookie_preference"
  - "https://api.arkhamintelligence.com/intelligence/search"
  - "https://api.arkhamintelligence.com/user"
  - "https://api.arkhamintelligence.com/intelligence/token/ethereum"
- tE.apiHost = "https://api.arkhamintelligence.com"

```javascript
ty = Math.floor(new Date().getTime() / 1e3).toString()
tv = tA(tr, ty, tE.clientKey)
t_ = {
  "X-Timestamp": ty,
  "X-Payload": tv,
  ...tu}

tA = (tr,ts,tu)=>{
let tp = tE.apiHost
  , ty = tr.replace(tp, "").split("?")[0]
  , tv = tS().createHash("sha256").update("".concat(ty, ":").concat(ts, ":").concat(tu)).digest("hex")
  , t_ = tS().createHash("sha256").update("".concat(tu, ":").concat(tv)).digest("hex");
return t_
```
```
const crypto = require('crypto');
crypto.createHash("sha256")
hasher.update("".concat(ty, ":").concat(ts, ":").concat(tu)).digest("hex")
```
