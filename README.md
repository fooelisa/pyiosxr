pyIOSXR
=====

In the spirit of [pyEOS](https://github.com/spotify/pyeos) for Arista EOS 
devices and [pyEZ](https://github.com/Juniper/py-junos-eznc) for JUNOS devices,
pyIOSXR is a python library to help interact with Cisco devices running 
IOS-XR.

Install
=======

To install, execute:

```
   pip install pyIOSXR
```

Documentation
=============

### Connect
```python
>>> from pyIOSXR import IOSXR
>>> device = IOSXR(hostname='lab001', username='ejasinska', password='passwd')
>>> device.open()
```

### Load and Compare Config
```python
>>> device.load_candidate_config(filename='/home/ejasinska/github/pyiosxr/config.txt')
>>> device.compare_config()
'!! IOS XR Configuration 5.1.3\r\ninterface TenGigE0/0/0/21\r\n description testing-xml-from-file\r\n!\r\nend'
```

### Discard Candidate Config
```python
>>> device.discard_config()
>>> device.compare_config()
'!! IOS XR Configuration 5.1.3\r\nend'
```

### Load and Commit Config
```python
>>> device.load_candidate_config(filename='/home/ejasinska/github/pyiosxr/other_config.txt')
>>> device.compare_config()
'!! IOS XR Configuration 5.1.3\r\ninterface TenGigE0/0/0/21\r\n description testing-xml-from-the-other-file\r\n!\r\nend'
>>> device.commit_config()
```

### Rollback Config
```python
>>> device.rollback()
```

### Close Connection
```python
>>> device.close()
```

License
======

Copyright 2015 Netflix, Inc.

Licensed under the Apache License, Version 2.0: http://www.apache.org/licenses/LICENSE-2.0
