from sqlmodel import SQLModel, create_engine, Session, select
from sqlalchemy import func

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
            name="兴业公账",
            bank_account_num="416010100102101017",
            bank_account_name="武汉寻鹰派文化传媒有限公司",
            bank="兴业银行武汉分行营业部",
            bank_short="兴业",
        )
        农行公账 = BankAccount(
            name="农行公账",
            bank_account_num="17-052601040012926",
            bank_account_name="武汉寻鹰派文化传媒有限公司",
            bank="中国农业银行武汉滨湖支行",
            bank_short="农行",
        )
        朱雀支付宝 = BankAccount(
            name="朱雀支付宝",
            bank_account_num="17612733217",
            bank_account_name="张正清",
            bank="支付宝",
        )
        朱雀微信 = BankAccount(
            name="朱雀微信公账",
            bank_account_num="cvczhuque",
            bank_account_name="张正清",
            bank="微信",
        )
        朱雀国行卡 = BankAccount(
            name="朱雀国行公账",
            bank_account_num="6217857600034343926",
            bank_account_name="张正清",
            bank="中国银行",
            bank_short="中国银行",
        )
        朱雀兴业卡 = BankAccount(
            name="朱雀兴业公账",
            bank_account_num="622908413151317616",
            bank_account_name="张正清",
            bank="兴业银行武汉分行营业部",
            bank_short="兴业",
        )
        朱雀招行卡 = BankAccount(
            name="朱雀招行公账",
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


def create_test_data():
    with Session(engine) as session:
        客户身份 = session.get(AccountRole, 6)
        达人身份 = session.get(AccountRole, 5)

        京东客户 = Account(
            name="京东客户", role=客户身份, bank_accounts=[京东客户账户 := BankAccount(name="京东客户账户")]
        )

        兴业公账 = session.get(BankAccount, 1)

        客户合并打款 = MoneyFlow(
            name="客户合并打款A",
            amount=25_000,
            flow_details=[
                客户合并打款开心 := MoneyFlowDetail(name="客户合并打款开心", amount=20_000),
                客户合并打款羊羊 := MoneyFlowDetail(name="客户合并打款羊羊", amount=5_000),
            ],
            bank_account_out=京东客户账户,
            bank_account_in=兴业公账,
        )

        开心 = Account(name="开心姐", role=达人身份)
        机构 = session.get(Account, 1)
        开心京东商单 = MoneyBill(
            name="开心京东商单",
            type="商单",
            flow_details=[
                客户合并打款开心,
                开心商单分成流水 := MoneyFlowDetail(name="开心商单分成", amount=12_000),
            ],
            bill_details=[
                开心分成账单 := MoneyBillDetail(name="开心分成账单", account=开心, amount=12000),
                机构分成账单 := MoneyBillDetail(name="机构分成账单", account=机构, amount=8000),
            ],
        )
        session.add(开心京东商单)
        session.commit()


def create_test_select():
    with Session(engine) as session:
        机构 = session.get(Account, 1)
        商单 = session.get(MoneyBill, 1)

        开心商单入账 = session.exec(
            select(func.sum(MoneyFlowDetail.amount))
            .join(MoneyFlow)
            .join(BankAccount, onclause=MoneyFlow.bank_account_in)
            .join(Account)
            .join(MoneyBill)
            .where(Account.id == 1)
            .where(MoneyBill.id == 1)
        ).one()
        print("### 开心商单入账")
        print(开心商单入账)
