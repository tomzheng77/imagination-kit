# Arkham Fetcher

### Next Steps BACKUP TODO
- figure out if its possible to calculate x-payload
- if the same x-payload can be used for multiple tokens
  - within a time window of say 1 minute
  - unfortunately no
- https://eciwdnbu5zh.larksuite.com/docx/EOendq0Bbo9dKPxtwpAuJknlsef

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
