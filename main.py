from fastapi import FastAPI
from products.controllers import products_routers
from users.controllers import users_routers
from orders.controllers import orders_routers


app = FastAPI(title='ecommerce-app')

app.include_router(router=products_routers)
app.include_router(router=users_routers)
app.include_router(router=orders_routers)



