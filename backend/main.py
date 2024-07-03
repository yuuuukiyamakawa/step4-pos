# バックエンドの処理

from fastapi import FastAPI
from db_control import crud, dbmodels
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional, List, Dict, Any
import datetime
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Qiita  https://qiita.com/satto_sann/items/0e1f5dbbe62efc612a78
# fastapi  https://fastapi.tiangolo.com/ja/tutorial/cors/

class TransactionItem(BaseModel):
    name: str
    quantity: int
    price: int
    totalprice: int

class TransactionRequest(BaseModel):
    emp_cd: Optional[int] = 9999999999
    store_cd: Optional[int] = 30
    pos_no: Optional[int] = 90
    total_amt: Optional[int] = 0
    transaction: List[TransactionItem]


@app.get('/')
def read_root():
    return {'message': 'Hello World'}

@app.get("/products")
def get_productInfo(
    code: Optional[str] = None,
):
    # print(code)
    model = dbmodels.Product_master
    result = crud.search(model, code)
    # print(result)
    return result, 200

@app.post("/transactions")
def purchase(transaction_request: TransactionRequest):
    model = dbmodels.Transaction
    current_datetime = datetime.datetime.now()
    transaction_date = current_datetime.strftime('%Y-%m-%d %H:%M:%S')

    values = {
        'DATETIME': transaction_date,
        'EMP_CD': transaction_request.emp_cd,
        'STORE_CD': transaction_request.store_cd,
        'POS_NO': transaction_request.pos_no,
        'TOTAL_AMT': transaction_request.total_amt,
    }

    trd_id = crud.create_transaction(model, values)
    print("ID:", trd_id)

    for item in transaction_request.transaction:
        productInfo = crud.extract_productInfos({
            "name": item.name,
            "quantity": item.quantity,
            "price": item.price,
            "totalprice": item.totalprice
        })

        product_info_list = {
            "TRD_ID": trd_id,
            "PRD_ID": productInfo.PRD_ID,
            "PRD_CODE": productInfo.CODE,
            "PRD_NAME": productInfo.NAME,
            "PRD_PRICE": productInfo.PRICE
        }
        
        crud.create_transactionDetails(dbmodels.Transaction_detail, product_info_list)

    result = crud.calculate_totalPrice(trd_id)
    print("合計金額は", result, "円")

    crud.update_totalAmount(trd_id)

    return {"total_amt": result}, 200
