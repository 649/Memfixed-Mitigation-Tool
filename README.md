# MEMFIXED DDOS MITIGATION TOOL

* Author: [@037](https://twitter.com/037)
* Credits to [@dormando](https://twitter.com/dormando) for the killswitch

This tool allows you to shutdown/flush vulnerable Memcached servers obtained from Shodan.io

### Prerequisites

The only thing you need installed is Python 3.x

```
apt-get install python3
```

You also require to have Scapy and Shodan modules installed
```
pip install scapy
```

```
pip install shodan
```

### Using Shodan API

This tool requires you to own an upgraded Shodan API

You may obtain one for free in [Shodan](https://shodan.io/) if you sign up using a .edu email

![alt text](https://raw.githubusercontent.com/649/Memfixed-Mitigation-Tool/master/menu.png)