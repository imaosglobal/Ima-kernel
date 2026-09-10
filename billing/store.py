from api.database.supabase_rest import (
    supabase_get,
    supabase_insert,
    supabase_update,
)


class BillingStore:

    def create_customer(self, data):
        return supabase_insert(
            "billing_customers",
            data,
        )

    def get_customer(self, user_id):
        return supabase_get(
            "billing_customers",
            {"user_id": f"eq.{user_id}"},
        )

    def create_subscription(self, data):
        return supabase_insert(
            "subscriptions",
            data,
        )

    def get_subscriptions(self, user_id):
        return supabase_get(
            "subscriptions",
            {"user_id": f"eq.{user_id}"},
        )

    def create_payment(self, data):
        return supabase_insert(
            "payments",
            data,
        )

    def get_payments(self, user_id):
        return supabase_get(
            "payments",
            {"user_id": f"eq.{user_id}"},
        )

    def update_subscription(self, subscription_id, data):
        return supabase_update(
            "subscriptions",
            data,
            {"id": f"eq.{subscription_id}"},
        )


billing_store = BillingStore()
