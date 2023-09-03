from sqlmodel import SQLModel, create_engine, Session, select
from .models import *

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def create_default_data():
    with Session(engine) as session:
        内部 = AccountRole(name="内部")
        公司 = AccountRole(name="公司")
        公账 = AccountRole(name="公账")
        财务 = AccountRole(name="财务")
        员工 = AccountRole(name="员工")
        外部 = AccountRole(name="外部")
        达人 = AccountRole(name="达人")
        客户 = AccountRole(name="客户")
        其他 = AccountRole(name="其他")

        """
        - 内部
            - 公司
                - 公账
                - 财务
            - 员工
        - 外部
            - 达人
            - 客户
            - 其他
        """

        内部.childs = [公司, 员工]
        公司.childs = [公账, 财务]

        外部.childs = [达人, 客户, 其他]

        session.add(内部)
        session.add(外部)

        兴业公账 = BankAccount(
            name="寻鹰派",
            bank_account_num="416010100102101017",
            bank_account_name="武汉寻鹰派文化传媒有限公司",
            bank="兴业银行武汉分行营业部",
            bank_short="兴业",
        )
        农行公账 = BankAccount(
            name="寻鹰派",
            bank_account_num="17-052601040012926",
            bank_account_name="武汉寻鹰派文化传媒有限公司",
            bank="中国农业银行武汉滨湖支行",
            bank_short="农行",
        )
        朱雀支付宝 = BankAccount(
            name="朱雀",
            bank_account_num="17612733217",
            bank_account_name="张正清",
            bank="支付宝",
        )
        朱雀微信 = BankAccount(
            name="朱雀",
            bank_account_num="cvczhuque",
            bank_account_name="张正清",
            bank="微信",
        )
        朱雀国行卡 = BankAccount(
            name="朱雀",
            bank_account_num="6217857600034343926",
            bank_account_name="张正清",
            bank="中国银行",
            bank_short="中国银行",
        )
        朱雀兴业卡 = BankAccount(
            name="朱雀",
            bank_account_num="622908413151317616",
            bank_account_name="张正清",
            bank="兴业银行武汉分行营业部",
            bank_short="兴业",
        )
        朱雀招行卡 = BankAccount(
            name="朱雀",
            bank_account_num="6214832767161107",
            bank_account_name="张正清",
            bank="招商银行",
            bank_short="招行",
        )

        公司 = Account(name="海外创作者联盟", role=公账, bank_accounts=[兴业公账, 农行公账])
        朱雀财务 = Account(
            name="朱雀财务", role=财务, bank_accounts=[朱雀微信, 朱雀支付宝, 朱雀国行卡, 朱雀兴业卡, 朱雀招行卡]
        )

        session.add(公司)
        session.add(朱雀财务)

        session.commit()


# def create_test_data():
#     with Session(engine) as session:
#         # 客户合并打款 = MoneyFlow(amount=25000, )
#         ...
