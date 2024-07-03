# crud関数

import platform  # プラットフォームに依存した情報を取得するためのモジュールをインポートしています。
# print(platform.uname())

from sqlalchemy import create_engine, select, insert, update
import sqlalchemy
from sqlalchemy.orm import sessionmaker
import json
from db_control.connect import engine
from db_control.dbmodels import Product_master, Transaction_detail, Transaction
from sqlalchemy import func


def search(dbmodel, code):
    Session = sessionmaker(bind=engine)
    session = Session()

    query = session.query(dbmodel).filter(dbmodel.CODE == code)
    try:
        with session.begin():
            result = query.all()
        if not result:
            return None  # 一致するコードが見つからなかった場合、Noneを返す
        result_dict_list = []
        for product_info in result:
            result_dict_list.append({
                "PRD_ID": product_info.PRD_ID,
                "CODE": product_info.CODE,
                "NAME": product_info.NAME,
                "PRICE": product_info.PRICE
            })
    except sqlalchemy.exc.IntegrityError:
        print("一意制約違反により、挿入に失敗しました")
    session.close()
    return result_dict_list

def create_transaction(dbmodel, values):
    if any(value is None for value in values.values()):
        print("値にnullが含まれているため、挿入に失敗しました")
        return "failed"
    else:
        Session = sessionmaker(bind=engine)
        session = Session()

        query = insert(dbmodel).values(values).returning(dbmodel.TRD_ID)

        try:
            with session.begin():
                result = session.execute(query)
                inserted_id = result.scalar()  # 挿入されたIDを取得
                print("挿入が成功しました")
                return inserted_id
        except sqlalchemy.exc.IntegrityError:
            print("一意制約違反により、挿入に失敗しました")
            session.rollback()
            return inserted_id
        except Exception as e:
            print(f"挿入中にエラーが発生しました: {e}")
            session.rollback()
            return "insert failed"
        finally:
            session.close()

def extract_productInfos(input_data):
    Session = sessionmaker(bind=engine)
    session = Session()

    tmp = select(Product_master).where(Product_master.NAME == input_data["name"])
    result = session.execute(tmp).fetchone()

    if result:
        product = result[0]
        return product
    else:
        return None

    # セッションを閉じる
    session.close()

def create_transactionDetails(dbmodel, values):
    if any(value is None for value in values.values()):
        print("値にnullが含まれているため、挿入に失敗しました")
        return "failed"
    else:
        Session = sessionmaker(bind=engine)
        session = Session()

        query = insert(dbmodel).values(values)

        try:
            with session.begin():
                result = session.execute(query)
                print("挿入が成功しました")
                return "insert successed"
        except sqlalchemy.exc.IntegrityError:
            print("一意制約違反により、挿入に失敗しました")
            session.rollback()
            return "failed"
        except Exception as e:
            print(f"挿入中にエラーが発生しました: {e}")
            session.rollback()
            return "failed"
        finally:
            session.close()

def calculate_totalPrice(trd_id):
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        total_price = session.query(func.sum(Transaction_detail.PRD_PRICE)).filter(Transaction_detail.TRD_ID == trd_id).scalar()
        
        if total_price is not None:
            return total_price
        else:
            return 0.0  # 一致するデータがない場合は0を返す

    except Exception as e:
        print(f"価格計算中にエラーが発生しました: {e}")
        return "calculation failed"
    finally:
        session.close()

def update_totalAmount(trd_id):
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        total_price = calculate_totalPrice(trd_id)
        if total_price == "calculation failed":
            return "calculation failed"
        
        query = update(Transaction).where(Transaction.TRD_ID == trd_id).values(TOTAL_AMT=total_price)

        with session.begin():
            session.execute(query)
            print("合計金額が更新されました")
            return "update succeeded"
    except Exception as e:
        print(f"合計金額の更新中にエラーが発生しました: {e}")
        return "update failed"
    finally:
        session.close()