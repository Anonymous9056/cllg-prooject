from supertokens_python import init, InputAppInfo, SupertokensConfig
from supertokens_python.recipe import thirdparty, emailpassword, session
from supertokens_python.recipe.thirdparty.provider import ProviderInput, ProviderConfig, ProviderClientConfig
from core.config import settings

def init_supertokens():
    init(
        app_info=InputAppInfo(
            app_name=settings.PROJECT_NAME,
            api_domain=settings.API_URL,
            website_domain=settings.WEBSITE_URL,
            api_base_path="/api/auth",
            website_base_path="/auth"
        ),
        supertokens_config=SupertokensConfig(
            connection_uri="https://try.supertokens.com",
            # api_key=settings.SUPERTOKENS_API_KEY
        ),
        framework='fastapi',
        recipe_list=[
            session.init(),
            thirdparty.init(
                sign_in_and_up_feature=thirdparty.SignInAndUpFeature(
                    providers=[
                        # We have provided you with development keys which you can use for testing.
                        # IMPORTANT: Please replace them with your own OAuth keys for production use.
                        ProviderInput(
                            config=ProviderConfig(
                                third_party_id="google",
                                clients=[
                                    ProviderClientConfig(
                                        client_id="1060725074195-kmeum4crr01uirfl2op9kd5acmi9jutn.apps.googleusercontent.com",
                                        client_secret="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",
                                    ),
                                ],
                            ),
                        ),
                    ]
                )
            ),
            emailpassword.init()
        ],
        mode='asgi'
    )   