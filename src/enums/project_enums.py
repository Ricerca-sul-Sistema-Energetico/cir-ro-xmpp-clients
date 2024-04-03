from enum import Enum


class CyclicEnums(Enum):
    PWR_CSI = "LD_CIR/CSIMMXU1.TotW.mag"
    PWR_M1 = "LD_CIR/M1MMXU1.TotW.mag"
    PWR_M2 = "LD_CIR/M2MMXU1.TotW.mag"
    PWR_AV = "LD_CIR/M1DWMX1.WMaxSpt.setMag"
    FREQ = "LD_CIR/M1MMXU1.Hz.mag"


class SpontaneousEnums(Enum):
    SECONDS_TIL_TIMEOUT = "LD_CIR/M1DWMX1.Ttli.operTimeout"


class StateAlarmEnums(Enum):
    CSI_STATE = "LD_CIR/CSIDESE1.Beh.stVal"
    CIR_STATUS = "LD_CIR/LLN0.Loc.stVal"
    PWR_MODULATION = "LD_CIR/CSIDAGC1.Beh.stVal"
    CSI_FLEX_AV = "LD_CIR/CSIDAGC1.Flmod.stVal"
    CIR_ANOMALTY = "LD_CIR/CIRLPHD.PhyHealth.stVal"
    CIR_SYNC_ANOMALTY = "LD_CIR/CIRLTMS1.TmSynErr.stVal"


class CommandsADUEnums(Enum):
    PWR_MAX_CSI_DURATION = "LD_CIR/CSIDWMX1.WLimPctSpt.ctlVal"
    PWR_MAX_CSI_UNTIL = "LD_CIR/CSIDWMX2.WLimPctSpt.ctlVal"
    SUSPEND_DURATION = "LD_CIR/CSIDESE1.ClcStr.ctlVal"
    SUSPEND_UNTIL = "LD_CIR/CSIDESE2.ClcStr.ctlVal"


class AcknowledgeADUEnums(Enum):
    ACKNOWLEDGE_MEASURE = "LD_CIR/CIRGGIO1.SPCSO1.ctlVal"
    ACKNOWLEDGE_COMMAND = "LD_CIR/CIRGGIO1.SPCSO2.ctlVal"  # Note: added in this repository


class MessageADUEnums(Enum):
    CYCLIC_MEASURE = "LD_CIR/LLN0.DS_C_Meas"
    SPONT_MEASURE = "LD_CIR/LLN0.DS_S_Meas"
    STATE_ALARM = "LD_CIR/LLN0.DS_S_States"
