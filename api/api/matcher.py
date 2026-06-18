from rapidfuzz import fuzz
from typing import List, Dict

class Matcher:
    def __init__(self, config: Dict):
        self.cfg = config
        self.weights = config["fuzzyMatch"]["compositeScoring"]["weights"]
        self.auto_threshold = config["fuzzyMatch"]["compositeScoring"]["autoLinkScoreThreshold"]
        self.suggest_threshold = config["fuzzyMatch"]["compositeScoring"]["suggestScoreThreshold"]

    def _mac_hamming(self, a: str, b: str) -> int:
        a_clean = a.replace(":", "").lower()
        b_clean = b.replace(":", "").lower()
        if len(a_clean) != len(b_clean):
            return 99
        return sum(1 for x, y in zip(a_clean, b_clean) if x != y)

    def score_pair(self, discovery: Dict, asset: Dict) -> float:
        score = 0.0
        total_weight = sum(self.weights.values())
        # serial exact
        if discovery.get("serialNumber") and asset.get("serialNumber") and discovery["serialNumber"] == asset["serialNumber"]:
            score += self.weights["serial"]
        # assetTag exact
        if discovery.get("assetTag") and asset.get("assetTag") and discovery["assetTag"] == asset["assetTag"]:
            score += self.weights["assetTag"]
        # mac exact or fuzzy
        d_macs = discovery.get("macAddresses") or []
        a_macs = asset.get("macAddresses") or []
        if set(d_macs) & set(a_macs):
            score += self.weights["mac"]
        else:
            for dm in d_macs:
                for am in a_macs:
                    if self._mac_hamming(dm, am) <= self.cfg["fuzzyMatch"]["mac"]["maxNibbleDifferences"]:
                        score += self.weights["mac"] * 0.8
                        break
        # hostname fuzzy
        if discovery.get("hostname") and asset.get("hostname"):
            jw = fuzz.WRatio(discovery["hostname"], asset["hostname"]) / 100.0
            score += self.weights["hostname"] * jw
        # model fuzzy
        if discovery.get("model") and asset.get("model"):
            mscore = fuzz.WRatio(discovery["model"], asset["model"]) / 100.0
            score += self.weights["model"] * mscore
        return score / total_weight if total_weight else 0.0

    def suggest(self, discovery: Dict, assets: List[Dict]):
        scored = []
        for a in assets:
            s = self.score_pair(discovery, a)
            scored.append({"assetId": a["id"], "score": round(s, 4)})
        scored.sort(key=lambda x: x["score"], reverse=True)
        return scored[:5]
