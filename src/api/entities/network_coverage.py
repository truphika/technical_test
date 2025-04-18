from dataclasses import dataclass


@dataclass
class NetworkCoverage:
    supports_2G: bool
    supports_3G: bool
    supports_4G: bool
    operator: str

    def __repr__(self) -> str:
        return (
            f"Operator: {self.operator}, 2G: {self.supports_2G}, "
            f"3G: {self.supports_3G}, 4G: {self.supports_4G}"
        )

    def to_dict(self):
        return {
            self.operator: {
                "2G": self.supports_2G,
                "3G": self.supports_3G,
                "4G": self.supports_4G,
            }
        }
