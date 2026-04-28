---
title: "Reverse Engineering Ethstats Agent for a FluentD plugin"
date: 2017-04-23T22:20:00+0000
lastmod: 2017-04-23T22:41:04+0000
slug: "reverse-engineering-ethstats-agent-for-a-fluentd-plugin"
feature_image: "/images/2017/04/gabriele-diwald-small201135.jpg"
aliases:
  - /reverse-engineering-ethstats-agent-for-a-fluentd-plugin/
---

Just spouting about some progress I made on reverse engineering some API for Ethstats agent and dashboard that soon will be a FluentD plugin, and with that working with Azure OMS to feed the analytical reporting for monitoring and real-time analysis of the health of an Ethereum client.

Anybody working with Ethereum is probably familiar with the [Ethstats](http://ethstats.net) dashboard. This great dashboard is courtesy of [Marian](https://twitter.com/MarianOanceaCub).

Well, for that dashboard to work today, there are 2 parts; 1 is the Dashboard itself - which is up on GitHub at [dashboard](https://github.com/cubedro/eth-netstats). The Second part is the agent that must run on the local machine with the Ethereum client (Geth). That is also in the same GitHub organization [agent](https://github.com/cubedro/eth-net-intelligence-api).

We've been looking at creating a [FluentD plugin](https://fluentd.org) so folks can just feed their choice of analytical platform. On Azure, the [OMS suite](https://www.microsoft.com/en-us/cloud-platform/operations-management-suite) service utilizes FluentD in the agent. So, any FluentD plugin (or many) just work in OMS.

I was working with someone briefly and they where asking "where are the API documentation or specs" - casually, and seriously I just responded "It's here in the code". Well for some that's just not good enough.

For me however, suites me just right. I know it's always up-2-date :).

Now, the next part of this is that Geth had introduced the `--ethstats value` [command line option](https://github.com/ethereum/go-ethereum/wiki/Command-Line-Options).

So, here's a quick view of the basic status being sent to the FluentD plugin from Geth's `-ethstats` thread.

![fluentd plugin](https://cicorias-transit.s3.amazonaws.com/monosnap/1._node_2017-04-23_22-13-56.png)

What's nice is that Geth is fairly resilient to retrying the connection and recovering from breakage in the network link. Also, in the Geth 1.6 release some more fixes were made to bring the level of status more in line with what the two tools (Dashboard and Agent) that Marian provided.
