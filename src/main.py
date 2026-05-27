import datetime
from typing import Literal, Any

from fastapi import FastAPI
from pydantic import BaseModel, field_validator
from pymongo import AsyncMongoClient

db = AsyncMongoClient("mongodb://localhost:27017/")

app = FastAPI()


mock_menu = {
    "apple1": {"name": "Apple"},
    "banana1": {"name": "Banana"}
}

# export class CartItemInput {
#   @IsNotEmpty()
#   @IsString()
#   menuItemId: string;
#
#   @IsNotEmpty()
#   @IsNumber()
#   quantity: number;
#
#   @IsOptional()
#   modifiers?: Record<string, any>;
# }

class CartItemSchema(BaseModel):
    menuItemId: str
    quantity: int
    modifiers: dict[str, Any] | None = None

    @field_validator('menuItemId')
    def is_available(cls, menuItemId: int) -> int:
        if menuItemId not in mock_menu:
            raise ValueError(f'Menu item with id {menuItemId} is not available')
        return menuItemId


# export class CustomerInfoDto {
#   @IsNotEmpty()
#   @IsString()
#   name: string;
#
#   @IsOptional()
#   @IsString()
#   phone?: string;
# }

class CustomerSchema(BaseModel):
    name: str
    phone: str | None = None

# export class CheckoutFormDto {
#   @IsNotEmpty()
#   @IsString()
#   originId: string;
#
#   @IsNotEmpty()
#   @IsString()
#   menuId: string;
#
#   @IsArray()
#   @ValidateNested({ each: true })
#   @Type(() => CartItemInput)
#   items: CartItemInput[];
#
#   @IsNotEmpty()
#   @IsEnum(['card', 'wallet'])
#   paymentMethod: 'card' | 'wallet';
#
#   @ValidateNested()
#   @Type(() => CustomerInfoDto)
#   customerInfo: CustomerInfoDto;
# }

class CheckoutSchema(BaseModel):
    originId: str
    menuId: str
    paymentMethod: Literal['card', 'wallet']
    items: list[CartItemSchema]
    customerInfo: CustomerSchema


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/checkout")
async def checkout(checkout: CheckoutSchema):
    order = dict(
        checkout.model_dump(),
        createdAt = datetime.datetime.now(tz=datetime.timezone.utc),
        status = 'pending',
    )

    # print(order)
    # order_id = (await db.test_database.orders.insert_one(order)).inserted_id

    return {
      # orderId: order_id,
      "orderId": None,
      "createdAt": order["createdAt"],
      "status": 'pending',
    }
