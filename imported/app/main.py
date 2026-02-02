from pathlib import Path
import time
import csv
import io
from datetime import datetime, timedelta

from fastapi import FastAPI, File, Form, Request, UploadFile
from fastapi.responses import HTMLResponse, RedirectResponse, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.db import (
    UPLOADS_DIR,
    create_chat_message,
    create_insight,
    create_kpi_entry,
    create_post_entry,
    create_profile_analysis,
    create_roadmap,
    create_user,
    get_profile_analysis_by_id,
    get_stats,
    get_user_by_email,
    get_user_by_id,
    init_db,
    list_chat_messages,
    list_kpi_entries,
    list_profile_analyses,
    list_insights,
    list_post_entries,
    list_roadmaps,
)
from app.i18n import LANGUAGE_LABELS, SUPPORTED_LANGS, get_translations
import json

from app.services.profile_analysis import analyze_profile, translate_analysis_result
from app.security import create_session_cookie, hash_password, parse_session_cookie, verify_password


def _validate_password(password: str) -> bool:
    """Exige: mínimo 6 caracteres, maiúscula, minúscula, carácter especial e um número."""
    if len(password) < 6:
        return False
    if not any(c.isupper() for c in password) or not any(c.islower() for c in password):
        return False
    if not any(not c.isalnum() for c in password):
        return False
    if not any(c.isdigit() for c in password):
        return False
    return True


BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

app = FastAPI(title="LinkedIn Optimizer Assistant")

app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")


@app.on_event("startup")
def on_startup():
    init_db()


def _get_current_user(request: Request):
    cookie_value = request.cookies.get("session")
    if not cookie_value:
        return None
    session = parse_session_cookie(cookie_value)
    if not session:
        return None
    return get_user_by_id(session.user_id)


def _require_login(request: Request):
    user = _get_current_user(request)
    if not user:
        return None, RedirectResponse(url="/login", status_code=303)
    return user, None


def _get_lang(request: Request) -> str:
    lang = request.query_params.get("lang") or request.cookies.get("lang") or "pt-PT"
    if lang not in SUPPORTED_LANGS:
        lang = "pt-PT"
    return lang


def _template_response(request: Request, name: str, context: dict):
    lang = _get_lang(request)
    base_context = {
        "request": request,
        "lang": lang,
        "t": get_translations(lang),
        "user": _get_current_user(request),
        "languages": [
            {"code": code, "label": LANGUAGE_LABELS[code]} for code in SUPPORTED_LANGS
        ],
    }
    response = templates.TemplateResponse(name, {**base_context, **context})
    if request.query_params.get("lang") in SUPPORTED_LANGS:
        response.set_cookie("lang", lang, samesite="lax")
    return response


@app.get("/", response_class=HTMLResponse)
def landing(request: Request):
    user = _get_current_user(request)
    return _template_response(request, "landing.html", {"user": user})


@app.get("/register", response_class=HTMLResponse)
def register_form(request: Request):
    return _template_response(request, "register.html", {"error": None})


@app.post("/register")
def register_submit(
    request: Request,
    first_name: str = Form(...),
    last_name: str = Form(...),
    email: str = Form(...),
    country_code: str = Form(...),
    phone: str = Form(...),
    nif: str = Form(""),
    password: str = Form(...),
):
    existing = get_user_by_email(email.lower().strip())
    if existing:
        lang = _get_lang(request)
        response = _template_response(
            request,
            "register.html",
            {"error": get_translations(lang)["error_email_exists"]},
        )
        response.status_code = 400
        return response
    lang = _get_lang(request)
    if not _validate_password(password):
        response = _template_response(
            request,
            "register.html",
            {"error": get_translations(lang)["error_password_rules"]},
        )
        response.status_code = 400
        return response
    password_hash = hash_password(password)
    phone_value = f"{country_code} {phone}".strip()
    user_id = create_user(
        email.lower().strip(),
        password_hash,
        first_name.strip(),
        last_name.strip(),
        phone_value,
        nif.strip(),
    )
    response = RedirectResponse(url="/backoffice", status_code=303)
    response.set_cookie("session", create_session_cookie(user_id), httponly=True, samesite="lax")
    return response


@app.get("/login", response_class=HTMLResponse)
def login_form(request: Request):
    return _template_response(request, "login.html", {"error": None})


@app.post("/login")
def login_submit(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
):
    user = get_user_by_email(email.lower().strip())
    if not user or not verify_password(password, user["password_hash"]):
        lang = _get_lang(request)
        response = _template_response(
            request,
            "login.html",
            {"error": get_translations(lang)["error_invalid_credentials"]},
        )
        response.status_code = 400
        return response
    response = RedirectResponse(url="/backoffice", status_code=303)
    response.set_cookie("session", create_session_cookie(int(user["id"])), httponly=True, samesite="lax")
    return response


@app.post("/logout")
def logout():
    response = RedirectResponse(url="/", status_code=303)
    response.delete_cookie("session")
    return response


@app.get("/backoffice", response_class=HTMLResponse)
def backoffice_dashboard(request: Request):
    user, redirect = _require_login(request)
    if redirect:
        return redirect
    stats = get_stats(int(user["id"]))
    roadmaps = list_roadmaps(int(user["id"]))
    insights = list_insights(int(user["id"]))
    analyses = _normalize_analyses(list_profile_analyses(int(user["id"])))
    error = request.query_params.get("error")
    new_analysis_id = request.query_params.get("new_analysis_id")
    new_analysis_lang = request.query_params.get("new_analysis_lang")
    translated = request.query_params.get("translated")
    return _template_response(
        request,
        "backoffice.html",
        {
            "user": user,
            "stats": stats,
            "roadmaps": roadmaps,
            "insights": insights,
            "analyses": analyses,
            "error": error,
            "new_analysis_id": new_analysis_id,
            "new_analysis_lang": new_analysis_lang,
            "translated": translated,
            "supported_langs": SUPPORTED_LANGS,
            "language_labels": LANGUAGE_LABELS,
        },
    )


@app.get("/backoffice/history", response_class=HTMLResponse)
def backoffice_history(request: Request):
    user, redirect = _require_login(request)
    if redirect:
        return redirect
    analyses = _normalize_analyses(list_profile_analyses(int(user["id"])))
    roadmaps = list_roadmaps(int(user["id"]))
    insights = list_insights(int(user["id"]))
    messages = list_chat_messages(int(user["id"]))
    return _template_response(
        request,
        "history.html",
        {
            "user": user,
            "analyses": analyses,
            "roadmaps": roadmaps,
            "insights": insights,
            "messages": messages,
        },
    )


@app.get("/chat", response_class=HTMLResponse)
def chat_page(request: Request):
    user, redirect = _require_login(request)
    if redirect:
        return redirect
    messages = list_chat_messages(int(user["id"]))
    return _template_response(
        request,
        "chat.html",
        {
            "user": user,
            "messages": messages,
        },
    )


@app.post("/chat")
def chat_send(
    request: Request,
    message: str = Form(...),
):
    user, redirect = _require_login(request)
    if redirect:
        return redirect
    content = message.strip()
    if content:
        create_chat_message(int(user["id"]), "user", content)
        lang = _get_lang(request)
        placeholder = get_translations(lang)["chat_placeholder_reply"]
        create_chat_message(int(user["id"]), "assistant", placeholder)
    return RedirectResponse(url="/chat", status_code=303)


@app.get("/kpis", response_class=HTMLResponse)
def kpis_page(request: Request):
    user, redirect = _require_login(request)
    if redirect:
        return redirect
    kpi_entries = list_kpi_entries(int(user["id"]))
    post_entries = list_post_entries(int(user["id"]))
    format_filter = request.query_params.get("format") or "all"
    case_filter = request.query_params.get("case") or "all"
    if format_filter != "all":
        post_entries = [p for p in post_entries if p.get("format") == format_filter]
    if case_filter == "case":
        post_entries = [p for p in post_entries if int(p.get("is_case_study") or 0) == 1]
    kpi_summary = _kpi_summary(kpi_entries)
    post_highlights = _post_highlights(post_entries)
    kpi_trends = _kpi_trends(kpi_entries)
    post_trends = _post_trends(post_entries)
    kpi_weekly = _aggregate_weekly(
        kpi_entries,
        "entry_date",
        ["connection_invites", "events_attended", "new_connections", "profile_views"],
    )
    post_weekly = _aggregate_weekly(
        post_entries,
        "post_date",
        ["posts", "reach", "saves", "meaningful_comments", "shares", "dwell_time_seconds"],
        count_field="posts",
    )
    kpi_monthly = _aggregate_monthly(
        kpi_entries,
        "entry_date",
        ["connection_invites", "events_attended", "new_connections", "profile_views"],
    )
    post_monthly = _aggregate_monthly(
        post_entries,
        "post_date",
        ["posts", "reach", "saves", "meaningful_comments", "shares", "dwell_time_seconds"],
        count_field="posts",
    )
    kpi_monthly = _add_monthly_deltas(
        kpi_monthly,
        ["connection_invites", "new_connections", "profile_views"],
    )
    post_monthly = _add_monthly_deltas(
        post_monthly,
        ["saves", "reach"],
    )
    return _template_response(
        request,
        "kpis.html",
        {
            "user": user,
            "kpi_entries": kpi_entries,
            "post_entries": post_entries,
            "kpi_summary": kpi_summary,
            "post_highlights": post_highlights,
            "kpi_trends": kpi_trends,
            "post_trends": post_trends,
            "format_filter": format_filter,
            "case_filter": case_filter,
            "kpi_weekly": kpi_weekly,
            "post_weekly": post_weekly,
            "kpi_monthly": kpi_monthly,
            "post_monthly": post_monthly,
        },
    )


@app.post("/kpis/entry")
def add_kpi_entry(
    request: Request,
    entry_date: str = Form(...),
    connection_invites: int = Form(0),
    events_attended: int = Form(0),
    new_connections: int = Form(0),
    profile_views: int = Form(0),
    notes: str = Form(""),
):
    user, redirect = _require_login(request)
    if redirect:
        return redirect
    create_kpi_entry(
        int(user["id"]),
        entry_date,
        int(connection_invites),
        int(events_attended),
        int(new_connections),
        int(profile_views),
        notes.strip(),
    )
    return RedirectResponse(url="/kpis", status_code=303)


@app.post("/kpis/post")
def add_post_entry(
    request: Request,
    post_date: str = Form(...),
    title: str = Form(...),
    format_value: str = Form(...),
    impressions: int = Form(0),
    reach: int = Form(0),
    saves: int = Form(0),
    comments: int = Form(0),
    meaningful_comments: int = Form(0),
    likes: int = Form(0),
    shares: int = Form(0),
    clicks: int = Form(0),
    dwell_time_seconds: int = Form(0),
    is_case_study: str = Form("off"),
    notes: str = Form(""),
):
    user, redirect = _require_login(request)
    if redirect:
        return redirect
    create_post_entry(
        int(user["id"]),
        post_date,
        title.strip(),
        format_value,
        int(impressions),
        int(reach),
        int(saves),
        int(comments),
        int(meaningful_comments),
        int(likes),
        int(shares),
        int(clicks),
        int(dwell_time_seconds),
        1 if is_case_study == "on" else 0,
        notes.strip(),
    )
    return RedirectResponse(url="/kpis", status_code=303)


@app.get("/kpis/export")
def export_kpis(request: Request):
    user, redirect = _require_login(request)
    if redirect:
        return redirect
    entries = list_kpi_entries(int(user["id"]))
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(
        [
            "entry_date",
            "connection_invites",
            "events_attended",
            "new_connections",
            "profile_views",
            "notes",
        ]
    )
    for item in entries:
        writer.writerow(
            [
                item["entry_date"],
                item["connection_invites"],
                item["events_attended"],
                item["new_connections"],
                item["profile_views"],
                item["notes"],
            ]
        )
    return Response(
        content=output.getvalue(),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=kpis.csv"},
    )


@app.get("/kpis/posts/export")
def export_posts(request: Request):
    user, redirect = _require_login(request)
    if redirect:
        return redirect
    entries = list_post_entries(int(user["id"]))
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(
        [
            "post_date",
            "title",
            "format",
            "impressions",
            "reach",
            "saves",
            "comments",
            "meaningful_comments",
            "likes",
            "shares",
            "clicks",
            "dwell_time_seconds",
            "is_case_study",
            "notes",
        ]
    )
    for item in entries:
        writer.writerow(
            [
                item["post_date"],
                item["title"],
                item["format"],
                item["impressions"],
                item["reach"],
                item["saves"],
                item["comments"],
                item.get("meaningful_comments", 0),
                item["likes"],
                item.get("shares", 0),
                item["clicks"],
                item.get("dwell_time_seconds", 0),
                item["is_case_study"],
                item["notes"],
            ]
        )
    return Response(
        content=output.getvalue(),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=posts.csv"},
    )


@app.post("/backoffice/roadmap")
def add_roadmap(
    request: Request,
    title: str = Form(...),
    content: str = Form(...),
):
    user, redirect = _require_login(request)
    if redirect:
        return redirect
    create_roadmap(int(user["id"]), title.strip(), content.strip())
    return RedirectResponse(url="/backoffice", status_code=303)


@app.post("/backoffice/insight")
def add_insight(
    request: Request,
    summary: str = Form(...),
):
    user, redirect = _require_login(request)
    if redirect:
        return redirect
    create_insight(int(user["id"]), summary.strip())
    return RedirectResponse(url="/backoffice", status_code=303)


@app.post("/backoffice/profile-analysis")
def add_profile_analysis(
    request: Request,
    pdf_file: UploadFile = File(...),
):
    user, redirect = _require_login(request)
    if redirect:
        return redirect
    if not pdf_file.filename.lower().endswith(".pdf"):
        return RedirectResponse(url="/backoffice?error=pdf", status_code=303)
    original_name = Path(pdf_file.filename).name
    safe_name = f"user_{user['id']}_{time.time_ns()}_{original_name}"
    file_path = UPLOADS_DIR / safe_name
    with open(file_path, "wb") as f:
        f.write(pdf_file.file.read())
    lang = _get_lang(request)
    try:
        analysis = analyze_profile(str(file_path), lang)
        analysis_id = create_profile_analysis(
            int(user["id"]),
            "pdf",
            str(file_path),
            "Concluído",
            analysis.score,
            analysis.summary,
            analysis.recommendations,
            analysis.red_flags,
            analysis.report,
            lang=lang,
        )
        return RedirectResponse(
            url=f"/backoffice?new_analysis_id={analysis_id}&new_analysis_lang={lang}",
            status_code=303,
        )
    except Exception:
        create_profile_analysis(int(user["id"]), "pdf", str(file_path), "Erro", lang=lang)
    return RedirectResponse(url="/backoffice", status_code=303)


@app.post("/backoffice/profile-analysis/translate")
def translate_profile_analysis(
    request: Request,
    analysis_id: int = Form(...),
    target_lang: str = Form(...),
):
    user, redirect = _require_login(request)
    if redirect:
        return redirect
    if target_lang not in SUPPORTED_LANGS:
        return RedirectResponse(url="/backoffice?error=translate", status_code=303)
    row = get_profile_analysis_by_id(int(user["id"]), analysis_id)
    if not row:
        return RedirectResponse(url="/backoffice?error=translate", status_code=303)
    item = dict(row)
    try:
        item["recommendations"] = json.loads(item.get("recommendations") or "[]")
    except Exception:
        item["recommendations"] = []
    try:
        item["red_flags"] = json.loads(item.get("red_flags") or "[]")
    except Exception:
        item["red_flags"] = []
    try:
        item["report"] = json.loads(item.get("report_json") or "[]")
    except Exception:
        item["report"] = []
    source_lang = item.get("lang") or "pt-PT"
    if source_lang == target_lang:
        return RedirectResponse(url="/backoffice", status_code=303)
    summary_t, recs_t, flags_t, report_t = translate_analysis_result(
        item.get("summary") or "",
        item["recommendations"],
        item["red_flags"],
        item["report"],
        source_lang,
        target_lang,
    )
    create_profile_analysis(
        int(user["id"]),
        item.get("source") or "pdf",
        item.get("file_path"),
        "Concluído",
        item.get("score"),
        summary_t,
        recs_t,
        flags_t,
        report_t,
        lang=target_lang,
        source_analysis_id=analysis_id,
    )
    return RedirectResponse(url="/backoffice?translated=1", status_code=303)


def _normalize_analyses(rows):
    normalized = []
    for row in rows:
        item = dict(row)
        try:
            item["recommendations"] = json.loads(item.get("recommendations") or "[]")
        except Exception:
            item["recommendations"] = []
        try:
            item["red_flags"] = json.loads(item.get("red_flags") or "[]")
        except Exception:
            item["red_flags"] = []
        try:
            item["report"] = json.loads(item.get("report_json") or "[]")
        except Exception:
            item["report"] = []
        normalized.append(item)
    return normalized


def _parse_date(value: str):
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except Exception:
        return None


def _week_key(date_value):
    iso = date_value.isocalendar()
    return f"{iso.year}-W{iso.week:02d}"


def _month_key(date_value):
    return f"{date_value.year}-{date_value.month:02d}"


def _aggregate_weekly(entries, date_field, metrics, count_field=None):
    buckets = {}
    for item in entries:
        date_value = _parse_date(item.get(date_field, ""))
        if not date_value:
            continue
        key = _week_key(date_value)
        buckets.setdefault(key, {metric: 0 for metric in metrics})
        for metric in metrics:
            if metric == count_field:
                buckets[key][metric] += 1
            else:
                buckets[key][metric] += int(item.get(metric) or 0)
    return _normalize_buckets(buckets, metrics)


def _aggregate_monthly(entries, date_field, metrics, count_field=None):
    buckets = {}
    for item in entries:
        date_value = _parse_date(item.get(date_field, ""))
        if not date_value:
            continue
        key = _month_key(date_value)
        buckets.setdefault(key, {metric: 0 for metric in metrics})
        for metric in metrics:
            if metric == count_field:
                buckets[key][metric] += 1
            else:
                buckets[key][metric] += int(item.get(metric) or 0)
    return _normalize_buckets(buckets, metrics)


def _normalize_buckets(buckets, metrics):
    rows = []
    max_values = {metric: 1 for metric in metrics}
    for values in buckets.values():
        for metric in metrics:
            max_values[metric] = max(max_values[metric], values.get(metric, 0))
    for key in sorted(buckets.keys(), reverse=True):
        row = {"period": key, **buckets[key]}
        row["percentages"] = {
            metric: round((row[metric] / max_values[metric]) * 100, 1)
            for metric in metrics
        }
        rows.append(row)
    return rows


def _add_monthly_deltas(rows, metrics):
    updated = []
    for idx, row in enumerate(rows):
        previous = rows[idx + 1] if idx + 1 < len(rows) else None
        delta = {}
        for metric in metrics:
            current_value = row.get(metric, 0)
            previous_value = previous.get(metric, 0) if previous else 0
            diff = current_value - previous_value
            if previous_value > 0:
                percent = round((diff / previous_value) * 100, 1)
            else:
                percent = 0.0
            delta[metric] = {"diff": diff, "percent": percent}
        row["delta"] = delta
        updated.append(row)
    return updated


def _kpi_summary(entries):
    summary = {
        "total_invites": 0,
        "total_events": 0,
        "total_new_connections": 0,
        "total_profile_views": 0,
        "entries_count": len(entries),
    }
    for item in entries:
        summary["total_invites"] += int(item.get("connection_invites") or 0)
        summary["total_events"] += int(item.get("events_attended") or 0)
        summary["total_new_connections"] += int(item.get("new_connections") or 0)
        summary["total_profile_views"] += int(item.get("profile_views") or 0)
    return summary


def _post_highlights(entries):
    if not entries:
        return {
            "top_saves": None,
            "top_reach": None,
            "top_dwell": None,
            "top_meaningful": None,
            "case_studies": 0,
        }
    top_saves = max(entries, key=lambda e: int(e.get("saves") or 0))
    top_reach = max(entries, key=lambda e: int(e.get("reach") or 0))
    top_dwell = max(entries, key=lambda e: int(e.get("dwell_time_seconds") or 0))
    top_meaningful = max(entries, key=lambda e: int(e.get("meaningful_comments") or 0))
    case_studies = sum(1 for e in entries if int(e.get("is_case_study") or 0) == 1)
    return {
        "top_saves": dict(top_saves),
        "top_reach": dict(top_reach),
        "top_dwell": dict(top_dwell),
        "top_meaningful": dict(top_meaningful),
        "case_studies": case_studies,
    }


def _kpi_trends(entries):
    today = datetime.utcnow().date()
    ranges = {
        "last_7_days": today - timedelta(days=7),
        "last_30_days": today - timedelta(days=30),
    }
    trends = {
        "last_7_days": {"invites": 0, "events": 0, "connections": 0, "views": 0},
        "last_30_days": {"invites": 0, "events": 0, "connections": 0, "views": 0},
    }
    for item in entries:
        entry_date = _parse_date(item.get("entry_date", ""))
        if not entry_date:
            continue
        for key, start_date in ranges.items():
            if entry_date >= start_date:
                trends[key]["invites"] += int(item.get("connection_invites") or 0)
                trends[key]["events"] += int(item.get("events_attended") or 0)
                trends[key]["connections"] += int(item.get("new_connections") or 0)
                trends[key]["views"] += int(item.get("profile_views") or 0)
    return trends


def _post_trends(entries):
    today = datetime.utcnow().date()
    ranges = {
        "last_7_days": today - timedelta(days=7),
        "last_30_days": today - timedelta(days=30),
    }
    trends = {
        "last_7_days": {
            "saves": 0,
            "reach": 0,
            "impressions": 0,
            "posts": 0,
            "meaningful_comments": 0,
            "shares": 0,
            "dwell_time_seconds": 0,
        },
        "last_30_days": {
            "saves": 0,
            "reach": 0,
            "impressions": 0,
            "posts": 0,
            "meaningful_comments": 0,
            "shares": 0,
            "dwell_time_seconds": 0,
        },
    }
    for item in entries:
        post_date = _parse_date(item.get("post_date", ""))
        if not post_date:
            continue
        for key, start_date in ranges.items():
            if post_date >= start_date:
                trends[key]["saves"] += int(item.get("saves") or 0)
                trends[key]["reach"] += int(item.get("reach") or 0)
                trends[key]["impressions"] += int(item.get("impressions") or 0)
                trends[key]["meaningful_comments"] += int(item.get("meaningful_comments") or 0)
                trends[key]["shares"] += int(item.get("shares") or 0)
                trends[key]["dwell_time_seconds"] += int(item.get("dwell_time_seconds") or 0)
                trends[key]["posts"] += 1
    return trends
