"""
app.py
------
Chichewa Noun Classifier — Flask application.

Production-ready changes vs. the original:
  - No pandas / numpy / scipy imports.
  - ML model is NOT loaded at startup; it is lazily loaded on first request
    via model_loader.get_model().
  - CSV data is replaced by a SQLite database accessed through
    database.db (SQLAlchemy Core).
  - All classification logic lives in classifier.py (single source of truth).
"""

import traceback
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

try:
    from detector   import detect_language
    from explainer  import get_full_explanation, get_class_comparison
    from classifier import CLASS_INFO, rule_classify, ml_classify, get_morphology
    from database.db import (
        get_examples,
        get_class_info,
        get_all_classes,
        close_db,
    )

    # ── Close the DB connection at the end of every request context ───────────────
    app.teardown_appcontext(close_db)

    # ═══════════════════════════════════════════════════════════════════════════════
    # ROUTES
    # ═══════════════════════════════════════════════════════════════════════════════

    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/classify", methods=["POST"])
    def classify():
        noun = request.form.get("noun", "").strip()

        if not noun:
            return render_template("index.html", error="Please enter a Chichewa noun.")

        if len(noun) < 2:
            return render_template("index.html", error="Please enter a longer noun.")

        # ── Language detection ────────────────────────────────────────────────────
        lang_result = detect_language(noun)

        if not lang_result["is_chichewa"]:
            return render_template(
                "index.html",
                error=f'"{noun}" is not a valid Chichewa noun.',
            )

        # ── Rule-based classification ─────────────────────────────────────────────
        rule_class, rule_conf, rule_reason = rule_classify(noun)

        # ── ML classification (lazy model load on first call) ─────────────────────
        ml_class, ml_conf, all_scores = ml_classify(noun)

        # ── Hybrid decision ───────────────────────────────────────────────────────
        if rule_class and rule_conf >= 0.88:
            predicted  = rule_class
            confidence = round(rule_conf * 100, 1)
            method     = "Rule-Based"
        else:
            predicted  = ml_class
            confidence = round(ml_conf * 100, 1)
            method     = "Machine Learning"

        # ── Morphological breakdown ───────────────────────────────────────────────
        morphology = get_morphology(noun, predicted)

        # ── Full explanation ──────────────────────────────────────────────────────
        explanation = get_full_explanation(
            noun, predicted, method, confidence,
            morphology, lang_result["is_chichewa"], lang_result["reason"],
        )

        # ── Class comparison chart data ───────────────────────────────────────────
        all_scores_pct = {k: round(v * 100, 1) for k, v in all_scores.items()}
        comparison     = get_class_comparison(predicted, all_scores_pct)

        # ── Examples from DB (replaces pandas dataset.sample()) ──────────────────
        examples   = get_examples(predicted, noun)

        # ── Class metadata ────────────────────────────────────────────────────────
        class_info = CLASS_INFO.get(predicted, {})

        return render_template(
            "result.html",
            noun        = noun,
            predicted   = predicted,
            confidence  = confidence,
            method      = method,
            explanation = explanation,
            morphology  = morphology,
            comparison  = comparison,
            examples    = examples,
            class_info  = class_info,
            lang_result = lang_result,
            all_scores  = all_scores_pct,
        )

    @app.route("/classes")
    def classes():
        """
        Render the full noun class listing page.
        Data comes from the DB instead of the pandas dataset.
        """
        all_cls = get_all_classes()
        return render_template(
            "classes.html",
            class_info = CLASS_INFO,    # kept for backward-compat with template
            all_classes = all_cls,      # richer DB-sourced list for future use
        )

    @app.route("/api/classify", methods=["POST"])
    def api_classify():
        """JSON API endpoint for programmatic access."""
        data = request.get_json(silent=True) or {}
        noun = data.get("noun", "").strip()

        if not noun:
            return jsonify({"error": "No noun provided"}), 400

        lang_result               = detect_language(noun)
        rule_class, rule_conf, _  = rule_classify(noun)
        ml_class, ml_conf, scores = ml_classify(noun)

        if rule_class and rule_conf >= 0.88:
            predicted  = rule_class
            confidence = round(rule_conf * 100, 1)
            method     = "Rule-Based"
        else:
            predicted  = ml_class
            confidence = round(ml_conf * 100, 1)
            method     = "Machine Learning"

        return jsonify({
            "noun":        noun,
            "predicted":   predicted,
            "confidence":  confidence,
            "method":      method,
            "is_chichewa": lang_result["is_chichewa"],
            "warning":     lang_result["warnings"],
            "class_info":  CLASS_INFO.get(predicted, {}),
        })

    @app.errorhandler(500)
    def internal_error(e):
        import traceback
        return f"<h1>Flask Runtime Error</h1><pre>{traceback.format_exc()}</pre>", 500

except Exception as e:
    err_msg = traceback.format_exc()
    @app.route("/", defaults={"path": ""})
    @app.route("/<path:path>", methods=["GET", "POST"])
    def error_handler(path):
        return f"<h1>Vercel Initialization Error</h1><pre>{err_msg}</pre>", 500

# ═══════════════════════════════════════════════════════════════════════════════
# ENTRY POINT
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("=" * 55)
    print("  ChiNgeli — Chichewa Noun Classifier")
    print("  Open browser: http://127.0.0.1:5000")
    print("  (ML model loads on first classify request)")
    print("=" * 55)
    app.run(debug=True, host="127.0.0.1", port=5000, use_reloader=False)