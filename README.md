humming-py
==========

humminbird.me pyton client, switches between V1 and V2 when available.


```python

import hummingbird

c = hummingbird.Client()
search_results = c.search("dragonball")

# when no v2_token is given
assert search_results[0].full == search_results[0]

# episodes are only available with an v2_token
c = hummingbird.Client(v2_token="your_app_token")
first_dragonball_ep = c.search("dragonball")[0].full.episodes[0]


```
