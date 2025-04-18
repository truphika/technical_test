from dataclasses import dataclass
import json

from api.entities.network_coverage import NetworkCoverage


@dataclass
class OperatorCoverage:
    bouygues: NetworkCoverage
    free: NetworkCoverage
    orange: NetworkCoverage
    SFR: NetworkCoverage

    def to_json(self):
        return json.dumps(
            {
                "bouygues": self.bouygues.to_dict(),
                "free": self.free.to_dict(),
                "orange": self.orange.to_dict(),
                "SFR": self.SFR.to_dict(),
            }
        )
