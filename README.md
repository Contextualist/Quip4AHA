## Automatic Quip Job Script for AHA Broadcast
The scripts call [Quip](https://quip.com) API though [its official Python library](https://github.com/quip/quip-api) to perform certain automatic tasks on the broadcast doc.

Develop upon [Python Flask Skeleton for Google App Engine](https://cloud.google.com/python/getting-started/hello-world). Host on quip4aha.appspot.com. I'm not familiar with Flask, so this repo's precursor was just a clumsy straight copy from Google's example, and there will be a lot of redundancy and inconsistency.

### Include:
| Script | Call | Cron(UTC+08:00) | Description |
| ------ | ---- | --------------- | ----------- |
| [AssignHost.py](\AssignHost.py) | / | | divides the doc into parts and assigns them to the host evenly. |
| [NewDoc.py](\NewDoc.py) | /newdoc | every Friday 16:10 | creates the doc for the broadcast next week. |
| [UpdateWeather](\UpdateWeather.py) | /updateweather | every Wednesday 07:27 | updates "weather for today" in the doc. |
