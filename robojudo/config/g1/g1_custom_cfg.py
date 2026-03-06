from robojudo.config import cfg_registry
from robojudo.controller.ctrl_cfgs import (
    JoystickCtrlCfg,  # noqa: F401
    KeyboardCtrlCfg,  # noqa: F401
    UnitreeCtrlCfg,  # noqa: F401
)
from robojudo.pipeline.pipeline_cfgs import (
    RlLocoMimicPipelineCfg,  # noqa: F401
    RlMultiPolicyPipelineCfg,  # noqa: F401
    RlPipelineCfg,  # noqa: F401
)

from .ctrl.g1_beyondmimic_ctrl_cfg import G1BeyondmimicCtrlCfg  # noqa: F401
from .ctrl.g1_motion_ctrl_cfg import (  # noqa: F401
    G1MotionCtrlCfg,
    G1MotionH2HCtrlCfg,
    G1MotionKungfuBotCtrlCfg,
    G1MotionTwistCtrlCfg,
)
from .ctrl.g1_twist_redis_ctrl_cfg import G1TwistRedisCtrlCfg  # noqa: F401
from .env.g1_dummy_env_cfg import G1DummyEnvCfg  # noqa: F401
from .env.g1_mujuco_env_cfg import G1_12MujocoEnvCfg, G1_23MujocoEnvCfg, G1MujocoEnvCfg, G1_23LockEnvCfg  # noqa: F401
from .env.g1_real_env_cfg import G1RealEnvCfg, G1UnitreeCfg  # noqa: F401
from .policy.g1_amo_policy_cfg import G1AmoPolicyCfg  # noqa: F401
from .policy.g1_asap_policy_cfg import G1AsapLocoPolicyCfg, G1AsapPolicyCfg  # noqa: F401
from .policy.g1_beyondmimic_policy_cfg import G1BeyondMimicPolicyCfg  # noqa: F401
from .policy.g1_h2h_policy_cfg import G1H2HPolicyCfg  # noqa: F401
from .policy.g1_kungfubot_policy_cfg import G1KungfuBotGeneralPolicyCfg, G1KungfuBotPolicyCfg, G1_23PolicyCfg  # noqa: F401
from .policy.g1_smooth_policy_cfg import G1SmoothPolicyCfg  # noqa: F401
from .policy.g1_twist_policy_cfg import G1TwistPolicyCfg  # noqa: F401
from .policy.g1_unitree_policy_cfg import G1UnitreePolicyCfg, G1UnitreeWoGaitPolicyCfg  # noqa: F401

from robojudo.policy import PolicyCfg
from .pipeline.g1_locomimic_pipeline_cfg import G1_23RlLocoMimicPipelineCfg  # noqa: F401

# ======================== Custom Configs ======================== #
"""
Add your custom config here.
"""


@cfg_registry.register
class g1_dev(RlPipelineCfg):
    robot: str = "g1"
    env: G1_23MujocoEnvCfg = G1_23MujocoEnvCfg()

    ctrl: list[KeyboardCtrlCfg] = [
        KeyboardCtrlCfg(),
    ]

    policy: G1UnitreePolicyCfg = G1UnitreePolicyCfg()

@cfg_registry.register
class g1_custom(RlMultiPolicyPipelineCfg):
    robot: str = "g1"
    env: G1_23LockEnvCfg = G1_23LockEnvCfg()
    ctrl: list[KeyboardCtrlCfg | JoystickCtrlCfg] = [
        KeyboardCtrlCfg(
            # triggers_extra={
            #     "Key.space": "[SHUTDOWN]",
            #     "r": "[SIM_REBORN]",
            # }
        ),
        JoystickCtrlCfg(
            triggers_extra={
                "A": "[SHUTDOWN]",
                "X": "[MOTION_RESET]",
                "B": "[POLICY_SWITCH],0",
                "Y": "[SIM_REBORN]",
                "RB+Up": "[POLICY_SWITCH],4",
                "RB+Down": "[POLICY_SWITCH],1",
                "RB+Left": "[POLICY_SWITCH],2",
                "RB+Right": "[POLICY_SWITCH],3",
            }
        ),
    ]

    policies: list[PolicyCfg] = [
        G1UnitreePolicyCfg(),       # 0.踏步
        G1AmoPolicyCfg(),           # 1.站立
        G1_23PolicyCfg(),           # 2.作揖
        G1KungfuBotPolicyCfg(),     # 3.打拳
        G1_23PolicyCfg(),           # 4.作揖>打拳>踏步
    ]
    
    next_policy: dict[int, int] = {
        4: 3,
    }

@cfg_registry.register
class g1_cr(g1_custom):
    env: G1RealEnvCfg = G1RealEnvCfg(
        # env_type="UnitreeEnv",  # For unitree_sdk2py
        env_type="UnitreeCppEnv",  # For unitree_cpp, check README for more details
        unitree=G1UnitreeCfg(
            net_if="eth0",  # note: change to your network interface
        ),
    )
    ctrl: list[UnitreeCtrlCfg] = [
        UnitreeCtrlCfg(
            triggers_extra={
                "A": "[SHUTDOWN]",                  # 安全急停
                # "X": "[MOTION_RESET]",
                "B": "[POLICY_SWITCH],0",           # 踏步
                # "Y": "[SIM_REBORN]",
                # "R1+Up": "[POLICY_SWITCH],4",     # 作揖>打拳>踏步
                "R1+Down": "[POLICY_SWITCH],1",     # 站立
                "R1+Left": "[POLICY_SWITCH],2",     # 作揖
                # "R1+Right": "[POLICY_SWITCH],3",  # 打拳
            }
        ),
    ]

@cfg_registry.register
class g1_lm_sim(G1_23RlLocoMimicPipelineCfg):
    robot: str = "g1"
    env: G1_23LockEnvCfg = G1_23LockEnvCfg()

    ctrl: list[KeyboardCtrlCfg | JoystickCtrlCfg] = [
        JoystickCtrlCfg(
            triggers_extra={
                "Y": "[POLICY_LOCO]",
                "X": "[POLICY_MIMIC]",
                "B": "[SIM_REBORN]",
                "A": "[SHUTDOWN]",
                "RB+Up": "[POLICY_SWITCH],4",
                "RB+Left": "[POLICY_SWITCH],1",
                "RB+Down": "[POLICY_SWITCH],2",
                "RB+Right": "[POLICY_SWITCH],3",
                "LB+Up": "[POLICY_SWITCH],0",
                # "LB+Left": "[POLICY_SWITCH],5",
                # "LB+Down": "[POLICY_SWITCH],6",
                # "LB+Right": "[POLICY_SWITCH],7",
            }
        ),
    ]

    loco_policy: G1AmoPolicyCfg = G1AmoPolicyCfg()
    # loco_policy: G1AsapLocoPolicyCfg = G1AsapLocoPolicyCfg()
    # loco_policy: G1UnitreePolicyCfg = G1UnitreePolicyCfg()
    # loco_policy: G1UnitreeWoGaitPolicyCfg = G1UnitreeWoGaitPolicyCfg()
    mimic_policies: list[PolicyCfg] = [
        G1_23PolicyCfg(),               # 0.作揖
        G1AsapPolicyCfg(),              # 1.起跳转身
        G1_23PolicyCfg(                 # 2.马步甩臂 1
            policy_name="horse_stance",
            relative_path="pose_50000.onnx",
            motion_length_s=7.0
        ),
        G1_23PolicyCfg(                 # 3.马步甩臂 2
            policy_name="horse_stance",
            relative_path="pose_2_119000.onnx",
            motion_length_s=7.0
        ),
        G1AsapPolicyCfg(                # 4.跳舞
            policy_name="robomimic",
            relative_path="dance_0605.onnx",
            motion_length_s=18.0,
            start_upper_body_dof_pos = [
                0, 0, 0,
                0.35, 0.18, 0, 0.87, 
                0.35, -0.18, 0, 0.87,
            ],
        ),
        G1AsapPolicyCfg(),              # 5.起跳转身
    ]

    next_policy: dict[int, int] = {
        0: 5,
        5: 4,
    }

@cfg_registry.register
class g1_lm_real(g1_lm_sim):
    env: G1RealEnvCfg = G1RealEnvCfg(
        env_type="UnitreeCppEnv",
        unitree=G1UnitreeCfg(
            net_if="eth0",
        ),
    )
    loco_policy: G1AmoPolicyCfg = G1AmoPolicyCfg()
    ctrl: list[KeyboardCtrlCfg | JoystickCtrlCfg] = [
        JoystickCtrlCfg(
            triggers_extra={
                "Y": "[POLICY_LOCO]",
                "X": "[POLICY_MIMIC]",
                "B": "[SIM_REBORN]",
                "A": "[SHUTDOWN]",
                "RB+Up": "[POLICY_SWITCH],4",
                # "RB+Left": "[POLICY_SWITCH],1",
                "RB+Down": "[POLICY_SWITCH],2",
                "RB+Right": "[POLICY_SWITCH],3",
                # "LB+Up": "[POLICY_SWITCH],0",
                # "LB+Left": "[POLICY_SWITCH],5",
                # "LB+Down": "[POLICY_SWITCH],6",
                # "LB+Right": "[POLICY_SWITCH],7",
            }
        ),
    ]
    next_policy: dict[int, int] = {
        0: 5,
        5: 4,
    }
    