from flask import Response, Blueprint, render_template, current_app, request, redirect, abort, url_for, send_from_directory, jsonify
from app.core.paths import STATIC_PATH, TEMPLATES_PATH
from threading import Lock
from datetime import datetime
from urllib.parse import urlencode, urlparse, parse_qs, urlunparse
from app.services.fileio import append_csv_row, update_csv_row
from pathlib import Path
from werkzeug.utils import secure_filename


session = Blueprint("session", __name__, static_folder=STATIC_PATH, template_folder=TEMPLATES_PATH)
advance_lock = Lock()


@session.route("/stats", methods=["GET"])
def stats():
    with open(current_app.config["participant_data_file"], "r", encoding="utf-8") as f:
        csv_text = f.read()
    return Response(csv_text, mimetype="text/csv")

@session.route("/settings", methods=["POST"])
def set_settings():
    current_app.config["session_settings"] = {
        "start_time": datetime.utcnow(),
        "participant_id": request.form.get("participant-id"),
        "sona_paid_id": request.form.get("sona-paid-id"),
        "set": request.form.get("counterbalance-order"),
        "source": request.form.get("source"),
        "dry_run": request.form.get("dry-run") is not None,
        "condition": request.form.get("condition"),
        "sequence": request.form.get("screen-selection")
    }
    session_settings = current_app.config.get("session_settings")
    session_controller = current_app.extensions.get("session_controller")
    session_controller.set_seed(session_settings.get("participant_id"))
    session_controller.set_selected_set(session_settings.get("set"))
    session_controller.set_selected_sequence(session_settings.get("sequence"))
    session_controller.process_modules()

    if not session_settings.get("dry_run"):
        config_path = current_app.config["config_path"]
        participant_folder_name = ( 
            f"{session_settings.get('participant_id')}" 
            f"{'_' + session_settings.get('sona_paid_id') if session_settings.get('sona_paid_id') not in (None, '') else ''}" 
            f"_{session_settings.get('start_time').strftime('%Y%m%d_%H%M%S')}" 
        )

        current_app.config["audio_folder"] = config_path / "participant_data" / "responses" / "audio" / participant_folder_name
        current_app.config["text_folder"] = config_path / "participant_data" / "responses" / "text" / participant_folder_name
        current_app.config["audio_folder"].mkdir(parents=True, exist_ok=True)
        current_app.config["text_folder"].mkdir(parents=True, exist_ok=True)
        append_csv_row(
            current_app.config["participant_data_file"],
            session_settings,
            [
                "participant_id",
                "sona_paid_id",
                "set",
                "source",
                "dry_run",
                "condition",
                "sequence",
                "start_time",
                "end_time"
            ]
        )
    
    return redirect(url_for("session.get_page", query_module_index=0, query_trial_index=0))

@session.route('/page/<int:query_module_index>/<int:query_trial_index>', methods=["GET"])
def get_page(query_module_index, query_trial_index):
    session_controller = current_app.extensions.get("session_controller")

    with advance_lock:
        server_module_index = session_controller.get_current_module_index()
        server_trial_index = session_controller.get_current_trial_index()
        experiment_name = session_controller.get_experiment_name()
        set_names = session_controller.get_set_names()

        if server_module_index is None:
            return render_template("startup/startup.html", experiment_name=experiment_name, set_names=set_names)

        if query_module_index < server_module_index:
            return redirect(url_for("session.get_page", query_module_index=server_module_index, query_trial_index=server_trial_index))
        elif query_module_index > server_module_index:
            if query_module_index == server_module_index + 1:
                server_module_index = session_controller.increment_current_module_index()
                server_trial_index = session_controller.get_current_trial_index()
                if session_controller.is_complete() and not current_app.config.get("session_settings").get("dry_run"):
                    update_csv_row(
                        current_app.config["participant_data_file"],
                        -1,
                        {
                            "end_time": datetime.utcnow(),
                        }
                    )
                    return render_template("complete.html")
            else:
                abort(409, description="Invalid page progression")
        elif query_module_index == server_module_index:
            if query_trial_index < server_trial_index:
                return redirect(url_for("session.get_page", query_module_index=server_module_index, query_trial_index=server_trial_index))
            elif query_trial_index > server_trial_index:
                if query_trial_index == server_trial_index + 1:
                    server_trial_index = session_controller.increment_current_trial_index()
                else:
                    abort(409, description="Invalid page progression")
    
    try:
        module = session_controller.get_current_module()
    except ValueError:
        return render_template("startup/startup.html", experiment_name=experiment_name, set_names=set_names)
    
    next_url = url_for(
        "session.get_page",
        query_module_index=server_module_index + 1,
        query_trial_index=0,
        _external=True
    )

    if "url" in module:
        module["url"] = append_url_query_params(module["url"], next_url)
    
    template = module.get('template')
    if template == "web_link":
        return redirect(module.get("url"))
    else:
        return render_template(
            f"{template}.html",
            module_index=server_module_index,
            trial_index=server_trial_index,
            next_url=next_url,
            sona_id=current_app.config.get("session_settings").get("sona_paid_id"),
            participant_id=current_app.config.get("session_settings").get("participant_id"),
            **module
        )

@session.route("/assets/<path:filename>")
def experiment_assets(filename):
    return send_from_directory(current_app.config["config_path"], filename)

@session.route("/responses/save_audio", methods=["POST"])
def save_audio():
    if current_app.config.get("session_settings").get("dry_run"):
        return jsonify({"status": "ok"}), 200

    if "file" not in request.files:
        abort(400, description="No file provided")
    
    file = request.files["file"]
    if file.filename == "":
        abort(400, description="No filename provided")
    
    audio_folder = current_app.config["audio_folder"]
    save_path = audio_folder / f"{current_app.config.get('session_settings').get('participant_id')}_{secure_filename(file.filename)}"
    file.save(save_path)
    return jsonify({"status": "ok"}), 200

@session.route("/responses/save_transcript", methods=["POST"])
def save_transcript():
    if current_app.config.get("session_settings").get("dry_run"):
        return jsonify({"status": "ok"}), 200
        
    if "file" not in request.files:
        abort(400, description="No file provided")
    
    file = request.files["file"]
    if file.filename == "":
        abort(400, description="No filename provided")
    
    text_folder = current_app.config["text_folder"]
    save_path = text_folder / f"{current_app.config.get('session_settings').get('participant_id')}_{secure_filename(file.filename)}"
    file.save(save_path)
    return jsonify({"status": "ok"}), 200

def append_url_query_params(url, redirect_url):    
    url_parts = list(urlparse(url))
    query = parse_qs(url_parts[4])
    query["redirect_url"] = [redirect_url]
    query["sona_id"] = [current_app.config.get("session_settings").get("sona_paid_id")]
    query["participant_id"] = [current_app.config.get("session_settings").get("participant_id")]
    url_parts[4] = urlencode(query, doseq=True)
    return urlunparse(url_parts)