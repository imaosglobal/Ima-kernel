STATUS = {
    "founder": {
        "connected": False,
        "error": None
    },
    "product": {
        "connected": False,
        "error": None
    }
}


def check_founder():
    try:
        from ima_founder_bridge import connect
        result = connect()
        STATUS["founder"]["connected"] = result.get("connected", False)
    except Exception as e:
        STATUS["founder"]["error"] = str(e)


def check_product():
    try:
        import product.gateway.product_gateway
        STATUS["product"]["connected"] = True
    except Exception as e:
        STATUS["product"]["error"] = str(e)


def integration_status():
    check_founder()
    check_product()
    return STATUS
