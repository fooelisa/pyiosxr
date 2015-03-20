pyIOSXR
=====

In the spirit of [pyEOS](https://github.com/spotify/pyeos) for Arista EOS 
devices and [pyEZ](https://github.com/Juniper/py-junos-eznc) for JUNOS 
devices, pyIOSXR is a python library to help interact with Cisco devices 
running IOS-XR.

Install
=======

To install, execute:

```
   pip install pyIOSXR
```

Documentation
=============

### Connect
Connect to an IOS-XR device:
```python
>>> from pyIOSXR import IOSXR
>>> device = IOSXR(hostname='lab001', username='ejasinska', password='passwd')
>>> device.open()
```

### Load and Compare Config
Load a candidate configuration from a file and show the diff that is going to 
be applied when committing the config:
```python
>>> device.load_candidate_config(filename='unit/test/config.txt')
>>> device.compare_config()
---
+++
@@ -704,0 +705,3 @@
+interface TenGigE0/0/0/21
+ description testing-xml-from-file
+!
```

### Discard Candidate Config
If an already loaded configuration should be discarded without committing it,
call discard_config():
```python
>>> device.discard_config()
>>> device.compare_config()
>>>
```

### Load, Compare and Commit Config
If you want to commit the loaded configuration, call commit_config():
```python
>>> device.load_candidate_config(filename='unit/test/other_config.txt')
>>> device.compare_config()
---
+++
@@ -704,0 +705,3 @@
+interface TenGigE0/0/0/21
+ description testing-xml-from-the-other-file
+!
>>> device.commit_config()
```

### Commit Replace
If you would rather commit the config by replacing the existing configuration,
call commit_replace_config():
```python
>>> device.load_candidate_config(filename='unit/test/full_config.txt')
>>> device.compare_replace_config()
>>> device.commit_replace_config()
```

### Rollback Config
After a previous commit, rollback() will return to the configuration prior
to the commit:
```python
>>> device.rollback()
```

### Running Show Commands
Any show command can be executed in the following fashion, with the command 
embedded into the call:
```python
>>> device.show_bgp_summary()
...
>>> device.show_interfaces()
...
```

### Close Connection
Call close() to close the connection to the device:
```python
>>> device.close()
```

Thanks
======
A special thanks to David Barroso! This library is entirely based on David's
[pyEOS](https://github.com/spotify/pyeos), which is a wrapper around Arista's
eAPI for EOS.

Also, many thanks go out to Brady Walsh, without whom staying sane while 
digging through Cisco docs and XML would have been impossible.

License
======

Copyright 2015 Netflix, Inc.

Licensed under the Apache License, Version 2.0: http://www.apache.org/licenses/LICENSE-2.0
