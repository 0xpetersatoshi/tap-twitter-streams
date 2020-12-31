# tap-twitter-streams

This is a [Singer](https://singer.io) tap that produces JSON-formatted data
following the [Singer
spec](https://github.com/singer-io/getting-started/blob/master/SPEC.md).

This tap:

- Pulls raw data from the Twitter [Filtered Stream API](https://developer.twitter.com/en/docs/twitter-api/tweets/filtered-stream/introduction)
- Streams tweets in real-time that match the "rules" defined in a [config.json](sample_config.json) file.

---

Copyright &copy; 2018 Stitch
