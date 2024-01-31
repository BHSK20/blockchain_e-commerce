from starlette.routing import Route
from src.apis.health_check import HealthCheck
from src.apis.login import Login
from src.apis.logout import Logout
from src.apis.register import Register
from src.apis.checkout import Checkout
routes = [
    # Route('/', Home),
    Route('/health_check', HealthCheck),
    Route('/login', Login),
    Route('/logout', Logout),
    Route('/register', Register),
    Route('/checkout', Checkout),


]
