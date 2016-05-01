# MTP info

## Install

*MTP lib*   

    apt-get install jmtpfs

*Data recovery*   

    apt-get install testdisk

## Running

*Only one device connected*
    mkdir ~/mnt
    sudo jmtpfs -o allow_other ~/mnt

List devices and specify a device using --device=<busnum>,<devnum>

    $ sudo jmtpfs -l
    Unable to open ~/.mtpz-data for reading, MTPZ disabled.
    Device 0 (VID=22b8 and PID=2ea8) is UNKNOWN.
    Please report this VID/PID and the device model to the libmtp development team
    Available devices (busLocation, devNum, productId, vendorId, product, vendor):
    1, 5, 0x2ea8, 0x22b8, UNKNOWN, UNKNOWN

*Successful mount output*

    $ mount
    ...
    jmtpfs on /home/pi/mnt type fuse.jmtpfs (rw,nosuid,nodev,relatime,user_id=0,group_id=0,allow_other)


**Unmounting**
    
    sudo fusermount -u ~/mnt


## Searching

See 

### Folders of interest

- Android/data/
  - com.motorola.email/cache/ - Emails
  - com.motorola.MotGallery2/ - Images embedded in one file

