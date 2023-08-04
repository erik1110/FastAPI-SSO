from fastapi import APIRouter
from fastapi.openapi.docs import (get_redoc_html, get_swagger_ui_html,
                                  get_swagger_ui_oauth2_redirect_html)
from fastapi.staticfiles import StaticFiles

router = APIRouter()


@router.get("/docs", include_in_schema=False)
def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url="openapi.json",
        title="My SSO Template",
        swagger_js_url="/static/js/swagger-ui-bundle.js",
        swagger_css_url="/static/css/swagger-ui.css"
    )

@router.get("/docs/oauth2-redirect", include_in_schema=False)
def swagger_ui_redirect():
    return get_swagger_ui_oauth2_redirect_html()


@router.get("/redoc", include_in_schema=False)
def redoc_html():
    return get_redoc_html(
        redoc_js_url="/static/js/redoc.standalone.js",
    )