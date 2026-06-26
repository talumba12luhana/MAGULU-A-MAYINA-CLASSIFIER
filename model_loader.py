"""
model_loader.py
---------------
Thread-safe lazy loader for the Chichewa noun classifier (joblib pickle).

The model is NOT loaded at Flask startup. It is loaded on the first
request that needs it and then cached for the lifetime of the process.

Usage:
    from model_loader import get_model
    model = get_model()

Pattern used: double-checked locking
  - Fast path:  if _model is set, return immediately (no lock acquired).
  - Slow path:  acquire lock, re-check, then load. Guarantees exactly-once
                loading even under concurrent first requests.
"""

import threading
import joblib
import os

MODEL_PATH = os.environ.get("MODEL_PATH", "chichewa_noun_classifier.pkl")

_lock  = threading.Lock()
_model = None          # module-level cache


def get_model():
    """
    Return the loaded scikit-learn pipeline.
    Thread-safe; loads from disk at most once per process.
    """
    global _model

    # Fast path — model already loaded (no lock needed after first call)
    if _model is not None:
        return _model

    # Slow path — first caller loads the model
    with _lock:
        # Re-check inside the lock: another thread may have loaded it
        # between the outer check and acquiring the lock.
        if _model is None:
            print(f"[model_loader] Loading model from '{MODEL_PATH}' ...")
            _model = joblib.load(MODEL_PATH)
            print("[model_loader] Model loaded and cached.")

    return _model
