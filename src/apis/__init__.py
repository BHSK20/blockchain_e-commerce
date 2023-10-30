from starlette.routing import Route
from src.apis.health_check import HealthCheck
from src.apis.login import Login
from src.apis.logout import Logout
from src.apis.register import Register
routes = [
    # Route('/', Home),
    Route('/health_check', HealthCheck),
    Route('/login', Login),
    Route('/logout', Logout),
    Route('/register', Register),


]
