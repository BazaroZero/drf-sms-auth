from drf_yasg import openapi

user_post_response = {
    "400": openapi.Response(
        description="Error: Bad Request",
        examples={
            "application/json": {"phone": ["user with this phone already exists."]}
        },
    ),
}

pair_response = {
    "200": openapi.Response(
        description="",
        examples={
            "application/json": {
                "refresh": "header.payload.signature",
                "access": "header.payload.signature",
            }
        },
    ),
    "401": openapi.Response(
        description="Error: Unauthorized",
        examples={
            "application/json": {
                "detail": "No active account found with the given credentials",
            }
        },
    ),
}

refresh_response = {
    "200": openapi.Response(
        description="",
        examples={
            "application/json": {
                "access": "header.payload.signature",
                "refresh": "header.payload.signature",
            }
        },
    ),
    "401": openapi.Response(
        description="Error: Unauthorized",
        examples={
            "application/json": {
                "detail": "Token is invalid or expired",
                "code": "token_not_valid",
            }
        },
    ),
}
