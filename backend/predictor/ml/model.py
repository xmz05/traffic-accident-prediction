import numpy as np
from sklearn.linear_model import LogisticRegression

_model = None

def _generate_synthetic_data(n_samples=2000):
    rng = np.random.default_rng(42)
    hours = rng.integers(0, 24, size=n_samples)
    traffic_density = rng.uniform(0, 1, size=n_samples)
    bad_weather = rng.integers(0, 2, size=n_samples)

    is_rush_hour = ((hours >= 7) & (hours <= 10)) | ((hours >= 17) & (hours <= 20))
    is_rush_hour = is_rush_hour.astype(int)

    base_prob = 0.05 + 0.25 * traffic_density + 0.2 * bad_weather + 0.2 * is_rush_hour
    base_prob = np.clip(base_prob, 0, 0.95)
    y = rng.binomial(1, base_prob)

    X = np.column_stack([hours, traffic_density, bad_weather, is_rush_hour])
    return X, y

def init_model():
    global _model
    if _model is None:
        X, y = _generate_synthetic_data()
        clf = LogisticRegression(max_iter=1000)
        clf.fit(X, y)
        _model = clf
    return _model

def predict_probability(hour: int, traffic_density: float, is_bad_weather: int):
    model = init_model()
    is_rush_hour = 1 if (7 <= hour <= 10 or 17 <= hour <= 20) else 0
    X = np.array([[hour, traffic_density, is_bad_weather, is_rush_hour]])
    prob = model.predict_proba(X)[0, 1]
    return float(prob)
