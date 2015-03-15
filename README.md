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
```
>>> from pyIOSXR import IOSXR
>>> device = IOSXR(hostname='lab001', username='ejasinska', password='passwd')
>>> device.open()
```

### Load and Compare Config
```
>>> device.load_candidate_config(filename='/home/ejasinska/github/pyiosxr/config.txt')
>>> device.compare_config()
'<Response MajorVersion="1" MinorVersion="0"><CLI><Configuration>\r\nBuilding configuration...\r\n!! IOS XR Configuration 5.1.3\r\ninterface TenGigE0/0/0/21\r\n description testing-xml-from-file\r\n!\r\nend\r\n\r\n</Configuration></CLI><ResultSummary ErrorCount="0"/></Response>'
```

### Discard Candidate Config
```
>>> device.discard_config()
>>> device.compare_config()
'<Response MajorVersion="1" MinorVersion="0"><CLI><Configuration>\r\nBuilding configuration...\r\n!! IOS XR Configuration 5.1.3\r\nend\r\n\r\n</Configuration></CLI><ResultSummary ErrorCount="0"/></Response>'
```

### Load and Commit Config
```
>>> device.load_candidate_config(filename='/home/ejasinska/github/pyiosxr/other_config.txt')
>>> device.compare_config()
'<Response MajorVersion="1" MinorVersion="0"><CLI><Configuration>\r\nBuilding configuration...\r\n!! IOS XR Configuration 5.1.3\r\ninterface TenGigE0/0/0/21\r\n description testing-xml-from-the-other-file\r\n!\r\nend\r\n\r\n</Configuration></CLI><ResultSummary ErrorCount="0"/></Response>'
>>> device.commit_config()
```

### Rollback Config
----
```
>>> device.rollback()
```

### Close Connection
----
```
>>> device.close()
```

License
======

Copyright 2015 Netflix, Inc.

Licensed under the Apache License, Version 2.0: http://www.apache.org/licenses/LICENSE-2.0
