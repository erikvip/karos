'''
Test for pymtp / LibMTP. This test dumps all connected MTP devices

You must have a connected and enabled MTP device for this to show any devices
'''
import pymtp

mtp = pymtp.MTP()
d = mtp.detect_devices()
for i in d:
    #c+=1;
    print i.device_entry
    print "%(name)s (USB bus:%(bus)i device:%(dev)i)" % \
            {'name': i.device_entry, 'bus': i.bus_location, 'dev': i.devnum}

#        self.mtp_devices.append({
#            "index": c, 
#            "viewclass": "MtpDevice", 
#            "mtp_name": "%(name)s (USB bus:%(bus)i device:%(dev)i)" % 
#                {'name': i.device_entry, 'bus': i.bus_location, 'dev': i.devnum}
#        })
