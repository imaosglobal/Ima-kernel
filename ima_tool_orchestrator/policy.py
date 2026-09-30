SAFE_RISKS={"low","medium"}
class PolicyGate:
    def authorize(self,capability,request):
        if not capability or not capability.enabled: return False,"capability_disabled"
        if capability.risk not in SAFE_RISKS: return False,"explicit_authorization_required"
        if request.require_confirmation: return False,"user_confirmation_required"
        if request.context.get("time_space") and request.context["time_space"].get("human_authorization_required", True) is not True:
            return False,"time_space_authorization_required"
        return True,"authorized"
