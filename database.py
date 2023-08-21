from sqlmodel import SQLModel, create_engine, Session
from .models import BankAccountRole, BankAccount

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def create_default_data():
    with Session(engine) as session:
        内部 = BankAccountRole(name="内部")
        公司 = BankAccountRole(name="公司")
        公账 = BankAccountRole(name="公账")
        财务 = BankAccountRole(name="财务")
        员工 = BankAccountRole(name="员工")
        外部 = BankAccountRole(name="外部")
        达人 = BankAccountRole(name="达人")
        客户 = BankAccountRole(name="客户")
        其他 = BankAccountRole(name="其他")

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
            account_id="416010100102101017",
            account_name="武汉寻鹰派文化传媒有限公司",
            bank="兴业银行武汉分行营业部",
            bank_short="兴业",
            role=公账,
        )
        农行公账 = BankAccount(
            name="寻鹰派",
            account_id="17-052601040012926",
            account_name="武汉寻鹰派文化传媒有限公司",
            bank="中国农业银行武汉滨湖支行",
            bank_short="农行",
            role=公账,
        )
        朱雀支付宝 = BankAccount(
            name="朱雀",
            account_id="17612733217",
            account_name="张正清",
            bank="支付宝",
            role=财务,
        )
        朱雀微信 = BankAccount(
            name="朱雀",
            account_id="cvczhuque",
            account_name="张正清",
            bank="微信",
            role=财务,
        )
        朱雀国行卡 = BankAccount(
            name="朱雀",
            account_id="6217857600034343926",
            account_name="张正清",
            bank="中国银行",
            bank_short="中国银行",
            role=财务,
        )
        朱雀兴业卡 = BankAccount(
            name="朱雀",
            account_id="622908413151317616",
            account_name="张正清",
            bank="兴业银行武汉分行营业部",
            bank_short="兴业",
            role=财务,
        )
        朱雀招行卡 = BankAccount(
            name="朱雀",
            account_id="6214832767161107",
            account_name="张正清",
            bank="招商银行",
            bank_short="招行",
            role=财务,
        )
        session.add(兴业公账)
        session.add(农行公账)
        session.add(朱雀支付宝)
        session.add(朱雀微信)
        session.add(朱雀国行卡)
        session.add(朱雀兴业卡)
        session.add(朱雀招行卡)

        session.commit()
