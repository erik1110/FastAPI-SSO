from models.customer import Customer
from schema.valdate import PyObjectId
from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException, Query
from fastapi_sso.sso.google import GoogleSSO
from fastapi_sso.sso.facebook import FacebookSSO
from starlette.requests import Request
from rich.console import Console
import json
import os

load_dotenv()
console = Console()
router = APIRouter()

GOOGLE_OAUTH_CLIENT_ID=os.getenv("GOOGLE_OAUTH_CLIENT_ID")
GOOGLE_OAUTH_CLIENT_SECRET=os.getenv("GOOGLE_OAUTH_CLIENT_SECRET")
GOOGLE_CALLBACK_URL=os.getenv("GOOGLE_CALLBACK_URL")
FACEBOOK_OAUTH_CLIENT_ID=os.getenv("FACEBOOK_OAUTH_CLIENT_ID")
FACEBOOK_OAUTH_CLIENT_SECRET=os.getenv("FACEBOOK_OAUTH_CLIENT_SECRET")
FACEBOOK_CALLBACK_URL=os.getenv("FACEBOOK_CALLBACK_URL")

google_sso = GoogleSSO(
    client_id=GOOGLE_OAUTH_CLIENT_ID,
    client_secret=GOOGLE_OAUTH_CLIENT_SECRET,
    redirect_uri=GOOGLE_CALLBACK_URL,
    allow_insecure_http=False,
)

facebook_sso = FacebookSSO(
    client_id=FACEBOOK_OAUTH_CLIENT_ID,
    client_secret=FACEBOOK_OAUTH_CLIENT_SECRET,
    redirect_uri=FACEBOOK_CALLBACK_URL,
    allow_insecure_http=False,
)

@router.get("/google/auth/login", summary="Google 第三方登入")
async def auth_init(campaignName: str = Query(..., description="Campaign 名稱")):
    """Initialize auth and redirect"""
    state_params = {"campaignName": campaignName}
    return await google_sso.get_login_redirect(params={"prompt": "consent", "access_type": "offline"}, state=state_params)


@router.get("/google/auth/callback", summary="Google 第三方登入 Callback")
async def auth_callback(request: Request):
    """Verify login"""
    state = request.query_params.get("state", {}).replace("'", "\"")
    state = json.loads(state)
    campaign_name = state["campaignName"]
    info = await google_sso.verify_and_process(request)
    result = await Customer.find_one(Customer.campaign==campaign_name, Customer.sso_id== info.id)
    if result is None:
        customer = Customer(campaign=campaign_name,
                            sso="google",
                            sso_id=info.id,
                            info=info,
        )
        result = await customer.create()
    return result

@router.get("/facebook/auth/login", summary="FB第三方登入")
async def auth_init_facebook(campaignName: str = Query(..., description="Campaign 名稱")):
    """Initialize auth and redirect"""
    state_params = {"campaignName": campaignName}
    return await facebook_sso.get_login_redirect(params={"prompt": "consent", "access_type": "offline"}, state=state_params)


@router.get("/facebook/auth/callback", summary="FB第三方登入 Callback")
async def auth_callback_facebook(request: Request):
    """Verify login"""
    state = request.query_params.get("state", {}).replace("'", "\"")
    state = json.loads(state)
    campaign_name = state["campaignName"]
    info = await facebook_sso.verify_and_process(request)
    # result = await Customer.find_one(Customer.campaign==campaign_name, Customer.sso_id== info.id)
    # if result is None:
    #     customer = Customer(campaign=campaign_name,
    #                         sso="google",
    #                         sso_id=info.id,
    #                         info=info,
    #     )
    #     result = await customer.create()
    return info

@router.get("/userInfo", summary="查詢使用者資訊")
async def get_user_info(userId: PyObjectId = Query(..., description="使用者ID")):
    result = await Customer.get(userId)
    if result is None:
        error_message = f"The userId is not exists."
        raise HTTPException(status_code=400, detail=error_message)
    return result