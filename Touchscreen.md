# Touchscreen setup


## Ev test
    Input driver version is 1.0.1
    Input device ID: bus 0x0 vendor 0x0 product 0x0 version 0x0
    Input device name: "ADS7846 Touchscreen"
    Supported events:
      Event type 0 (EV_SYN)
      Event type 1 (EV_KEY)
        Event code 330 (BTN_TOUCH)
      Event type 3 (EV_ABS)
        Event code 0 (ABS_X)
          Value   1904
          Min        0
          Max     4095
        Event code 1 (ABS_Y)
          Value   2661
          Min        0
          Max     4095
        Event code 24 (ABS_PRESSURE)
          Value      0
          Min        0
          Max    65535
    Properties:


# Input Reading Process

- Type 1 (EV_KEY) value 1 -- Touch event start
- Read type 3 EV_ABS with ABS_X and ABS_y, value's this is the touch event
- Also includes ABS_PRESSURE on each touch event
- Keep reading until EV_KEY value 0 - Touch event stopped



# Working with TSLIB


## Run ts_calibrate

Set the TSLIB_ enviornment variables, and run ts_calibrate for screen calibration.  You must run as sudo, as this will create/modify /etc/ files

    sudo TSLIB_FBDEVICE=/dev/fb0 TSLIB_TSDEVICE=/dev/input/event0 ts_calibrate

Two files should now be in /etc:


    $ ls -l /etc/ts.conf /etc/pointer*
    -rwxr-xr-x 1 root root  45 Jan 24 06:03 /etc/pointercal
    -rw-r--r-- 1 root root 645 Jan 20  2014 /etc/ts.conf

You can now test the screen by running **ts_test**:

    sudo TSLIB_FBDEVICE=/dev/fb0 TSLIB_TSDEVICE=/dev/input/event0 ts_calibrate


