from statistics import mean


def assess_health(values: list[float], expected_range: tuple[float, float], uptime: float, packet_count: int) -> dict:
    if not values:
        return {"state": "unknown", "reason": "no measurements"}
    average = mean(values)
    static = len(set(values[-5:])) == 1 and len(values) >= 5
    in_range = expected_range[0] <= average <= expected_range[1]
    if static or not in_range:
        return {"state": "degraded", "reason": "physical variation or plausibility failure", "uptime": uptime, "packet_count": packet_count}
    return {"state": "healthy", "uptime": uptime, "packet_count": packet_count}
