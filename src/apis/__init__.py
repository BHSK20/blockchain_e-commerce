from starlette.routing import Route
from src.apis.health_check import HealthCheck
from src.apis.login import Login
from src.apis.logout import Logout
from src.apis.register import Register
from src.apis.merchant_register import MerchantRegister
from src.apis.get_order_input import GetOrderInput
from src.apis.create_order import CreateOrder
routes = [
    # Route('/', Home),
    Route('/health_check', HealthCheck),
    Route('/login', Login),
    Route('/logout', Logout),
    Route('/register', Register),
    Route('/merchant_register', MerchantRegister),
    Route('/get_order_input', GetOrderInput),
    Route('/create_order', CreateOrder),
]
