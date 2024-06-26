from starlette.routing import Route
from src.apis.health_check import HealthCheck
from src.apis.login import Login
from src.apis.logout import Logout
from src.apis.register import Register
from src.apis.merchant_register import MerchantRegister
from src.apis.get_order_input import GetOrderInput
from src.apis.create_order import CreateOrder
from src.apis.refresh_token import RefreshToken
from src.apis.user_info import UserPayload, MerchantInfo
from src.apis.transfer import Transfer, TransferOrder
from src.apis.balance import Balance
from src.apis.order import OrdersUser, OrdersMerchant
from src.apis.transfer_log import TransferLog, TransferOrderLog
from src.apis.deposit import Deposit
from src.apis.user_info_KYC import UserInfoKYC
routes = [
    # Route('/', Home),
    Route('/health_check', HealthCheck),
    Route('/login', Login),
    Route('/logout', Logout),
    Route('/register', Register),
    Route('/merchant_register', MerchantRegister),
    Route('/get_order_input', GetOrderInput),
    Route('/create_order', CreateOrder),
    Route('/refresh_token', RefreshToken),
    Route('/user/payload', UserPayload),
    Route('/merchant', MerchantInfo),
    Route('/transfer', Transfer),
    Route('/transfer/{order_id}', TransferOrder),
    Route('/balance', Balance),
    Route('/orders/user', OrdersUser),
    Route('/orders/merchant', OrdersMerchant),
    Route('/transactions', TransferLog),
    Route('/transactions/order', TransferOrderLog),
    Route('/deposit', Deposit),
    Route('/user_info', UserInfoKYC),
    
]
