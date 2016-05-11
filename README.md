## Automatic Quip Job Script for AHA Broadcast
The scripts call [Quip](https://quip.com) API though its [official Python libaray](https://github.com/quip/quip-api) to perform certain automatic tasks on the broadcast doc.

Develop upon Python [Flask](http://flask.pocoo.org) Skeleton for [Google App Engine](https://cloud.google.com/python/getting-started/hello-world). Host on quip4aha.appspot.com. I'm not familiar with Flask, so this repo's precursor was just a clumsy straight copy from Google's example, and there will be a lot of redundancy and inconsistency.

### Include:
* [AssignHost.py](\AssignHost.py) (/) divides the doc into parts and assigns them to the host evenly.
* [NewDoc.py](\NewDoc.py) (/newdoc, cron: every Friday 16:10(UTC+08:00)) creates the doc for the broadcast next week.
* UpdateWeather (coming soon) updates "weather for today" in the doc.
