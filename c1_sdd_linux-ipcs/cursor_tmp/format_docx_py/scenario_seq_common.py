# -*- coding: utf-8 -*-
"""Shared PlantUML sequence diagram header and SW-Unit participant colors."""

from __future__ import annotations

# Layer-aligned colors (match component UML pale-khaki family in .cursorrules)
COLOR_CORE = "#D4E6F1"
COLOR_QUEUE = "#D4E6F1"
COLOR_OSAL_RTOS = "#D5F5E3"
COLOR_OSAL_LINUX = "#D5F5E3"
COLOR_HAL = "#F5E6CC"
COLOR_LINUX_USER = "#FCF3CF"
COLOR_LINUX_KO = "#FDEBD0"
COLOR_REMOTE = "#E8DAEF"

SEQ_HEADER = """\
@startuml
skinparam backgroundColor #FFFCF5
skinparam sequenceArrowThickness 1.2
skinparam sequence {
  ArrowColor #5C4033
  LifeLineBorderColor #8B7355
  ParticipantBorderColor #8B7355
  BoxBorderColor #A08060
}
skinparam note {
  BackgroundColor #FFF8E8
  BorderColor #B89968
}
skinparam actor {
  BackgroundColor #FAF0E0
  BorderColor #8B7355
}
"""


def participant(unit_id: str, source: str, alias: str, color: str) -> str:
    label = f"{unit_id} ({source})"
    return f'participant "{label}" as {alias} {color}'


# SDD 序列图：每个 participant 须在消息流中使用 activate/deactivate（见 .cursorrules §5.1）
