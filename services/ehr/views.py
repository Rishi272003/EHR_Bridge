
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import base64
import urllib
import requests
from django.utils import timezone
from core.models import EHRConnection
from django.shortcuts import redirect

@csrf_exempt
@require_http_methods(["GET"])
def ecw_callback(request):
    """
    ECW OAuth callback handler.
    Receives authorization code from ECW and exchanges it for access token.
    """
    code = request.GET.get("code")
    state = request.GET.get("state")

    if not code:
        return JsonResponse({"error": "Authorization code not provided"}, status=400)

    if not state:
        return JsonResponse({"error": "State parameter not provided"}, status=400)

    try:
        state_parts = state.split(",")

        if len(state_parts) >= 3:
            connection_uuid = state_parts[0]
            ehr_name = state_parts[1]  # eclinicalworks
            app_type = state_parts[2]  # provider or patient
        else:
            # Fallback: try to get connection by UUID only
            connection_uuid = state_parts[0]
            ehr_name = "eclinicalworks"
            app_type = "provider"  # default

        # Get ECW connection directly by UUID
        try:
            ecw_connection = EHRConnection.objects.get(
                uuid=connection_uuid, ehr_name=ehr_name
            )
        except EHRConnection.DoesNotExist:
            return JsonResponse({"error": "ECW connection not found"}, status=404)

        # Prepare headers
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
        }

        # Prepare Basic Auth header (client_id:client_secret)
        client_id = ecw_connection.client_id
        client_secret = ecw_connection.client_secret or ""

        # Create Basic Auth credentials
        auth_credentials = base64.b64encode(
            f"{client_id}:{client_secret}".encode()
        ).decode()
        headers["Authorization"] = f"Basic {auth_credentials}"

        # Prepare payload
        # Use redirect_uri from connection to ensure it matches the authorization request
        redirect_uri = ecw_connection.redirect_uri or request.build_absolute_uri(
            "/callback-uri"
        )
        payload = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": redirect_uri,
        }

        # Add code_verifier if available (PKCE flow)
        if ecw_connection.code_verifier:
            payload["code_verifier"] = ecw_connection.code_verifier

        # Exchange code for token
        try:
            response = requests.post(
                ecw_connection.token_url,
                headers=headers,
                data=payload,
            )
            response.raise_for_status()
            try:
                token_data = response.json()
            except ValueError:
                # If response is not JSON, return error
                return JsonResponse(
                    {
                        "error": "Invalid response from token endpoint",
                        "response": response.text[:500],  # Limit response length
                    },
                    status=500,
                )
        except requests.exceptions.HTTPError as e:
            # Handle HTTP errors (4xx, 5xx)
            error_response = None
            if hasattr(e.response, "text"):
                try:
                    error_response = e.response.json()
                except ValueError:
                    error_response = {"error": e.response.text[:500]}
            return JsonResponse(
                {
                    "error": "Failed to exchange code for token",
                    "status_code": (
                        e.response.status_code if hasattr(e, "response") else None
                    ),
                    "details": error_response or str(e),
                },
                status=e.response.status_code if hasattr(e, "response") else 500,
            )
        except requests.exceptions.RequestException as e:
            return JsonResponse(
                {
                    "error": "Failed to exchange code for token",
                    "details": str(e),
                },
                status=500,
            )

        # Save tokens to connection
        ecw_connection.access_token = token_data.get("access_token")
        ecw_connection.refresh_token = token_data.get("refresh_token")
        ecw_connection.access_token_generated_at = timezone.now()
        ecw_connection.save()


        # Redirect to org_redirect_uri if set, otherwise return JSON
        if ecw_connection.org_redirect_uri:
            redirect_url = (
                ecw_connection.org_redirect_uri
                + "?"
                + urllib.parse.urlencode(
                    {
                        "status": "success",
                        "access_token": token_data.get("access_token"),
                    }
                )
            )
            return redirect(redirect_url)

        # Return JSON response with token data
        return JsonResponse(
            {
                "status": "success",
                "access_token": token_data.get("access_token"),
                "token_type": token_data.get("token_type"),
                "expires_in": token_data.get("expires_in"),
                "refresh_token": token_data.get("refresh_token"),
                "scope": token_data.get("scope"),
            },
            status=200,
        )

    except Exception as e:
        return JsonResponse(
            {"error": "Internal server error", "details": str(e)}, status=500
        )
