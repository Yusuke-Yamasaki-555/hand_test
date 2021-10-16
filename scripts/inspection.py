#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import rospy
import test

if __name__ == '__main__':  # main関数を使うためのIF文(別にifを組む必要はない。ただの保険で、ifとtryを使っている)
    try:
        if not rospy.is_shutdown():
            print("Read test.main")
            test.main()
    except rospy.ROSInterruptException:
        pass
