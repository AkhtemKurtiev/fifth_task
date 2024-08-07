from typing import Optional


def add_params_in_router_filter(
    oil_id: Optional[str] = None,
    delivery_type_id: Optional[str] = None,
    delivery_basis_id: Optional[str] = None,
):
    return {
        'oil_id': oil_id,
        'delivery_type_id': delivery_type_id,
        'delivery_basis_id': delivery_basis_id
    }
