from fastapi import APIRouter, Request, HTTPException, Header, Depends
from svix.webhooks import Webhook, WebhookVerificationError
import stripe
from posthog import Posthog

from app.config import settings

router = APIRouter(prefix="/webhooks", tags=["webhooks"])

posthog = None
if settings.POSTHOG_KEY:
    posthog = Posthog(settings.POSTHOG_KEY, host=settings.POSTHOG_HOST or 'https://us.i.posthog.com')

@router.post("/auth")
async def auth_webhook(
    request: Request,
    svix_id: str = Header(None, alias="svix-id"),
    svix_timestamp: str = Header(None, alias="svix-timestamp"),
    svix_signature: str = Header(None, alias="svix-signature")
):
    if not settings.CLERK_WEBHOOK_SECRET:
        return {"message": "Not configured", "ok": False}
    
    if not svix_id or not svix_timestamp or not svix_signature:
        raise HTTPException(status_code=400, detail="Missing svix headers")

    body = await request.body()
    wh = Webhook(settings.CLERK_WEBHOOK_SECRET)

    try:
        event = wh.verify(body, {
            "svix-id": svix_id,
            "svix-timestamp": svix_timestamp,
            "svix-signature": svix_signature
        })
    except WebhookVerificationError:
        raise HTTPException(status_code=400, detail="Invalid signature")

    event_type = event.get("type")
    data = event.get("data", {})
    user_id = data.get("id")

    if event_type == "user.created":
        if posthog and user_id:
            email = data.get("email_addresses", [{}])[0].get("email_address")
            posthog.identify(user_id, {
                "email": email,
                "firstName": data.get("first_name"),
                "lastName": data.get("last_name"),
            })
            posthog.capture(user_id, "User Created")

    # Handle other events similarly...

    if posthog:
        posthog.flush()

    return {"status": "ok"}

@router.post("/payments")
async def payments_webhook(request: Request, stripe_signature: str = Header(None)):
    if not settings.STRIPE_WEBHOOK_SECRET:
        return {"message": "Not configured", "ok": False}

    body = await request.body()
    
    try:
        event = stripe.Webhook.construct_event(
            body, stripe_signature, settings.STRIPE_WEBHOOK_SECRET
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    # Process Stripe event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        customer_id = session.get('customer')
        # Here we would query clerk to find user by stripeCustomerId
        pass

    return {"status": "ok"}
