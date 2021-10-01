#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import rospy  # pythonでROSを使うためのライブラリのロード
import moveit_commander # moveit関連の関数のロード
import geometry_msgs.msg  # ros：Topicの型を作る関数のロード
import rosnode  # 恐らく、rosとか諸々を立ち上げるときと一緒にいくつかのプログラム(node)も同時に起動している
                 # そこで動いている関数やらにアクセスするためのロードだと思われる
from tf.transformations import quaternion_from_euler  # ros：(確か)座標変換のやつ(tf)


def main():  # main
    rospy.init_node("pose_groupstate_example")#rospyライブラリを使って、ROSのNodeを作っている　（）内はNodeの名前を指定している
    robot = moveit_commander.RobotCommander()
    arm = moveit_commander.MoveGroupCommander("arm")
    arm.set_max_velocity_scaling_factor(0.1)
    arm.set_max_acceleration_scaling_factor(1.0)
    gripper = moveit_commander.MoveGroupCommander("gripper")

    while len([s for s in rosnode.get_node_names() if 'rviz' in s]) == 0:
        rospy.sleep(1.0)
    rospy.sleep(1.0)

    print("Group names:")
    print(robot.get_group_names())

    print("Current state:")
    print(robot.get_current_state())

    # アーム初期ポーズを表示
    arm_initial_pose = arm.get_current_pose().pose
    print("Arm initial pose:")
    print(arm_initial_pose)

    # 何かを掴んでいた時のためにハンドを開く
    gripper.set_joint_value_target([0.9, 0.9])
    gripper.go()

    # SRDFに定義されているmove_1
    print("move_1")
    arm.set_named_target("move_1")
    arm.go()
    
    # move_noと同様の動き
    print("move_2")
    arm.set_named_target("move_2")
    arm.go()
    
    # move_1と同様の動き
    print("move_3")
    arm.set_named_target("move_3")
    arm.go()
    
    # SRDFに定義されている"move_no"の姿勢にする
    print("move_0")
    arm.set_named_target("move_0")
    arm.go()

    # ハンドを少し閉じる
    gripper.set_joint_value_target([0.1, 0.1])
    gripper.go()

    # 手動で姿勢を指定するには以下のように指定
    """
    target_pose = geometry_msgs.msg.Pose()
    target_pose.position.x = 0.0
    target_pose.position.y = 0.0
    target_pose.position.z = 0.624
    q = quaternion_from_euler( 0.0, 0.0, 0.0 )
    target_pose.orientation.x = q[0]
    target_pose.orientation.y = q[1]
    target_pose.orientation.z = q[2]
    target_pose.orientation.w = q[3]
    arm.set_pose_target( target_pose )	# 目標ポーズ設定
    arm.go()							# 実行
    """

    # 移動後の手先ポーズを表示
    arm_goal_pose = arm.get_current_pose().pose
    print("Arm goal pose:")
    print(arm_goal_pose)
    print("done")


if __name__ == '__main__':  # main関数を使うためのIF文(別にifを組む必要はない。ただの保険で、ifとtryを使っている)
    try:
        if not rospy.is_shutdown():
            main()
    except rospy.ROSInterruptException:
        pass
