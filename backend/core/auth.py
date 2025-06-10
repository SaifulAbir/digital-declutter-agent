from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from backend.config.settings import settings
from backend.config.database import get_db
from backend.models.user import User
from backend.schemas.user import User as UserSchema
import jwt
from datetime import datetime, timedelta
from typing import Optional

security = HTTPBearer()


class GoogleAuth:
    def __init__(self):
        self.client_config = {
            "web": {
                "client_id": settings.GOOGLE_CLIENT_ID,
                "client_secret": settings.GOOGLE_CLIENT_SECRET,
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "redirect_uris": [settings.GOOGLE_REDIRECT_URI]
            }
        }

    def get_authorization_url(self, state: str = None) -> str:
        """Generate Google OAuth authorization URL"""
        flow = Flow.from_client_config(
            self.client_config,
            scopes=settings.GMAIL_SCOPES + settings.DRIVE_SCOPES,
            redirect_uri=settings.GOOGLE_REDIRECT_URI
        )

        if state:
            flow.state = state

        auth_url, _ = flow.authorization_url(
            access_type='offline',
            include_granted_scopes='true',
            prompt='consent'
        )

        return auth_url

    def exchange_code_for_tokens(self, code: str, state: str = None) -> dict:
        """Exchange authorization code for access tokens"""
        flow = Flow.from_client_config(
            self.client_config,
            scopes=settings.GMAIL_SCOPES + settings.DRIVE_SCOPES,
            redirect_uri=settings.GOOGLE_REDIRECT_URI,
            state=state
        )

        try:
            flow.fetch_token(code=code)
            credentials = flow.credentials

            # Get user info
            user_info = self._get_user_info(credentials)

            return {
                "access_token": credentials.token,
                "refresh_token": credentials.refresh_token,
                "expires_at": credentials.expiry,
                "user_info": user_info
            }
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Token exchange failed: {str(e)}")

    def _get_user_info(self, credentials: Credentials) -> dict:
        """Get user information from Google"""
        service = build('oauth2', 'v2', credentials=credentials)
        user_info = service.userinfo().get().execute()

        return {
            "google_id": user_info.get("id"),
            "email": user_info.get("email"),
            "name": user_info.get("name"),
            "picture": user_info.get("picture")
        }

    def refresh_token(self, refresh_token: str) -> dict:
        """Refresh expired access token"""
        credentials = Credentials(
            token=None,
            refresh_token=refresh_token,
            token_uri=self.client_config["web"]["token_uri"],
            client_id=self.client_config["web"]["client_id"],
            client_secret=self.client_config["web"]["client_secret"]
        )

        try:
            credentials.refresh(Request())
            return {
                "access_token": credentials.token,
                "expires_at": credentials.expiry
            }
        except Exception as e:
            raise HTTPException(status_code=401, detail=f"Token refresh failed: {str(e)}")


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create JWT access token"""
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

    return encoded_jwt


def verify_token(token: str) -> dict:
    """Verify JWT token"""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


async def get_current_user(
        credentials: HTTPAuthorizationCredentials = Depends(security),
        db: Session = Depends(get_db)
) -> UserSchema:
    """Get current authenticated user"""
    token = credentials.credentials
    payload = verify_token(token)

    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return UserSchema.from_orm(user)


def get_user_credentials(user: User) -> Credentials:
    """Get Google credentials for a user"""
    if not user.access_token:
        raise HTTPException(status_code=401, detail="User not authenticated with Google")

    credentials = Credentials(
        token=user.access_token,
        refresh_token=user.refresh_token,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=settings.GOOGLE_CLIENT_ID,
        client_secret=settings.GOOGLE_CLIENT_SECRET
    )

    # Check if token needs refresh
    if credentials.expired and credentials.refresh_token:
        try:
            credentials.refresh(Request())
            # Update user's tokens in database
            # This should be done in a service layer in production
        except Exception as e:
            raise HTTPException(status_code=401, detail="Failed to refresh token")

    return credentials


google_auth = GoogleAuth()