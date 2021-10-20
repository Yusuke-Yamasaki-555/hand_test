#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import rospy  # pythonでROSを使うためのライブラリのロード
import moveit_commander # moveit関連の関数のロード
import geometry_msgs.msg  # ros：Topicの型を作る関数のロード
import rosnode
from tf.transformations import quaternion_from_euler  # ros：座標変換のやつ(tf)


def main():  # main
    rospy.init_node("pose_groupstate_example")#rospyライブラリを使って、ROSのNodeを作っている　（）内はNodeの名前を指定している
    robot = moveit_commander.RobotCommander()
    arm = moveit_commander.MoveGroupCommander("arm")
    arm.set_max_velocity_scaling_factor(0.1) #  アームの速度・加速度のコントロール。値＝最大値に対する倍率
    arm.set_max_acceleration_scaling_factor(1.0)
    gripper = moveit_commander.MoveGroupCommander("gripper")

    while len([s for s in rosnode.get_node_names() if 'rviz' in s]) == 0:
        rospy.sleep(1.0)
    rospy.sleep(1.0)

    print("Group names:")
    print(robot.get_group_names())

    print("Current state:")
    print(robot.get_current_state())

    print("====================================================================")

    # 初期位置に移動
    print("move_reset")
    arm.set_named_target("move_reset")
    arm.go()

    # ハンドを開く＝処理確認
    gripper.set_joint_value_target([0.9, 0.9])
    gripper.go()
    """
    #  srdfの値をプログラムから直接指定。(34行を参考)
    print("arm_set_start")
    arm.set_joint_value_target({"crane_x7_shoulder_revolute_part_tilt_joint":-0.78539816339745,\
                                "crane_x7_shoulder_fixed_part_pan_joint":1.5707963267949})
    arm.go()
    print("arm_set_end")
    
    #srdfファイルからの読み取りは以下から(各関節角度の設定＝順運動学)
    
    print("move_1")
    arm.set_named_target("move_1")
    arm.go()

    print("move_2")
    arm.set_named_target("move_2")
    arm.go()
    
    print("move_3")
    arm.set_named_target("move_3")
    arm.go()
    """
    
    # 
    target_pose = geometry_msgs.msg.Pose()
    target_pose.position.x = 0
    target_pose.position.y = 0
    target_pose.position.z = 0.3

     #  
    q = quaternion_from_euler( 1.0, 0.0, 0.0 )
    target_pose.orientation.x = q[0]
    target_pose.orientation.y = q[1]
    target_pose.orientation.z = q[2]
    target_pose.orientation.w = q[3]
    arm.set_pose_target( target_pose )	# 目標ポーズ設定
    arm.go()							# 実行
    
    # 初期位置に移動
    print("move_reset")
    arm.set_named_target("move_reset")
    arm.go()
    
    # ハンドを少し閉じる＝処理確認
    gripper.set_joint_value_target([0.1, 0.1])
    gripper.go()
