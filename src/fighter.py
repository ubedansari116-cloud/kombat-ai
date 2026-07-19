from dataclasses import dataclass, field


@dataclass
class Fighter:
    name: str

    stats: dict = field(default_factory=dict)

    attributes: dict = field(default_factory=dict)

    style: str = ""

    grade: str = ""

    fight_iq: float = 0.0

    strengths: list = field(default_factory=list)

    weaknesses: list = field(default_factory=list)

    gameplan: list = field(default_factory=list)